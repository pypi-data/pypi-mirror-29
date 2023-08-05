from __future__ import print_function

import os
import sys
import re
import atexit
from signal import signal, SIGABRT, SIGINT, SIGTERM
import webbrowser
import argparse
try:
    from ConfigParser import SafeConfigParser as ConfigParser
except ImportError:
    from configparser import ConfigParser
try:
    from shlex import quote
except ImportError:
    from pipes import quote

from pexpect import pxssh

from .utils import (eprint, join_cmd, check_dns, try_quit_xquartz)
from .pysectools import (zero, Pinentry, PINENTRY_PATH)


JO2_DEFAULTS = {
    "DEFAULT_HOST": "o2.hms.harvard.edu",
    "DEFAULT_JP_PORT": "8887",
    "DEFAULT_JP_TIME": "0-12:00",
    "DEFAULT_JP_MEM": "1G",
    "DEFAULT_JP_CORES": "1",
    "DEFAULT_JP_SUBCOMMAND": "notebook",
    "MODULE_LOAD_CALL": "",
    "SOURCE_JUPYTER_CALL": "",
}

config = ConfigParser(defaults=JO2_DEFAULTS)
config.add_section('Defaults')
config.add_section('Settings')

CFG_FILENAME = "jupyter-o2.cfg"
CFG_DIR = "jupyter-o2"

if not config.read([
    CFG_FILENAME,  # jupyter-o2.cfg
    os.path.join(os.path.expanduser("~"), "." + CFG_FILENAME),  # ~/.jupyter-o2.cfg
    os.path.join(sys.prefix, "etc", CFG_DIR, CFG_FILENAME),  # etc/jupyter-o2/jupyter-o2.cfg
    os.path.join("/usr/local/etc", CFG_DIR, CFG_FILENAME),  # /usr/local/etc/jupyter-o2/jupyter-o2.cfg
    os.path.join("/etc", CFG_DIR, CFG_FILENAME)  # /etc/jupyter-o2/jupyter-o2.cfg
]):
    print("Config file could not be read. Using internal defaults.")

DEFAULT_HOST = config.get('Defaults', 'DEFAULT_HOST')
DEFAULT_JP_PORT = config.getint('Defaults', 'DEFAULT_JP_PORT')
DEFAULT_JP_TIME = config.get('Defaults', 'DEFAULT_JP_TIME')
DEFAULT_JP_MEM = config.get('Defaults', 'DEFAULT_JP_MEM')
DEFAULT_JP_CORES = config.getint('Defaults', 'DEFAULT_JP_CORES')
DEFAULT_JP_SUBCOMMAND = config.get('Defaults', 'DEFAULT_JP_SUBCOMMAND')

MODULE_LOAD_CALL = config.get('Settings', 'MODULE_LOAD_CALL')
SOURCE_JUPYTER_CALL = config.get('Settings', 'SOURCE_JUPYTER_CALL')

JO2_ARG_PARSER = argparse.ArgumentParser(description='Launch and connect to a Jupyter session on O2.')
JO2_ARG_PARSER.add_argument("user", type=str, help="O2 username")
JO2_ARG_PARSER.add_argument("subcommand", help="the subcommand to launch")
JO2_ARG_PARSER.add_argument("--host", type=str, default=DEFAULT_HOST, help="Host to connect to")
JO2_ARG_PARSER.add_argument("-p", "--port", dest="jp_port", type=int, default=DEFAULT_JP_PORT,
                            help="Available port on your system")
JO2_ARG_PARSER.add_argument("-t", "--time", dest="jp_time", type=str, default=DEFAULT_JP_TIME,
                            help="Time to run Jupyter")
JO2_ARG_PARSER.add_argument("-m", "--mem", dest="jp_mem", type=str, default=DEFAULT_JP_MEM,
                            help="Memory to allocate for Jupyter")
JO2_ARG_PARSER.add_argument("-c", "-n", dest="jp_cores", type=int, default=DEFAULT_JP_CORES,
                            help="Cores to allocate for Jupyter")
JO2_ARG_PARSER.add_argument("-k", "--keepalive", default=False, action='store_true',
                            help="Keep interactive session alive after exiting Jupyter")
JO2_ARG_PARSER.add_argument("--kq", "--keepxquartz", dest="keepxquartz", default=False, action='store_true',
                            help="Do not quit XQuartz")
JO2_ARG_PARSER.add_argument("-Y", "--ForwardX11Trusted", dest="forwardx11trusted", default=False, action='store_true',
                            help="Enables trusted X11 forwarding. Equivalent to ssh -Y.")

SRUN_CALL_FORMAT = "srun -t {} --mem {} -c {} --pty -p interactive --x11 /bin/bash"
JP_CALL_FORMAT = "jupyter {} --port={} --browser='none'"

# patterns to search for in ssh
SITE_PATTERN_FORMAT = "\s(https?://((localhost)|(127\.0\.0\.1)):{}[\w\-./%?=]+)\s"  # {} formatted with jupyter port
PASSWORD_PATTERN = re.compile(b"[\w-]+@[\w-]+'s password: ")  # e.g. "user@compute-e-16-175's password: "

if sys.version_info.major >= 3:
    STDOUT_BUFFER = sys.stdout.buffer
else:
    STDOUT_BUFFER = sys.stdout


class CustomSSH(pxssh.pxssh):
    def login(self, *args, **kwargs):
        """Login and suppress the traceback for pxssh exceptions (such as incorrect password errors)."""
        try:
            super(CustomSSH, self).login(*args, **kwargs)
        except pxssh.ExceptionPxssh as err:
            eprint("pxssh error: {}".format(err))
            sys.exit(1)

    def silence_logs(self):
        """Prevent printing into any logfile."""
        self.logfile = None
        self.logfile_read = None
        self.logfile_send = None

    def digest_all_prompts(self, timeout=0.5):
        """Digest all prompts until there is a delay of <timeout>."""
        if timeout == -1:
            timeout = self.timeout
        while self.prompt(timeout):
            pass


class FilteredOut(object):
    def __init__(self, txtctrl, by):
        self.txtctrl = txtctrl
        self.by = by

    def write(self, bytestr):
        try:
            if bytestr[:len(self.by)] == self.by:
                self.txtctrl.write(bytestr)
        except IndexError:
            pass

    def flush(self):
        self.txtctrl.flush()

    def exit_on_find(self, bytestr):
        if self.by in bytestr:
            sys.exit(0)
        return bytestr


class JupyterO2(object):
    def __init__(
            self,
            user,
            host,
            subcommand=DEFAULT_JP_SUBCOMMAND,
            jp_port=DEFAULT_JP_PORT,
            jp_time=DEFAULT_JP_TIME,
            jp_mem=DEFAULT_JP_MEM,
            jp_cores=DEFAULT_JP_CORES,
            keepalive=False,
            keepxquartz=False,
            forwardx11trusted=False,
    ):
        self.user = user
        self.host = host
        self.subcommand = subcommand
        self.jp_port = jp_port
        self.keep_alive = keepalive
        self.keep_xquartz = keepxquartz

        self.srun_call = SRUN_CALL_FORMAT.format(quote(jp_time), quote(jp_mem), jp_cores)
        self.jp_call = JP_CALL_FORMAT.format(quote(subcommand), jp_port)

        self.__o2_pass = ""
        self.__pinentry = Pinentry(pinentry_path=PINENTRY_PATH, fallback_to_getpass=True)

        login_ssh_options = {
            "ForwardX11": "yes",
            "LocalForward": "{} 127.0.0.1:{}".format(jp_port, jp_port),
            "PubkeyAuthentication": "no"
        }
        if forwardx11trusted:
            login_ssh_options["ForwardX11Trusted"] = "yes"

        self.__login_ssh = CustomSSH(timeout=60, ignore_sighup=False, options=login_ssh_options)

        self.__second_ssh = CustomSSH(timeout=10, ignore_sighup=False, options={"PubkeyAuthentication": "no"})

        # perform close() on exit or interrupt
        atexit.register(self.close)
        self.flag_exit = False
        for sig in (SIGABRT, SIGINT, SIGTERM):
            signal(sig, self.term)

    def ask_for_pin(self):
        self.__o2_pass = self.__pinentry.ask(
            prompt="Enter your passphrase: ",
            description="Connect to O2 server for jupyter {}".format(self.subcommand),
            error="No password entered", validator=lambda x: x is not None and len(x) > 0)
        self.__pinentry.close()

    def connect(self):
        """
        First SSH into an interactive node and run jupyter.
        Then SSH into that node to set up forwarding.
        Finally, open the jupyter notebook page in the browser.
        """
        # start login ssh
        print("ssh {}@{}".format(self.user, self.host))
        dns_err, host = check_dns(self.host)
        if dns_err == 1:
            print("ssh {}@{}".format(self.user, host))
        elif dns_err == 2:
            sys.exit(1)
        self.__login_ssh.force_password = True
        self.__login_ssh.silence_logs()
        self.__login_ssh.login(host, self.user, self.__o2_pass)

        # get the login hostname
        self.__login_ssh.sendline("hostname")
        self.__login_ssh.prompt()
        jp_login_host = self.__login_ssh.before.decode('utf-8').strip().split('\n')[1]
        print("hostname: {}".format(jp_login_host))

        # enter an interactive session
        print()
        self.__login_ssh.PROMPT = PASSWORD_PATTERN
        self.__login_ssh.logfile_read = FilteredOut(STDOUT_BUFFER, b'srun')
        self.__login_ssh.sendline(self.srun_call)
        if not self.__login_ssh.prompt():
            eprint("The timeout ({}) was reached.".format(self.__login_ssh.timeout))
            sys.exit(1)
        self.__login_ssh.silence_logs()
        self.__login_ssh.sendline(self.__o2_pass)

        # within interactive: get the name of the interactive node
        self.__login_ssh.PROMPT = self.__login_ssh.UNIQUE_PROMPT
        self.__login_ssh.sendline("unset PROMPT_COMMAND; PS1='[PEXPECT]\$ '")
        self.__login_ssh.prompt()
        self.__login_ssh.sendline("hostname | sed 's/\..*//'")
        self.__login_ssh.prompt()
        jp_interactive_host = self.__login_ssh.before.decode('utf-8').strip().split('\n')[1]
        print("interactive node: {}\n".format(jp_interactive_host))

        # start jupyter
        if MODULE_LOAD_CALL:
            print(join_cmd("module load", MODULE_LOAD_CALL))
            self.__login_ssh.sendline(join_cmd("module load", MODULE_LOAD_CALL))
            self.__login_ssh.prompt()
        if SOURCE_JUPYTER_CALL:
            print(join_cmd("source", SOURCE_JUPYTER_CALL))
            self.__login_ssh.sendline(join_cmd("source", SOURCE_JUPYTER_CALL))
            self.__login_ssh.prompt()
        self.__login_ssh.sendline(self.jp_call)
        self.__login_ssh.logfile_read = STDOUT_BUFFER

        # get the address jupyter is running at
        site_pat = re.compile(SITE_PATTERN_FORMAT.format(self.jp_port).encode('utf-8'))
        self.__login_ssh.PROMPT = site_pat
        if not self.__login_ssh.prompt():  # timed out; failed to launch jupyter
            eprint("Failed to launch jupyter. (timed out, {})".format(self.__login_ssh.timeout))
            if self.keep_alive:
                eprint("Starting interactive mode.")
                self.interact()
            else:
                sys.exit(1)
        jp_site = self.__login_ssh.after.decode('utf-8').strip()

        # log in to the second ssh
        print("\nssh {}@{}".format(self.user, jp_login_host))
        dns_err, jp_login_host = check_dns(jp_login_host)
        if dns_err == 1:
            print("ssh {}@{}".format(self.user, jp_login_host))
        elif dns_err == 2:
            sys.exit(1)
        self.__second_ssh.force_password = True
        self.__second_ssh.silence_logs()
        self.__second_ssh.login(jp_login_host, self.user, self.__o2_pass)

        # ssh into the running interactive node
        print("\nssh -N -L {0}:127.0.0.1:{0} {1}".format(self.jp_port, jp_interactive_host))
        self.__second_ssh.PROMPT = PASSWORD_PATTERN
        self.__second_ssh.sendline("ssh -N -L {0}:127.0.0.1:{0} {1}".format(self.jp_port, jp_interactive_host))
        if not self.__second_ssh.prompt():
            eprint("The timeout ({}) was reached.".format(self.__second_ssh.timeout))
            sys.exit(1)
        self.__second_ssh.silence_logs()
        self.__second_ssh.sendline(self.__o2_pass)
        zero(self.__o2_pass)  # password is not needed anymore
        self.__o2_pass = None
        self.__second_ssh.logfile_read = STDOUT_BUFFER  # print any errors/output from self.__second_ssh to stdout

        # open Jupyter in browser
        print("\nJupyter is ready! Access at:\n{}\nOpening in browser...\n".format(jp_site))
        try:
            webbrowser.open(jp_site, new=2)
        except webbrowser.Error as error:
            print("Error: {}\nPlease open the Jupyter page manually.".format(error))

        # quit XQuartz because the application is not necessary to keep the connection open.
        if not self.keep_xquartz:
            try_quit_xquartz()

    def interact(self):
        """Keep the ssh session alive and allow input such as Ctrl-C to close Jupyter."""
        self.__login_ssh.silence_logs()
        if self.keep_alive:  # exit when you log out of the login shell
            interact_filter = FilteredOut(None, b'[PEXPECT]$ logout')
            self.__login_ssh.interact(output_filter=interact_filter.exit_on_find)
        else:  # exit when jupyter exits and [PEXPECT]$ appears
            interact_filter = FilteredOut(None, b'[PEXPECT]$ ')
            self.__login_ssh.interact(output_filter=interact_filter.exit_on_find)

    def close(self, cprint=print, *_):
        """cprint allows printing to be disabled if necessary using `cprint=lambda x, end=None, flush=None: None`"""
        def _cprint(*args, **kwargs):
            if sys.version_info.major == 2:
                kwargs.pop('flush', None)
            cprint(*args, **kwargs)
        _cprint("Cleaning up\r\n", end="", flush=True)
        zero(self.__o2_pass)
        self.__pinentry.close()
        if not self.__login_ssh.closed:
            _cprint("Closing login_ssh\n", end="", flush=True)
            self.__login_ssh.close(force=True)
        if not self.__second_ssh.closed:
            _cprint("Closing second_ssh\n", end="", flush=True)
            self.__second_ssh.close(force=True)

    def term(self, *_):
        if not self.flag_exit:
            self.flag_exit = True
            try:
                self.close()
            except RuntimeError:  # printing from signal can cause RuntimeError: reentrant call
                self.close(cprint=lambda x, end=None, flush=None: None)
            sys.stdout.close()
            sys.stderr.close()
            sys.stdin.close()
            os.closerange(0, 3)
            os._exit(1)


def main():
    pargs = JO2_ARG_PARSER.parse_args()

    jupyter_o2 = JupyterO2(**vars(pargs))

    jupyter_o2.ask_for_pin()
    jupyter_o2.connect()
    jupyter_o2.interact()

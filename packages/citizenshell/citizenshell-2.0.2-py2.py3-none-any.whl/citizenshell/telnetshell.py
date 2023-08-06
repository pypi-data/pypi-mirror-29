from telnetlib import Telnet
from uuid import uuid4
from time import sleep
from hashlib import md5
from os import chmod
from re import compile as compile_regex

from .abstractconnectedshell import AbstractConnectedShell
from .shellresult import ShellResult
from .streamreader import PrefixedStreamReader
from .queue import Queue
from .utils import convert_permissions

class TelnetShell(AbstractConnectedShell):

    def __init__(self, hostname, username, password=None, port=23, *args, **kwargs):
        super(TelnetShell, self).__init__(hostname, *args, **kwargs)
        self._prompt = str(uuid4())
        self._prompt_re = compile_regex(self._prompt)
        self._endl_re = compile_regex("\n")
        self._hostname = hostname
        self._username = username
        self._password = password
        self._port = port
        self._telnet = Telnet()
        self._is_connected = False
        self._buffer = ""
        self.connect()
        self._available_commands = None

    def do_connect(self):
        self._telnet.open(self._hostname, self._port)
        self._read_until("login: ")
        self._write(self._username + "\n")
        if self._password:
            self._read_until("Password: ")
            self._write(self._password + "\n")            
        sleep(.1)
        self._write("export PS1=%s\n" % self._prompt)
        self._read_until(self._prompt)
        self._read_until(self._prompt)

        self._write("export COLUMNS=500\n")
        self._read_until(self._prompt)

    def do_disconnect(self):
        self._telnet.close()

    def _write(self, text):        
        self.log_spy_write(text)
        self._telnet.write(text.encode('utf-8'))

    def _read_until(self, marker):
        out = self._telnet.read_until(marker.encode('utf-8'))
        self.log_spy_read(out)
        return out

    def readline(self):
        (index, _, line) = self._telnet.expect([self._endl_re, self._prompt_re])
        self.log_spy_read(line.decode('utf-8').rstrip("\n\r"))
        if index == 0:
            return line            
        return None         

    def execute_command(self, command, env={}, wait=True, check_err=False):    
        wrapped_command = PrefixedStreamReader.wrap_command(command, env)
        self._write(wrapped_command + "\n")
        queue = Queue()
        PrefixedStreamReader(self, queue)
        return ShellResult(command, queue, wait, check_err)

    def detect_available(self):
        if self._available_commands is None:
            self._available_commands = []
            for command in [ "md5", "md5sum", "hexdump", "od" ]:
                if self.execute_command("which %s" % command).exit_code() == 0:
                    self._available_commands.append(command)

    def compute_md5(self, remote_path):
        self.detect_available()
        if "md5sum" in self._available_commands:
            result = self.execute_command("md5sum '%s'" % remote_path)
            return str(result).split()[0].strip() if result else None
        elif "md5" in self._available_commands:
            result = self.execute_command("md5 '%s'" % remote_path)
            return str(result).split()[0].strip() if result else None
        return None

    def hexdump(self, remote_path):
        self.detect_available()
        if "hexdump" in self._available_commands:
            result = self.execute_command("hexdump -C %s | cut -c 10-60" % remote_path)
            return str(result).replace(" ", "").rstrip("\r\n")
        elif "od" in self._available_commands:
            result = self.execute_command("od -t x1 -An %s" % remote_path)
            return str(result).replace(" ", "").rstrip("\r\n")
        return None
        
    def pull(self, local_path, remote_path):
        self.log_oob("pulling '%s' <- '%s'..." % (local_path, remote_path))        
        result = self.execute_command("ls -la %s" % remote_path)
        permissions = convert_permissions(str(result).split()[0])
        remote_md5 = self.compute_md5(remote_path)
        content = self.hexdump(remote_path).decode('hex')
        if remote_md5 and (md5(content).hexdigest() != remote_md5):
            raise RuntimeError("file transfer error")
        open(local_path, "wb").write(content)
        chmod(local_path, permissions)
        self.log_oob("done!")
        
    def reboot_wait_and_reconnect(self, reboot_delay=40):
        # TODO(cme): add oob logging
        self._write("reboot\n")
        self.log_stdin("reboot")
        self.disconnect()
        sleep_left=reboot_delay
        sleep_delta=5
        while sleep_left > 0:
            self.log_oob("reconnecting in %d sec..." % (sleep_left))
            sleep(sleep_delta)
            sleep_left -= sleep_delta
        self.connect()



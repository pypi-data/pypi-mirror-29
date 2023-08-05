from .abstractcharshell import AbstractCharacterBasedShell
from .shellresult import ShellResult

from time import sleep
from serial import serial_for_url, EIGHTBITS, PARITY_NONE
from uuid import uuid4


class SerialShell(AbstractCharacterBasedShell):

    def __init__(self, port, baudrate=115200, bytesize=EIGHTBITS, parity=PARITY_NONE, username=None, password=None, check_xc=False, check_err=False, **kwargs):
        AbstractCharacterBasedShell.__init__(self, check_xc, check_err, **kwargs)
        
        if bytesize not in [ 5, 6, 7, 8 ]:
            raise ValueError("invalid bytesize '%d'" % bytesize)

        self._port = port
        self._baudrate = baudrate
        self._bytesize = bytesize
        self._parity = parity
        self._username = username
        self._password = password        
        self._connected = False
        self.connect()

    def connect(self):
        if not self._connected:            
            self.log_oob("connecting to '%s'..." % self._port)
            self._serial = serial_for_url(self._port, baudrate=self._baudrate, parity=self._parity, bytesize=self._bytesize)
            if self._username:
                self._write("\n" * 3)
                sleep(.1)
                out = self._read_available()
                if not out.endswith("login: "):
                    self._write("exit\n")
                    self._read_until("login: ")
                self._write(self._username + "\n")
                if self._password:
                    self._read_until("Password: ")
                    self._write(self._password + "\n")
                sleep(.1)
            self._write("export COLUMNS=500\n")
            self._write("export PS1=%s\n" % self._prompt)
            self._read_until(self._prompt)
            self._read_until(self._prompt)
            self._inject_env(self.get_global_env())
            self.log_oob("connected!")
            self._connected = True

    def disconnect(self):
        if self._connected:
            self.log_oob("disconnecting from '%s'..." % self._port)
            self._cleanup_env(self.get_global_env())
            self._write("exit\n")
            self._serial.close()
            self.log_oob("disconnected!")
            self._connected = False
        
    def _write(self, text):
        self.log_spy(">>> " + text)
        self._serial.write(text.encode("utf-8"))

    def _read_available(self):
        out = ''
        while self._serial.in_waiting:
            out += self._serial.read(self._serial.in_waiting)
        self.log_spy("<<< " + out)
        return out

    def _read_until(self, marker):
        out = ''
        while True:
            out += self._serial.read(1)
            if out.endswith(marker):
                break
        self.log_spy("<<< " + out)
        return out


from .loggers import stdin_logger, stdout_logger, stderr_logger, oob_logger, spy_read_logger, spy_write_logger
from .shellerror import ShellError


class AbstractShell(dict):

    @staticmethod
    def log_stdin(line):        
        stdin_logger.info(line.rstrip("\n\r"))

    @staticmethod
    def log_stdout(line):
        stdout_logger.info(line.rstrip("\n\r"))

    @staticmethod
    def log_stderr(line):
        stderr_logger.error(line.rstrip("\n\r"))

    @staticmethod
    def log_oob(line):
        oob_logger.info(line.rstrip("\n\r"))

    @staticmethod
    def log_spy_read(line):
        spy_read_logger.debug(line.rstrip("\n\r"))

    @staticmethod
    def log_spy_write(line):
        spy_write_logger.debug(line.rstrip("\n\r"))
    

    def __init__(self, check_xc=False, check_err=False, wait=True, **kwargs):        
        dict.__init__(self, kwargs)
        self._local_env = {}
        self._check_xc = check_xc
        self._check_err = check_err
        self._wait = wait

    def __call__(self, cmd, check_xc=None, check_err=None, wait=None, **kwargs):
        check_xc = check_xc if check_xc is not None else self._check_xc
        check_err = check_err if check_err is not None else self._check_err
        wait = wait if wait is not None else self._wait

        env = dict(self)
        env.update(kwargs)
        self._result = self.execute_command(cmd, env, wait, check_err)

        if check_xc and self._result.exit_code() != 0:
            raise ShellError(cmd, "exit code '%s'" % str(self._result.exit_code()))
        return self._result

    def wait(self):
        self._result.wait()

    def execute_command(self, cmd, env, wait, check_xc):
        raise NotImplementedError("this method must be implemented by the subclass")

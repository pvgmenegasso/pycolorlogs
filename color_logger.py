from distutils.debug import DEBUG
import logging
from typing import Optional

from colors import bcolors

class ColorFormatter(logging.Formatter):

    BASEFORMAT : str = f'%(asctime)s %(filename)s | %(levelname)s:'
    MESSAGE : str = f'%(message)s'
    FORMATS = {
            logging.INFO : f'{bcolors.OKBLUE}{BASEFORMAT}{bcolors.ENDC} {MESSAGE}',
            logging.DEBUG : f'{bcolors.OKGREEN}{BASEFORMAT}{bcolors.ENDC} {MESSAGE}',
            logging.WARNING : f'{bcolors.WARNING}{BASEFORMAT}{bcolors.ENDC} {MESSAGE}',
            logging.ERROR : f'{bcolors.FAIL}{bcolors.BOLD}{BASEFORMAT}{bcolors.ENDC} {MESSAGE}'
        }
    DATEFMT = '%d/%m-%X'

    def __init__(self, fmt: Optional[str] = ..., datefmt: Optional[str] = ..., validate: bool = ...) -> None:
        super().__init__()

    def format(self, record: Optional[logging.LogRecord]) -> str:
        if record is not None:
            newformat = logging.Formatter(fmt = self.FORMATS.get(record.levelno)
            , datefmt=self.DATEFMT)
            return newformat.format(record)
       



def init_logs(severity : int):

    try:
        assert severity in (
            logging.CRITICAL,
            logging.DEBUG,
            logging.ERROR,
            logging.FATAL,
            logging.INFO,
            logging.WARN,
            logging.WARNING,
            )
    except:
        Warning('Log severity level not found')

    
    log = logging.getLogger()
    log.setLevel(severity)
    sh = logging.StreamHandler()
    sh.setFormatter(ColorFormatter())
    log.removeHandler(log.handlers)
    log.addHandler(sh)

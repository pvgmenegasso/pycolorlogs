import logging
from typing import ClassVar, Dict, Optional, TextIO, Tuple, Union
from dataclasses import dataclass
from sys import version_info


if version_info.major > 2:
    if version_info.minor < 10:
        from typing_extensions import Literal
    else:
        from typing import Literal

BRIGHT_OPT = (';', 1)

@dataclass
class AscIIColors:

    ENDC : ClassVar[Literal['\033[0m']] = '\033[0m'
    COLORFMT : ClassVar[Literal['\033[{color_id}{opt}{opt_arg}m']] = "\033[{color_id}{opt}{opt_arg}m"
    CODES : ClassVar[Dict[str, int]] = {
        'bold' : 1,
        'light' : 2,
        'italic' : 3,
        'underline' : 4,
        'blinking' : 5,
        'white_bg' : 7,
        'dark' : 8,
        'striketrough' : 9,
        'gray' : 30,
        'red' : 31,
        'green' :  32,
        'yellow' : 33,
        'ocean_blue' : 34,
        'pink' : 35,
        'cyan' : 36,
        'white' : 37,
        'gray_bg' : 40,
        'red_bg' : 41,
        'green_bg' : 42,
        'yellow_bg' : 43,
        'blue_bg' : 44,
        'rose_bg' : 45,
        'fuschia_bg' : 46,
        'white_bg' : 47,
        'pastel_red' :91,
        'pastel_gray_bg' : 100,
        'pastel_red_bg' : 101,
        'pastel_green_bg' : 102,
        'pastel_yellow_bg' : 103,
        'pastel_blue_bg' : 104,
        'pastel_rose_bg' : 105,
        'pastel_cyan_bg' : 106,
        'pastel_white_bg' : 107
    }


    @classmethod
    def parse_fmt(cls, color_id : int, opt : Optional[Tuple[str, int]] = None) -> str:
        map = {
            'color_id' : f'{color_id}',
            'opt' : '',
            'opt_arg' : ''
        }
        if opt:
            map['opt'] = opt[0]
            map['opt_arg'] = f'{opt[1]}'
        return AscIIColors.COLORFMT.format_map(map)

    @classmethod
    def make_color(
        cls, 
        color_name : Union[str, int, Tuple[int, int]]
    ) -> str:
        aux_map : Optional[Tuple[str, int]] = None
        if isinstance(color_name, str):
            if color_name.count('bright') > 0:
                aux_map = BRIGHT_OPT
                color_name = color_name.replace('bright', '')
            if color_name in list(AscIIColors.CODES.keys()):
                return AscIIColors.parse_fmt(color_id=AscIIColors.CODES[color_name], opt = aux_map)
        if isinstance(color_name, int):
            if color_name in list(AscIIColors.CODES.values()):
                return AscIIColors.parse_fmt(color_id=color_name, opt=aux_map)
        if isinstance(color_name, Tuple):
            if isinstance(color_name[0], int):
                if color_name[0] in list(AscIIColors.CODES.values()):
                    return AscIIColors.parse_fmt(color_id=color_name[0], opt=BRIGHT_OPT)
        return AscIIColors.parse_fmt(color_id = 10)

        for entry in inspect.stack(10):
            print(entry.frame.f_locals)
        print(getframeinfo(frame =currentframe(), context=10))    
        raise IndexError('Invalid color name !')

@dataclass
class ColorFormatter(logging.Formatter):
    
    # HEADER : Literal['\033[95m'] = '\033[95m'
    # OKBLUE : Literal['\033[94m'] = '\033[94m' 
    # OKCYAN : Literal['\033[96m'] = '\033[96m'
    # OKGREEN : Literal['\033[92m'] = '\033[92m'
    # WARNING : Literal['\033[93m'] = '\033[93m'
    # FAIL : Literal['\033[91m'] = '\033[91m'
    # BOLD : Literal['\033[1m'] = '\033[1m'
    # UNDERLINE : Literal['\033[4m'] = '\033[4m'
    # MAGENTA : Literal["\033[35m"] = '\033[35m'
    # BRIGHTRED : Literal["\033[31;1m"] = '\033[31;1m'
    
    OKBLUE : ClassVar[Union[str, int]] = AscIIColors.make_color((34, 1))
    HEADER : ClassVar[Union[str , int]] = AscIIColors.make_color(35)
    OKCYAN : ClassVar[Union[str , int]] = AscIIColors.make_color(36)
    OKGREEN : ClassVar[Union[str , int]] = AscIIColors.make_color(32)
    WARNING: ClassVar[Union[str , int]] = AscIIColors.make_color(33)
    FAIL: ClassVar[Union[str , int]] = AscIIColors.make_color(8)
    BOLD: ClassVar[Union[str , int]] = AscIIColors.make_color(1)
    UNDERLINE: ClassVar[Union[str , int]] = AscIIColors.make_color(4)
    MAGENTA: ClassVar[Union[str , int]] = AscIIColors.make_color((35, 1))
    BRIGHTRED: ClassVar[Union[str , int]] = AscIIColors.make_color('brightred')
    ENDC: ClassVar[Union[str , int]] = '\033[0m'
    
    BASEFORMAT : ClassVar[str] = (
        f'%(asctime)s %(filename)s | %(levelname)s:'
    )
    EXTENDEDFORMAT : ClassVar[str] = (
        f'%(asctime)s %(filename)s l:%(lineno)d | %(levelname)s:'
    )
    MESSAGE : ClassVar[str] = f'%(message)s'
    

    FORMATS : ClassVar[Dict[int, str]] = {
        logging.INFO : f'{OKBLUE}{BASEFORMAT}{ENDC} {MESSAGE}',
        logging.DEBUG : f'{OKGREEN}{BASEFORMAT}{ENDC} {MESSAGE}',
        logging.WARNING : f'{WARNING}{BOLD}{BASEFORMAT}{ENDC} {MESSAGE}',
        logging.ERROR : f'{BRIGHTRED}{BOLD}{EXTENDEDFORMAT}{ENDC} {MESSAGE}'
    }
    DATEFMT : ClassVar[str] = '%d/%m-%X'

    def __init__(
        self, 
        fmt: Optional[str] = None, 
        datefmt: Optional[str] = None
    ) -> None:
        super().__init__(
            fmt      = fmt,
            datefmt  = datefmt
        )

    def format(self, record: logging.LogRecord) -> str:
        newformat = logging.Formatter(
            fmt = self.FORMATS.get(record.levelno),
            datefmt=self.DATEFMT
        )
        return newformat.format(record)
 

def init_logs(severity : int) -> None:

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

    log: logging.Logger = logging.getLogger()
    log.setLevel(severity)
    sh: logging.StreamHandler[TextIO] = logging.StreamHandler()
    sh.setFormatter(ColorFormatter())
    for handler in log.handlers:
        log.removeHandler(handler)
    log.addHandler(sh)
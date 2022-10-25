from pycolorlogs.colors import init_logs
from pycolorlogs import info, debug, error, warning, INFO, DEBUG, ERROR



init_logs(DEBUG)

info(f'This is an INFOrmational log message')
info(f'Use this on messages that are central to understanding your program\'s current workflow')


debug(f'This is a debug message, it usually should provide more verbose low level insight into the')
debug(f'inner workings of your program in order to check execution bugs and detailed run info')

warning(f'This is a warning message, use this to notify when something potentially dangerous happens')

error(f' AN ERROR MESSAGE, this should usually be followed by a raise statement. Indicates things that should not happen')
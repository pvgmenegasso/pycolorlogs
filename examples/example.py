# Import the module
from pycolorlogs import init_logs, DEBUG, debug, error, info

# Initialize the handler
init_logs(DEBUG)

# Log away !
info('Starting program...')
a: int = 5
b: int = 3
result: int = a+b
debug(f'The result is {result}')
try:
    denominator = randint(0, 100)
    division = 100/denominator
except:
    error('Can\'t divide by 0 !!')
finally:
    debug(f'The result is: {division}')
info('Done !')
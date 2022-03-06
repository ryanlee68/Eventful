from . import config

from .logs import setUpLogger, set_pretty_formatter, logs_dir, PrettyFormatter

set_pretty_formatter('%(levelname)s | %(name)s: %(asctime)s - [%(funcName)s()] %(message)s')
# ADD ELEMENTS TO THE ARRAY BELOW AS WEL ADD NEW FILES
for name in ['app']:
    setUpLogger(f'ucmbot.{name}', files=not config.testing)
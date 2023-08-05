# logorama
Light-weight python colored logging package

Here is a simple example

```
from logorama import logger, BaseLogger

logger.debug("Debugging...")
logger.info("Hello from Logorama")
logger.warning("This is a warning")
logger.error("THis is an ERRORRRRRRRR!!!!!")
logger.critical("THis is an EXCEPTIONNNNNNNNN!!!!!")


class LogExample(BaseLogger):
    def hello(self):
        self.logger.debug("Debugging...")
        self.logger.info("Hello from Logorama")
        self.logger.warning("This is a warning")
        self.logger.error("THis is an ERRORRRRRRRR!!!!!")
        self.logger.critical("THis is an EXCEPTIONNNNNNNNN!!!!!")

log_ex = LogExample()
log_ex.hello()

```

![alt text](./example1.png "Example 1")

Here is another example. We activate **DEBUG** logging.

```
import logging
from logorama.settings import LOGORAMA_DEFAULT_FORMAT
import colorama

from logorama import logger, BaseLogger

BaseLogger.LOG_LEVEL = logging.DEBUG

logger.setLevel(logging.DEBUG)

logger.debug("Debugging...")
logger.info("Hello from Logorama")
logger.warning("This is a warning")
logger.error("THis is an ERRORRRRRRRR!!!!!")
logger.critical("THis is an EXCEPTIONNNNNNNNN!!!!!")


class LogExample(BaseLogger):
    def hello(self):
        self.logger.debug("Debugging...")
        self.logger.info("Hello from Logorama")
        self.logger.warning("This is a warning")
        self.logger.error("THis is an ERRORRRRRRRR!!!!!")
        self.logger.critical("THis is an EXCEPTIONNNNNNNNN!!!!!")


log_ex = LogExample()
log_ex.hello()

```

![alt text](./example2.png "Example 2")







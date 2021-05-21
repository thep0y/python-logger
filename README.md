# python-logger
Colorful logger for python3

## How to use

### Install

```shell
pip install colorful-logger
```

### Usage

You can directly use the default logger, the colored logs will be printed on the terminal, and the default logger level is **warning**.

```python
from colorful_logger.logger import logger

logger.debug("This is a debug message.")
logger.info("This is a info message.")
logger.warning("This is a warning message.")
logger.error("This is a error message.")
logger.fatal("This is a fatal message.")
```

![default logger](https://cdn.jsdelivr.net/gh/thep0y/image-bed/md/1621580826694.png)

You can also change the log level, save the log to a file, change the logger name, and the log may not be output to the terminal.

```python
import logging
from colorful_logger.logger import get_logger

logger = get_logger(name="logger", level=logging.DEBUG, file_path="./test.log")

logger.debug("This is a debug message.")
logger.info("This is a info message.")
logger.warning("This is a warning message.")
logger.error("This is a error message.")
logger.fatal("This is a fatal message.")
```

![custom logger](https://cdn.jsdelivr.net/gh/thep0y/image-bed/md/1621581068178.png)

The contents of the log file:

```
[DEBUG] 2021-05-21 15:08:42 test.py:8 - This is a debug message.
[INFO] 2021-05-21 15:08:42 test.py:9 - This is a info message.
[WARNING] 2021-05-21 15:08:42 test.py:10 - This is a warning message.
[ERROR] 2021-05-21 15:08:42 test.py:11 - This is a error message.
[CRITICAL] 2021-05-21 15:08:42 test.py:12 - This is a fatal message.
```

As you can see, the log saved to the file uses the default formatter, so it is not in color.

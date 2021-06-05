> :warning: This README is translated by Google. If there is a grammatical error, please open an issue to correct it!

# python-logger

Colorful logger for python3

## How to use

### Install

```shell
pip install colorful-logger
```

### Usage

#### 1 default logger

You can directly use the default logger, the colored logs will be printed on the terminal, and the default logger level is **warning**.

```python
from colorful_logger.logger import logger

with logger:
  logger.debug("This is a debug message.")
  logger.info("This is a info message.")
  logger.warning("This is a warning message.")
  logger.error("This is a error message.")
  logger.critical("This is a critical message.")
  logger.fatal("This is a fatal message.")
```

As you can see, `logger` needs to be executed in the `with` statement, because this package uses `QueueListener` to call log output. You need to call the `start` method before using `logger` to output the log, and you need to call `after the end of use. For the stop` method, I encapsulated these two methods in the `with` statement. In non-special scenarios, there is no need to call the `start` and `stop` methods separately.

![default logger](https://cdn.jsdelivr.net/gh/thep0y/image-bed/md/1621580826694.png)

#### 2 custom logger

You can also change the log level, save the log to a file, change the logger name, and the log may not be output to the terminal.

```python
from colorful_logger.logger import get_logger, DEBUG

logger = get_logger(name="sample_logger", level=DEBUG, file_path="./test.log")

with get_logger(name="sample_logger", level=DEBUG, file_path="./test.log", file_colorful=True) as logger:
  logger.debug("This is a debug message.")
  logger.info("This is a info message.")
  logger.warning("This is a warning message.")
  logger.error("This is a error message.")
  logger.critical("This is a critical message.")
  logger.fatal("This is a fatal message.")
```

There may be unexpected situations when outputting logs outside of the `with` statement, which may not achieve the expected results.

![custom logger](https://cdn.jsdelivr.net/gh/thep0y/image-bed/md/1621653262747.png)

The content of the log file `./test.log` (example, inconsistent with the information in the above figure):

```
[DEBUG] 2021-05-21 15:08:42 test.py:8 - This is a debug message.
[INFO] 2021-05-21 15:08:42 test.py:9 - This is a info message.
[WARNING] 2021-05-21 15:08:42 test.py:10 - This is a warning message.
[ERROR] 2021-05-21 15:08:42 test.py:11 - This is a error message.
[CRITICAL] 2021-05-21 15:08:42 test.py:12 - This is a fatal message.
```

The log output to the file is not a color log by default.

If you need to save the color log in a file, set the `file_colorful` parameter to `True`. In this example, the color log is saved.

The color log file has only one function, which is to view the real-time log in the terminal:

```shell
tail -f test.log
# 或
cat test.log
```

#### 3 child logger

After defining a `logger`, I want to use all the parameters of this `logger` except `name` to output the log. At this time, you need to use the `child_logger` method to generate a child logger. The child logger needs to be in the `with` of the parent logger Execute in the statement:

```python
from colorful_logger import get_logger
from colorful_logger.logger import DEBUG

# parent logger
logger = get_logger(name="sample_logger", level=DEBUG, file_path="./test.log")

with logger:
  logger.error("parent error")
  l1 = child_logger("l1", logger)
  l1.error("l1 error")
  l1.fatal("l1 fatal")
```

The child logger is the same except that the name is different from the parent logger, and it will not output the log of the third-party library.

The execution of the child logger in the `with` statement of the parent logger does not mean that it must be called directly in the `with` statement. It can be executed in a function in the `with` statement, such as:

```python
# main.py
from colorful_logger import get_logger
from colorful_logger.logger import DEBUG

from other_file import test

# parent logger
logger = get_logger(name="sample_logger", level=DEBUG, file_path="./test.log")

with logger:
  test()
```

```python
# other_file.py

test_logger = child_logger("test_logger", logger)

def test():
  test_logger.error("test error")
```


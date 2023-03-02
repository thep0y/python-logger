> :warning: This README is translated by Google. If there is a grammatical error, please open an issue to correct it!

<h1 align="center">Python Colorful Logger</h1>

<p align="center">
    <a href="https://pepy.tech/project/colorful-logger"><img alt="Downloads" src="https://static.pepy.tech/badge/colorful-logger"></a>    
    <a href="https://pepy.tech/project/colorful-logger"><img alt="Downloads" src="https://static.pepy.tech/badge/colorful-logger/month"></a>
    <a href="https://pepy.tech/project/colorful-logger"><img alt="Downloads" src="https://static.pepy.tech/badge/colorful-logger/week"></a>
</p>

Colorful logger for python3.

## How to use

### Install

```shell
pip install colorful-logger
```

### Usage

#### 1 default logger

You can directly use the default logger, the colored logs will be printed on the terminal, and the default logger level is **warning**.

```python
from colorful_logger import logger

with logger:
    logger.debug("default logger")
    logger.info("default logger")
    logger.warning("default logger")
    logger.error("default logger")
```

As you can see, `logger` needs to be executed in the `with` statement, because this package uses `QueueListener` to call log output. You need to call the `start` method before using `logger` to output the log, and you need to call the `stop` after the end of use. I encapsulated these two methods in the `with` statement. In non-special scenarios, there is no need to call the `start` and `stop` methods separately.

![image-20230221100744751](https://s2.loli.net/2023/02/21/yXh5d9n4vO1mW3x.png)

#### 2 custom logger

You can also change the log level, save the log to a file, change the logger name, and the log may not be output to the terminal.

```python
from colorful_logger import get_logger, DEBUG


def demo_logger(to_file=False):
    file = "test_%d.log"

    l1 = get_logger(
        "demo",
        DEBUG,
        add_file_path=False,
        disable_line_number_filter=False,
        file_path=file % 1 if to_file else None,
    )
    with l1:
        l1.debug("without file path")
        l1.info("without file path")
        l1.warning("without file path")
        l1.error("without file path")

    l2 = get_logger(
        "demo",
        DEBUG,
        add_file_path=True,
        disable_line_number_filter=False,
        file_path=file % 2 if to_file else None,
    )
    with l2:
        l2.debug("with file path")
        l2.info("with file path")
        l2.warning("with file path")
        l2.error("with file path")

    l3 = get_logger(
        None,
        DEBUG,
        add_file_path=True,
        disable_line_number_filter=True,
        file_path=file % 3 if to_file else None,
    )
    with l3:
        l3.debug("without name, and with path")
        l3.info("without name, and with path")
        l3.warning("without name, and with path")
        l3.error("without name, and with path")

    l4 = get_logger(
        None,
        DEBUG,
        add_file_path=False,
        disable_line_number_filter=True,
        file_path=file % 4 if to_file else None,
    )
    with l4:
        l4.debug("without name and path")
        l4.info("without name and path")
        l4.warning("without name and path")
        l4.error("without name and path")
```

There may be unexpected situations when outputting logs outside of the `with` statement, which may not achieve the expected results.

![image-20230221100003891](https://s2.loli.net/2023/02/21/hqTSfOUobxgaQBI.png)

The content of the log file `./test.log` (example, inconsistent with the information in the above figure):

```
[90m10:09:33.146[0m [35mDEB[0m [36mdemo[0m[1m:26[0m [96m-[0m without file path
[90m10:09:33.146[0m [32mINF[0m [36mdemo[0m [96m-[0m without file path
[90m10:09:33.146[0m [33mWAR[0m [36mdemo[0m [96m-[0m without file path
[90m10:09:33.146[0m [91mERR[0m [36mdemo[0m[1m:29[0m [96m-[0m without file path
```

The log output to the file is not a color log by default.

If you need to save the color log in a file, set the `file_colorful` parameter to `True`. In this example, the color log is saved.

The color log file has only one function, which is to view the real-time log in the terminal:

- Unix

```shell
tail -f test.log
# 或
cat test.log
```

- Windows

```powershell
Get-Content -Path test.log
```

#### 3 child logger

After defining a `logger`, I want to use all the parameters of this `logger` except `name` to output the log. At this time, you need to use the `child_logger` method to generate a child logger. The child logger needs to be in the `with` of the parent logger Execute in the statement:

```python
from colorful_logger import get_logger, DEBUG

# parent logger
logger = get_logger(name="sample_logger", level=DEBUG, file_path="./test.log")

with logger:
    logger.error("parent error")
    l1 = logger.child("l1")
    l1.error("l1 error")
    l1.fatal("l1 fatal")
```

The child logger is the same except that the name is different from the parent logger, and it will not output the log of the third-party library.

The execution of the child logger in the `with` statement of the parent logger does not mean that it must be called directly in the `with` statement. It can be executed in a function in the `with` statement, such as:

```python
# log.py
from colorful_logger import get_logger, DEBUG

logger = get_logger(name="sample_logger", level=DEBUG, file_path="./test.log")
```

```python
# main.py
from log import logger
from other_file import test

with logger:
    test()
```

```python
# other_file.py

test_logger = logger.child("test_logger")

def test():
    test_logger.error("test error")
```


# python-logger
Python3 的彩色异步日志包。

## 使用方法

### 安装

```shell
pip install colorful-logger
```

### 使用

#### 1 默认 logger

可以直接使用默认的`logger`实例输出日志，默认的日志等级是`warning`：

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

如你所见，`logger`需要在`with`语句中执行，因为本包使用的是`QueueListener`调用日志输出，使用`logger`输出日志前需要调用`start`方法，使用结束后需要调用`stop`方法，我将这两个方法封装到了`with`语句中，非特殊场景下，不需要单独调用`start`和`stop`方法。

> 如果调用了`start`方法，一定要在调用日志后后执行`stop`方法

![default logger](https://cdn.jsdelivr.net/gh/thep0y/image-bed/md/1621580826694.png)

#### 2 自定义 logger

也可以自定义`name`、日志等级、是否在终端显示、是否保存日志到文件：

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

在`with`语句外输出日志时可能会有意外情况，达不到预期结果。

![custom logger](https://cdn.jsdelivr.net/gh/thep0y/image-bed/md/1621653262747.png)

日志文件`./test.log`内容（示例，与上图信息不一致）：

```
[35m[DEBUG] [0m[34m2021-06-05 20:13:26[0m  [36msample_logger - [0mThis is a debug message.
[32m[INFO]  [0m[34m2021-06-05 20:13:26[0m  [36msample_logger - [0mThis is a info message.
[33m[WARN]  [0m[34m2021-06-05 20:13:26[0m  [36msample_logger - [0mThis is a warning message.
[31m[ERROR] [0m[34m2021-06-05 20:13:26[0m  [33mtest.py:11[0m	[36msample_logger - [0mThis is a error message.
[31m[FATAL] [0m[34m2021-06-05 20:13:26[0m  [33mtest.py:12[0m	[36msample_logger - [0mThis is a critical message.
[31m[FATAL] [0m[34m2021-06-05 20:13:26[0m  [33mtest.py:13[0m	[36msample_logger - [0mThis is a fatal message.
```

输出到文件的日志默认不是彩色日志。

如果你需要在文件中保存彩色日志，将`file_colorful`参数设置为`True`即可，本例中保存的就是彩色日志。

彩色日志文件的作用也只有一个，就是在终端查看实时日志：

```shell
tail -f test.log
# 或
cat test.log
```

这样查看的日志才是彩色的。

>`FATAL`或`CRITICAL`本就是影响程序运行的严重错误，而 python 默认的日志管理器中此方法与其他方法没有什么区别，这让我觉得莫名其妙，在本包中，我在`fatal`方法中加入了`sys.exit(1)`用来退出程序。如果在程序出现严重错误时不想退出程序，可以调用`critical`方法。

`get_logger`方法：

```python
def get_logger(
    name: Optional[str] = None,
    level: int = logging.WARNING,
    show: bool = True,
    file_path: Optional[str] = None,
    file_colorful: bool = False,
) -> Logger: ...
```

- *name* logger 实例名，可以在不同的实例对象调用日志时为日志命名
- *level* 日志等级
- *show* 是否在终端中显示。如果你想用此彩色日志包的话，通常是想在终端显示的吧
- *file_path* 是否保存到文件。默认是`None`，当其不是`None`时，会保存到对应的文件中
- *file_colorful* 保存到文件的日志是否为彩色，默认为 False，以 python 默认的日志格式保存

#### 3 子 logger

定义完一个`logger`后，还想用此`logger`的除`name`外的所有参数输出日志，这时就需要使用`child_logger`方法生成子 logger，子 logger 需要在父 logger 的`with`语句中执行：

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

子 logger 除了 name 与父 logger 不同，其他均相同，也不会输出第三方库的日志。

子 logger 在父 logger 的`with`语句中执行并不意味着一定在`with`语句中直接调用，在`with`语句中的某个函数中执行就可以，如：

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



## TODO

- [x] 改为异步日志，毕竟加入色彩后可能会影响整个程序的性能
- [x] 改写保存文件的 formatter，使 `fatal`日志和`critical`日志分开，一个退出程序，一个不退出程序

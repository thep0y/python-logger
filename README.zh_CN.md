# python-logger
Python3 的彩色日志包。

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

logger.debug("This is a debug message.")
logger.info("This is a info message.")
logger.warning("This is a warning message.")
logger.error("This is a error message.")
logger.fatal("This is a fatal message.")
```

![default logger](https://cdn.jsdelivr.net/gh/thep0y/image-bed/md/1621580826694.png)

#### 2 自定义 logger

也可以自定义`name`、日志等级、是否在终端显示、是否保存日志到文件：

```python
from colorful_logger.logger import get_logger, DEBUG

logger = get_logger(name="sample_logger", level=DEBUG, file_path="./test.log")

logger.debug("This is a debug message.")
logger.info("This is a info message.")
logger.warning("This is a warning message.")
logger.error("This is a error message.")
logger.fatal("This is a fatal message.")
```

![custom logger](https://cdn.jsdelivr.net/gh/thep0y/image-bed/md/1621653262747.png)

日志文件`./test.log`内容

```
[DEBUG] 2021-05-22 11:21:46 - sample_logger - test.py:6 - This is a debug message.
[INFO] 2021-05-22 11:21:46 - sample_logger - test.py:7 - This is a info message.
[WARNING] 2021-05-22 11:21:46 - sample_logger - test.py:8 - This is a warning message.
[ERROR] 2021-05-22 11:21:46 - sample_logger - test.py:9 - This is a error message.
[CRITICAL] 2021-05-22 11:21:46 - sample_logger - test.py:10 - This is a fatal message.
```

输出到文件的日志没有使用彩色格式，因为我个人觉得，保存到文件中的日志没有必要是彩色的。

>`FATAL`或`CRITICAL`本就是影响程序运行的严重错误，而 python 默认的日志管理器中此方法与其他方法没有什么区别，这让我觉得莫名其妙，在本包中，我在`fatal`方法中加入了`sys.exit(1)`用来退出程序。如果在程序出现严重错误时不想退出程序，可以调用`critical`方法。

`get_logger`方法：

```python
def get_logger(
    name: Optional[str] = None,
    level: int = logging.WARNING,
    show: bool = True,
    file_path: Optional[str] = None,
) -> Logger: ...
```

- *name* logger 实例名，可以在不同的实例对象调用日志时为日志命名
- *level* 日志等级
- *show* 是否在终端中显示。如果你想用此彩色日志包的话，通常是想在终端显示的吧
- *file_path* 是否保存到文件。默认是`None`，当其不是`None`时，会保存到对应的文件中

#### 3 全局配置

一个项目中通常会有很多文件，每个文件都想使用相同样式或格式的有着不同的 name 的 logger，可以使用全局配置解决。

在项目的主文件或较先执行的文件或函数中调用全局配置方法`basic_logger`：

```python
from colorful_logger import basic_logger
from colorful_logger.logger import INFO

basic_logger(level=INFO, show=False, file_path="./test.log")
```

然后在其他文件中就可以使用不同的 name 生成有相同格式的 logger了：

```python
# a.py
import logging

logger = logging.getLogger("a")

# b.py
import logging

logger = logging.getLogger("b")
```

使用全局配置有一个问题，就是当日志等级为`NOTSET`或`DEBUG`时，生成的日志中可能会有一些第三方库的日志。

#### 4 子 logger

通常我们是不想看见第三方库的日志的，这时就需要使用`child_logger`方法生成子 logger：

```python
from colorful_logger import get_logger
from colorful_logger.logger import DEBUG

# parent logger
logger = get_logger(name="sample_logger", level=DEBUG, file_path="./test.log")

# child logger in other files
from colorful_logger import child_logger

# child1.py
child1 = child_logger("child1", logger)
# child2.py
child2 = child_logger("child2", logger)
# child3.py
child3 = child_logger(__name__, logger)
```

子 logger 除了 name 与父 logger 不同，其他均相同，也不会输出第三方库的日志。

如果项目中只有一个父 logger，可以重新写一个生成子 logger 的方法：

```python
from colorful_logger import get_logger, child_logger
from colorful_logger.logger import DEBUG

# parent logger
logger = get_logger(name="sample_logger", level=DEBUG, file_path="./test.log")

def my_child_logger(name: str):
    return child_logger(name, logger)

# child1.py
child1 = my_child_logger("child1")
# child2.py
child2 = my_child_logger("child2")
# child3.py
child3 = my_child_logger(__name__)
```

## TODO

- [ ] 改为异步日志，毕竟加入色彩后可能会影响整个程序的性能
- [ ] 改写保存文件的 formatter，使 `fatal`日志和`critical`日志分开，一个退出程序，一个不退出程序

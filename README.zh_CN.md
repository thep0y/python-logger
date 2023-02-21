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
from colorful_logger import logger

with logger:
    logger.debug("default logger")
    logger.info("default logger")
    logger.warning("default logger")
    logger.error("default logger")
```

![image-20230221105448303](https://i.imgtg.com/2023/02/21/sFcdv.png)

#### 2 自定义 logger

也可以自定义`name`、日志等级、是否在终端显示、是否保存日志到文件：

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

![image-20230221105524460](https://i.imgtg.com/2023/02/21/sFsaq.png)

日志文件`./test.log`内容（带颜色标记）

```
[90m10:09:33.146[0m [35mDEB[0m [36mdemo[0m[1m:26[0m [96m-[0m without file path
[90m10:09:33.146[0m [32mINF[0m [36mdemo[0m [96m-[0m without file path
[90m10:09:33.146[0m [33mWAR[0m [36mdemo[0m [96m-[0m without file path
[90m10:09:33.146[0m [91mERR[0m [36mdemo[0m[1m:29[0m [96m-[0m without file path
```

输出到文件的日志默认不使用彩色，但你可以手动开启文件日志颜色。

>`FATAL`或`CRITICAL`本就是影响程序运行的严重错误，而 python 默认的日志管理器中此方法与其他方法没有什么区别，这让我觉得莫名其妙，在本包中，我在`fatal`方法中加入了`sys.exit(1)`用来退出程序。如果在程序出现严重错误时不想退出程序，可以调用`critical`方法。

`get_logger`方法：

```python
def get_logger(
    name: Optional[str] = None,
    level: int = default_level,
    datefmt: str = TIME_FORMAT_WITHOUT_DATE,
    show: bool = True,
    file_path: Optional[StrPath] = None,
    file_colorful: bool = False,
    add_file_path: bool = True,
    disable_line_number_filter: bool = False,
) -> ColorfulLogger:
    ...
```

- *name* logger 实例名，可以在不同的实例对象调用日志时为日志命名
- *level* 日志等级
- *datefmt* 时间格式
- *show* 是否在终端中显示。如果你想用此彩色日志包的话，通常是想在终端显示的吧
- *file_path* 是否保存到文件。默认是`None`，当其不是`None`时，会保存到对应的文件中
- *file_colorful* 是否开启文件日志颜色
- *add_file_path* 是否添保调用文件路径
- *disable_line_number_filter* 是否关闭调用行选择器（默认只显示 debug 、error、fatal、critical 的调用行，关闭则显示全部等级的调用行）

查看文件日志：

- Unix Like

```shell
tail -f test.log
# 或
cat test.log
```

- Windows

```powershell
Get-Content [-Wait] -Path test.log
```

#### 3 全局配置

当前日志器相当于重写，不兼容内置 Logging API，所以无法使用全局配置，建议使用子 logger 代替。

#### 4 子 logger

通常我们是不想看见第三方库的日志的，这时就需要使用`child_logger`方法生成子 logger：

```python
from colorful_logger import get_logger, DEBUG

# parent logger
logger = get_logger(name="sample_logger", level=DEBUG, file_path="./test.log")

# child1.py
child1 = logger.child("child1")
# child2.py
child2 = logger.child("child2")
# child3.py
child3 = logger.child(__name__)
```

如果项目中只有一个父 logger，可以重新写一个生成子 logger 的方法：

```python
from colorful_logger import get_logger, DEBUG

# parent logger
logger = get_logger(name="sample_logger", level=DEBUG, file_path="./test.log")

def my_child_logger(name: str):
    return logger.child(name)

# child1.py
child1 = my_child_logger("child1")
# child2.py
child2 = my_child_logger("child2")
# child3.py
child3 = my_child_logger(__name__)
```

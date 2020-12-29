## 03 编写模块

模块是指在Hyperion中的一个可执行流程，负责控制爬虫、POC、指纹树校验、流量控制等的调度，把控它们之间的执行流程和关系

### 建立模块

- 创建`自定.py`文件在`./modules`目录下

- 创建自定类继承`hyperion_types.BaseModule`类，所有在`./modules`目录下继承`BaseModule`的子类将被视为模块

- 根据需求重写`arg_declare`、`hit`、`execute`成员函数，具体含义如下

  `arg_declare`: 用于注册命令行中的参数、帮助、参数约束等

  `hit`: 根据用户输入的参数判断是否选择了当前模块

  `execute`: 模块主要逻辑，若用户选择了当前模块，则执行该函数

  简单的例子:

  ```python
  class NormalModule(BaseModule):
      @staticmethod
      def arg_declare(parser: argparse.ArgumentParser):
          # 注册本模块触发的关键字，定义方式详情见argparse模块
          parser.add_argument(
              "-f",
              "--file",
              type=str,
              help="load targets from file",
              default=""
          )
          parser.add_argument(
              "-t",
              "--test",
              help="test",
              action="store_true",
              default=false
          )
      @staticmethod
      def hit(args: argparse.Namespace) -> bool:
          # 判断用户是否选择了该模块
          return args.test
      
      @staticmethod
      def execute(args: argparse.Namespace):
          # 选择该模块后的行为
          print("测试模块被执行了")
  ```

  当输入`python hyperion.py -t`时将会触发该模块

### 模块生命周期

1. 模块继承`BaseModule`类后被模块装载器载入，执行该模块的`arg_declare`函数，其原型为`arg_declare(parser: argparse.ArgumentParser) -> NoReturn`，`parser`为hyperion的parser，用于注册该模块的参数、解释等
2. 用户输入完毕后解析参数，并执行该模块的`hit`函数，其原型为`hit(args: argparse.Namespace) -> bool`，`args`为解析完毕后用户的输入，hit函数用于判断用户是否选择使用该模块，若用户选择使用该模块，则返回真，否则返回假
3. 若`hit`函数返回的结果为真，则下一步将执行该模块的`execute`函数，其原型为`execute(args: argparse.Namespace) -> NoReturn`，`args`为用户输入的参数，可通过用户的参数决定目标，参数等


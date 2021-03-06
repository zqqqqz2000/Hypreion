## 02 编写POC

在Hyperion中编写POC并不需要考虑协程，所有请求或自定义的协程将交付调度器调度

### 建立POC

- 创建`自定名称.py`文件在`./poc`目录下

- 创建自定类继承`hyperion_types.POC`类，所有在`./poc`目录下继承`POC`的子类将被视为POC

- 根据需求重写`execute`、`filter`成员函数，具体含义如下

  `filter`: 判断当前目标是否符合执行该POC的条件

  `execute`: 该POC的主体执行内容

  #### 在POC主体中发起request请求
  
  执行的http请求操作请使用`core.requester`下的`requests`进行请求，例如对`www.xxx.com`的请求请写为`自定变量 = yield requests('http://www.xxx.com')`，执行完毕后请求该网站的结果将会以`Dict`的形式存储在自定变量中，若访问出错，请使用`POC.is_error`函数进行判断是否出错，具体内容请查阅`requests`
  
  #### 在POC主体中启动自定协程
  
  将自定义的协程函数加入事件循环的方式为`yield coroutines`，例如`yield 自定协程函数(参数...)`
  
  #### 在POC主体中输出结果
  
  在进行输出时请勿使用`print`函数而使用`self.logger`进行输出，这种方式可以根据模块加载而展现出不同的输出行为
  
  **注: 退出execute函数的唯一方式为`yield`而并非return，且必须确保execute函数拥有`yield`，哪怕不返回任何内容，若需要返回内容给回调函数，请返回一个元祖对象，例如：`yield ({'code': 200},)`**
  
  **注: 若希望将POC分为多个函数编写，且函数中将发起request请求，则该函数编写要求与`execute`函数一致，且在调用时请使用`yield`调用，例如`返回结果变量 = yield 自定义的函数(参数...)`，否则和普通函数一样编写**
  
  下面为上述操作的小例子
  
  ```python
  import asyncio
  from config import Default
  from core.requester import requests
  from core.requester import mount2dispatcher
  from hyperion_types import POC
  from hyperion_types.target import Target
  import time
  
  
  # 测试自定义协程的执行
  async def sleep_return_test():
      await asyncio.sleep(3)
      return 'return success'
  
  
  # 测试自定义的发起request请求的函数
  def test_request_inner_function():
      res = yield requests('https://www.baidu.com/', timeout=1)
      yield (res['status'],)
  
  
  class Test(POC):
      # POC测试主体
      def execute(self):
          t = time.time()
          # 使用模块要求的logger输出
          self.logger.debug('Test', 'Test error')
          res = yield requests('https://111www.baiduuu.com/', timeout=1)
          # 错误捕获
          if POC.is_error(res):
              # 错误则输出错误
              self.logger.error('Test', repr(res))
          else:
              # 正常执行则输出
              self.logger.information('Test', f"status: {res['status']}")
          # 正常访问测试
          self.logger.debug('Test', 'Test normal request')
          res = yield requests('https://www.baidu.com/', timeout=1)
          # 错误捕获
          if POC.is_error(res):
              # 错误则输出错误
              self.logger.error('Test', repr(res))
          else:
              # 正常执行则输出
              self.logger.information('Test', f"status: {res['status']}")
          self.logger.information('Test', str(time.time() - t))
          self.logger.debug('Test', 'Test asyncio sleep')
          # 测试自定的协程
          t = time.time()
          async_result = yield sleep_return_test()
          self.logger.information('Test', async_result + f' sleep {time.time() - t} s')
          self.logger.debug('Test', 'Test done')
          # 测试自定义的发起请求的函数
          res = yield test_request_inner_function()
          print(*res)
          # 重要，请务必使用yield标记POC主体的退出
          yield ('测试完毕',)
  
      @staticmethod
      def filter(target: Target):
          return True
  
  
  # 为了确保poc能直接运行，编写main函数，main函数的具体含义在modules中给出
  # 逻辑与POC编写无关，此处可以不做理解
  if __name__ == '__main__':
      for i in range(100):
          target = Target('https://www.baidu.com/')
          poc = Test(target, Default)
          mount2dispatcher(poc)
  ```
### POC生命周期

1. POC类被POC装载器载入
2. 以目标初始化POC
3. POC被挂载至调度器，这是POC唯一的执行方式
4. POC执行结束或遇到错误


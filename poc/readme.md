## 02 编写POC

在Hyperion中编写POC并不需要考虑协程，所有请求或自定义的协程将交付调度器调度

### 建立POC

- 创建`自定名称.py`文件在`./poc`目录下

- 创建自定类继承`hyperion_types.POC`类，所有在`./modules`目录下继承`POC`的子类将被视为POC

- 根据需求重写`execute`、`filter`成员函数，具体含义如下

  `execute`: 该POC的主体执行内容

  `filter`: 判断当前目标是否符合执行该POC的条件

  ```python
  class Test(POC):
      # POC测试主体
      def execute(self):
          t = time.time()
          # 测试十次http访问
          for i in range(10):
              # 后五个测试http错误捕获
              if i >= 5:
                  # 使用模块要求的logger输出
                  self.logger.debug('Test', 'Test error')
                  url = '1' + self.target.url
              else:
                  # 正常访问测试
                  self.logger.debug('Test', 'Test normal request')
                  url = self.target.url
              res = yield requests(url, timeout=1)
              # 错误捕获
              if POC.is_error(res):
                  # 错误则输出错误
                  self.logger.error('Test', repr(res))
              else:
                  # 正常执行则输出
                  self.logger.information('Test', f"status: {res['status']}")
          self.logger.information('test', str(time.time() - t))
          self.logger.debug('Test', 'Test asyncio sleep')
          # 测试自定的协程
          for i in range(5):
              t = time.time()
              async_result = yield sleep_return_test()
              self.logger.information('Test', async_result + f' sleep {time.time() - t} s')
          self.logger.debug('Test', 'Test done')
          # 报错，直接触发模块的错误回调
          1 / 0
          yield
  
      @staticmethod
      def filter(target: Target):
          return True
```
  
  

### POC生命周期

1. POC类被POC装载器载入
2. 以目标初始化POC
3. POC被挂载至调度器，这是POC唯一的执行方式
4. POC执行结束
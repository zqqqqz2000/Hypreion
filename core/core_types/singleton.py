import threading


class Singleton:
    _instance_lock = threading.Lock()
    _instance = None
    _first_init_flag = True

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            with cls._instance_lock:
                if cls._instance is None:
                    cls._instance = super().__new__(cls)
        else:
            cls._first_init_flag = False
        return cls._instance

    @classmethod
    def stop_serve(cls):
        ...

    @classmethod
    def drop_instance(cls):
        """
        Stop service and drop singleton instance
        :return: None
        """
        if cls._instance is not None:
            cls.stop_serve()
            cls._instance = None

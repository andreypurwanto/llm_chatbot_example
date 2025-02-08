from threading import current_thread

class CurrentThread():
    def __init__(self):
        self.__current_thread_dict = current_thread().__dict__

    def set(self, key, value):
        self.__current_thread_dict[key] = value

    def get(self, key):
        if key in self.__current_thread_dict:
            return self.__current_thread_dict[key]
        return None

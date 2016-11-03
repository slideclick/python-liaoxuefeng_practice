# -*- coding: UTF-8 -*-
import inspect

class B(object):
    bNum=2
    def __init__(self,v):
        self.v=v
    pass

class metaB(type):
    def __call__(self, *args, **kwargs):
            print('{0}  {1} in '.format(self.__name__,inspect.stack()[0][3]),end='\r\n')
            obj = super().__call__(*args, **kwargs)
            print('{0}  {1} out'.format(self.__name__,inspect.stack()[0][3]),end='\r\n')
            return obj

    def __init__(self, *args, **kwargs):
            print('{0}  {1} in '.format(self.__name__,inspect.stack()[0][3]),end='\r\n')
            obj = super().__init__(*args, **kwargs)
            print('{0}  {1} out'.format(self.__name__,inspect.stack()[0][3]),end='\r\n')
            return obj            

class C(B,metaclass=metaB)    :
    pass

o=C();    
        
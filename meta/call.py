# -*- coding: UTF-8 -*-
import inspect
import collections
class B(object):
    bNum=2
    def __init__(self,v):
        self.v=v
    pass

class metaB(type):#注意你仅仅hook了C这个东东的创建过程，但是type的metaClass还是type.call而不是metaB.call
#所以你看不到C=type()这个call里面的template,你只能看到o=C()的()的过程
#A的call是给a()用的，metaB的call是给A()用的。而A=type()那个type()的()不是你能override的
    def __call__(self, *args, **kwargs):#o=C(3); 
            print('{0}  {1} in '.format(self.__name__,inspect.stack()[0][3]),end='\r\n')
            obj = super().__call__(*args, **kwargs)
            print('{0}  {1} out'.format(self.__name__,inspect.stack()[0][3]),end='\r\n')
            return obj
            
    @classmethod
    def __prepare__(metacls, name, bases, **kwds):
        return collections.OrderedDict()

    def __new__(cls, name, bases, namespace, **kwds):
        print('{0}  {1} in '.format(cls.__name__,inspect.stack()[0][3]),end='\r\n')
        result = super().__new__(cls, name, bases, namespace)
        result._order = tuple(n for n in namespace if not        n.startswith('__'))
        print('{0}  {1} out '.format(cls.__name__,inspect.stack()[0][3]),end='\r\n')
        return result
        
    def __init__(self, *args, **kwargs):
            print('{0}  {1} in '.format(self.__name__,inspect.stack()[0][3]),end='\r\n')
            obj = super().__init__(*args, **kwargs)
            print('{0}  {1} out'.format(self.__name__,inspect.stack()[0][3]),end='\r\n')
                       

class C(B,metaclass=metaB)    :
    cNum=5
  
    def __init__(self,v,d):
            print('{0}  {1} in '.format(self.__class__,inspect.stack()[0][3]),end='\r\n')
            super().__init__(v)#这里不能写self居然
            self.d=d
            print('{0}  {1} out'.format(self.__class__,inspect.stack()[0][3]),end='\r\n')
            
    pass

o=C(7,9);    
#发现一个小的陷阱，你空白写的py文件，如果不显式设置为utf-8在notepad++中，它会存为cp936你虽然可以看到中文，换个机器就不行了。        
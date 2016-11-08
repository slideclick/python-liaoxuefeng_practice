# -*- coding: UTF-8 -*-
import inspect
import collections


import collections.abc
class sth( collections.abc.Callable ):
    def __call__(self, *args, **kwargs):
        print('{0}  {1} in '.format(self.__class__,inspect.stack()[0][3]),end='\r\n')
        pass
    pass
#http://openhome.cc/Gossip/Python/Metaclass.html
#为什么  metafunc可以当元类使用，看了内部还是做了检查的，上面的sth不行  
#答：它要的是可以call的东东。sth不可以call，但是sth的对象可以call
def metafunc(definedclzname, supers, attrs):
     print(definedclzname, supers, attrs,sep=' ',end='\r\n\r\n\r\n')
     result = type(definedclzname, supers, attrs)
     #type()里面怎么做，不是你可以控制的
     result = type.__new__(type,definedclzname, supers, attrs)
     type.__init__(result,2)
     print(definedclzname, supers, attrs)
     return result
'''
class type(object):
    def __call__(self, *args, **kwargs):#这里self指向的是A这个东东（type的inst），参数是你传给init的东东
        # should do the same thing as type.__call__
        obj = self.__new__(self, *args, **kwargs)
        if isinstance(obj, self):
            obj.__init__(*args, **kwargs)
        return obj

'''

     
class metaB(type):#注意你仅仅hook了C这个东东的创建过程，但是type的metaClass还是type.call而不是metaB.call
#所以你看不到C=type()这个call里面的template,你只能看到o=C()的()的过程
#A的call是给a()用的，metaB的call是给A()用的。而A=type()那个type()的()不是你能override的
    def __call__(self, *args, **kwargs):#o=C(3); 
            print('{0}  {1} in '.format(self.__name__,inspect.stack()[0][3]),end='\r\n')
            obj = super().__call__(*args, **kwargs)# super会先检查参数的数量，不是随便调用new init等待它们抛异常
            #错了，不是先检查。也是等待它们跑异常，只是它抛出时，你看不到stack就好像是call抛出的
            print('{0}  {1} out'.format(self.__name__,inspect.stack()[0][3]),end='\r\n')
            return obj
    print('metaB Class was made',end='\r\n\r\n')        
    @classmethod
    def __prepare__(metacls, name, bases, **kwds):
        return collections.OrderedDict()

    def __new__(cls, name, bases, namespace, **kwds):
        print('{0}  {1} in '.format(name,inspect.stack()[0][3]),end='\r\n')
        result = super().__new__(cls, name, bases, namespace)
        result._order = tuple(n for n in namespace if not        n.startswith('__'))
        print('{0}  {1} out '.format(name,inspect.stack()[0][3]),end='\r\n\r\n')
        return result
        
    def __init__(self, *args, **kwargs):
            print('{0}  {1} in '.format(self.__name__,inspect.stack()[0][3]),end='\r\n')
            obj = super().__init__(*args, **kwargs)
            print('{0}  {1} out'.format(self.__name__,inspect.stack()[0][3]),end='\r\n\r\n')
                       
class B(object,metaclass=metafunc):#B=type() B=metaB() 至于type()里面怎么实现，不是你可以override的. metaB里面定义的__call是给b=B()用的
    bNum=2
    print('B Class was made',end='\r\n\r\n')
    def __new__(cls,v):    
        print('{0}  {1} in '.format('<'+cls.__name__+'>',inspect.stack()[0][3]),end='\r\n')
        result = super().__new__(cls)
        print('{0}  {1} out '.format('<'+cls.__name__+'>',inspect.stack()[0][3]),end='\r\n')
        return result    
    def __init__(self,v):
        print('{0}  {1} in '.format(self.__class__,inspect.stack()[0][3]),end='\r\n')
        self.v=v
        print('{0}  {1} out'.format(self.__class__,inspect.stack()[0][3]),end='\r\n\r\n')
class C(metaclass=metaB)    :
    cNum=5 
    print('C Class was made',end='\r\n\r\n')
    def __new__(cls,v,d):    
        print('{0}  {1} in '.format('<'+cls.__name__+'>',inspect.stack()[0][3]),end='\r\n')
        result = super().__new__(cls)
        result.unit = v
        print('{0}  {1} out '.format('<'+cls.__name__+'>',inspect.stack()[0][3]),end='\r\n')
        return result
        
    def __init__(self,v,d):
            print('{0}  {1} in '.format(self.__class__,inspect.stack()[0][3]),end='\r\n')
            super().__init__()#这里不能写self居然.这里如果参数不对，是运行时错误。
            self.d=v
            print('{0}  {1} out'.format(self.__class__,inspect.stack()[0][3]),end='\r\n')

o=C(7,9);   
b=B(1) 
#发现一个小的陷阱，你空白写的py文件，如果不显式设置为utf-8在notepad++中，它会存为cp936你虽然可以看到中文，换个机器就不行了。        
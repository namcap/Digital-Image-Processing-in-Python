class my_stack:

    def __init__(self,size=1,max_size=-1):
        self.__size=size if 0<size else 1
        self.__max_size=max_size
        self.__index=0
        self.__data=[None]*self.__size

    def __double_size(self):
        if 0<self.__max_size<2*self.__size:
            self.__data+=[None]*(self.__max_size-self.__size)
            self.__size=self.__max_size
        else:
            self.__data+=[None]*self.__size
            self.__size*=2

    def push(self,ele):
        if (self.__size-1<self.__index):
            self.__double_size()
        try:
            self.__data[self.__index]=ele #will throw an exception if __double_size() fails
        except:
            raise
        self.__index+=1

    def pop(self):
        if (0<self.__index):
            self.__index-=1
            return self.__data[self.__index]
        else:
            return None

    def is_empty(self):
        return self.__index==0

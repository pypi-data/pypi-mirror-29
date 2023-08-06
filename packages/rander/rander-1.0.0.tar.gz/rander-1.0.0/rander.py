import random
from functools import wraps
from time import time


def timer(func):
    @wraps(func)
    def wrap(*args, **kwargs):
        start = time()
        func(*args, **kwargs)
        end = time()
        print("['{model}' Called Time {time} ms]".format(
            model=func.__name__, time=int(round((end-start) * 1000))))
    return wrap


class rander(object):
    '''
        quantity    生成随机数的个数
        minval      生成随机数的最小值
        maxval      生成随机数的最大值
        typed       生成随机数的类型
            -'i'    整数
            -'f'    浮点数
            -'.1f'  一个小数位的浮点数
            -'.nf'  n个小数位的浮点数(最大9)

            -'b'    二进制
            -'d'    十进制
            -'o'    八进制
            -'h'    十六进制

            eg.
                typed='di'      十进制整数
                      '.2df'    十进制带两位小数位的浮点数
        repeat      数字是否可重复
    '''

    def __init__(self, quantity, minval, maxval, typed='di', repeat=False):
        self.quantity = quantity    # 随机数个数
        self.minval = minval        # 随机数最小值
        self.maxval = maxval        # 随机数最大值
        self.repeat = repeat        # 是否可重复

        self.typed = typed[-1]      # 数值类型 [-i int -f float]
        if self.typed in['i', 'f']:
            pass
        else:
            raise('参数错误')
        self.ary = typed[-2]        # 数值进制 [-d 十进制 -b 二进制 -o 八进制  -h 十六进制]
        if self.ary in ['b', 'd', 'o', 'h']:
            pass
        else:
            raise('参数错误')
        if self.typed is 'f' and self.ary in ['b', 'o', 'h']:
            raise('浮点数暂不支持转换为其他进制!')
        if self.typed != 'i':
            self.dig = typed[1:-2]
            if self.dig in ['{0}'.format(i) for i in range(1, 10)]:
                self.dig = int(self.dig)    # 小数位数 [区间范围  [1,9] 默认 0 ]
            else:
                raise('参数错误')
            if typed[-0] != '.':
                raise('参数错误')
        else:
            self.dig = 0

        if self.typed is 'i' and self.repeat is False:
            if self.maxval-self.minval < self.quantity:
                raise('序列长度不足!')
        self.randlist = []  # 随机数组

        # print(self.typed, self.ary, self.dig)
        self.__rander()

    @timer
    def __rander(self):
        while len(self.randlist) < self.quantity:
            if self.typed in ['i']:
                temp = random.randint(self.minval, self.maxval)
                if self.ary is 'b':
                    temp = bin(temp)
                elif self.ary is 'o':
                    temp = oct(temp)
                elif self.ary is 'h':
                    temp = hex(temp)
            elif self.typed in ['f']:
                temp = random.uniform(self.minval, self.maxval)
                temp = round(temp, self.dig)
            if self.repeat:
                self.randlist.append(temp)
            elif not self.repeat:
                if temp not in self.randlist:
                    self.randlist.append(temp)

    def __len__(self):
        return len(self.randlist)

    def __iter__(self):
        return iter(self.randlist)

    def __getitem__(self, index):
        return self.randlist[index]

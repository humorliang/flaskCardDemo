from functools import wraps


# 定义一个装饰器

def my_decorate(a, b):
    def my_chek(fun):
        def chek(*args, **kwargs):
            print('a', a)
            print('b', b)
            print('装饰器')
            return fun(*args, **kwargs)
        return chek
    return my_chek

@my_decorate('A','B')
def test(a):
    print(a)


test('asd')

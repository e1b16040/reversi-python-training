import time

def time_record(func):
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        elapsed_time = time.time() - start
        print('----------------')
        print("elapsed time: {}".format(elapsed_time))
        return result
    return wrapper


def func_info(func):
    def wrapper(*args, **kwargs):
        result = func(*args, **kwargs)
        print('----------------')
        print("function name: {}".format(func.__name__))
        print("args: {}, {}".format(args, kwargs))
        return result
    return wrapper

@time_record
@func_info
def main(a, b):
    print('aaaaa')
    print(a)
    print(b)


if __name__ == '__main__':
    main(111, 'BBB')
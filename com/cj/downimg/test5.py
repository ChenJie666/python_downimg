from multiprocessing import Process, Pool
import os
import time
import random
import threading


# 子进程任务
def download(f):
    print("threadPool:" + str(threading.currentThread()))

    print('__进程池中的进程——pid=%d,ppid=%d' % (os.getpid(), os.getppid()))
    for i in range(3):
        print(f, '--文件--%d' % i)
        time.sleep(random.randint(1, 9))
        # time.sleep(1)
    return {"result": 1, "info": '下载完成！'}


# 主进程调用回调函数
def alterUser(msg):
    print("callback:" + str(threading.currentThread()))

    print("----callback func --pid=%d" % os.getpid())
    print("get result:", msg["info"])


if __name__ == "__main__":
    print("Main:" + str(threading.currentThread()))

    p = Pool(3)
    p.apply_async(func=download, args=(1111,), callback=alterUser)
    p.apply_async(func=download, args=(2222,), callback=alterUser)
    p.apply_async(func=download, args=(3333,), callback=alterUser)
    # 当func执行完毕后，return的东西会给到回调函数callback
    print("---start----")
    p.close()  # 关闭进程池，关闭后，p不再接收新的请求。
    p.join()
    print("---end-----")
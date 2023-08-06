# 项目：标准库函数
# 模块：协程模块
# 作者：黄涛
# License:GPL
# Email:huangtao.sh@icloud.com
# 创建：2016-12-26 13:34

'''
对asyncio库进行进一步封装，主要功能如下：

1. 执行一个或并行运行多个协程：
    start(coro1,coro2,...)
2. 中断协程，并等待另一个协程的运行结果：
    result=await coro()
3. 在协程中，并发多个协程：
    await wait(*coros)
'''
import asyncio

__all__ = 'start', 'wait', 'wait_for', 'sleep', 'iscoroutine', 'batch', 'run'

wait = asyncio.wait
wait_for = asyncio.wait_for
sleep = asyncio.sleep
iscoroutine = asyncio.iscoroutine


def batch(coro, *datas):
    # 使用一个协程函数批量生成协程
    return wait(map(coro, *datas))


def start(*coros):
    # 执行协程，如coro为多个，则全部并发执行。
    try:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        coro = coros[0] if len(coros) == 1 else wait(coros)
        loop.run_until_complete(coro)
    finally:
        loop.close()


def run(*coros):
    loop = asyncio.get_event_loop()
    coro = coros[0] if len(coros) == 1 else wait(coros)
    loop.run_until_complete(coro)

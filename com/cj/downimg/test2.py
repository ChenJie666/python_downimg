from concurrent.futures import ThreadPoolExecutor
import time


def sleeper(secs):
    time.sleep(secs)
    print('I slept for {} seconds'.format(secs))
    return secs


with ThreadPoolExecutor(max_workers=3) as executor:
    times = [4, 1, 2]
    start_t = time.time()

    futs = [executor.submit(sleeper, secs) for secs in times]
    for fut in futs:
        print(fut.result())

    print(time.time() - start_t)

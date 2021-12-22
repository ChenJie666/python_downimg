from concurrent.futures import ThreadPoolExecutor, as_completed
import time
import threading
import tkinter


def sleeper(secs):
    print("threadPool:" + str(threading.currentThread()))
    time.sleep(secs)
    print('I slept for {} seconds'.format(secs))
    return secs


def call_back(arg):
    print("callback")


def sub_thread():
    with ThreadPoolExecutor(max_workers=3) as executor:
        print("Main:" + str(threading.currentThread()))
        times = [4, 1, 2]
        start_t = time.time()

        futs = [executor.submit(sleeper, secs) for secs in times]
        for fut in as_completed(futs):
            fut.add_done_callback(call_back)
            print(fut.result())

        print(time.time() - start_t)


if __name__ == "__main__":
    window = tkinter.Tk()
    window.geometry("500x300+500+500")
    window.title("test")


    def start():
        th = threading.Thread(target=sub_thread)
        th.start()
        # th.join()

    button = tkinter.Button(window, text="start", command=start)
    button.pack()

    tkinter.mainloop()

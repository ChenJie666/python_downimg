from misaka import Markdown, HtmlRenderer
from os import walk, path, mkdir, startfile
from uuid import uuid4
from bs4 import BeautifulSoup
from logging import basicConfig, getLogger
from time import strftime, localtime
from tkinter.filedialog import askdirectory
from tkinter.ttk import Progressbar
from PIL import Image
from PIL.ImageTk import PhotoImage
from concurrent.futures import ThreadPoolExecutor, as_completed
from tkinter import Tk, constants, Scrollbar, Canvas, BooleanVar, Checkbutton, Label, Button, Frame, messagebox
from threading import Thread
import sys


# from multiprocessing import cpu_count
# import traceback


def get_files_list():
    """
    获取一个目录下所有文件列表，包括子目录
    :return: files_list
    """
    files_list = []
    for root, dirs, files in walk(dir_path, topdown=True):
        for file in files:
            # 遍历所有以.md结尾的文件
            if file.endswith('md'):
                files_list.append(path.join(root, file))
    return files_list


def get_pics_list(args):
    """
    下载图片并替换地址
    :param args:
    :return:
    """
    md_content = args[0]
    file = args[1]

    logger.info(f'正在处理：{file}')

    # 下载并替换图片
    try:
        new_md_content = md_content
        md_render = Markdown(HtmlRenderer())
        html = md_render(md_content)
        soup = BeautifulSoup(html, features='html.parser')
        logger.debug(f"soup.find_all('img') : {soup.find_all('img')}")

        for index, img in enumerate(soup.find_all('img')):
            url = img['src']
            logger.debug(f'found_image_url: {url}')
            if url.startswith('http'):
                logger.debug(f'正在下载第 {index + 1} 张图片 {url}')
                url_location = download_pics(url, file)
                logger.debug(f'正在替换第 {index + 1} 张图片 {url_location}')
                new_md_content = new_md_content.replace(url, url_location)

        # 覆盖到原文件
        with open(file, 'w', encoding='utf-8') as n:
            n.buffer.write(new_md_content.encode())

    except Exception as exception:
        # traceback.print_exc()
        raise MyException(file, repr(exception))

    logger.info(f'处理完成：{file}')
    return file


def download_pics(url, file):
    """
    下载图片
    :param file:
    :param url, file
    :return:
    """
    from urllib.request import urlretrieve

    filename = path.basename(file)
    dirname = path.dirname(file)
    targer_dir = path.join(dirname, f"{filename[:filename.rindex('.')]}.assets")
    if not path.exists(targer_dir):
        mkdir(targer_dir)
    # 图片保存到本地
    pic_name = f'{uuid4().hex}.png'
    abs_location = path.join(targer_dir, pic_name)
    urlretrieve(url, abs_location)

    # TODO 这里需要根据操作系统可以识别的目录分隔符来选择，如typero可以识别"/"和"\"，但是obsidian只识别"/"，所以这里改为"/"
    rel_location = f"{filename[:filename.rindex('.')]}.assets/{pic_name}"
    # rel_location = f"{filename[:filename.rindex('.')]}.assets\\{pic_name}"
    return rel_location


def execute(files_label_dict):
    with open(dir_path + '/' + logfile_name, 'w', encoding='utf-8') as log:
        log.buffer.write(f'任务开始 -- {strftime("%Y-%m-%d %H:%M:%S", localtime())} \n'.encode())

    logger.debug(files_label_dict.keys())

    # 这里用的线程池，对于Python来说，只会使用一个CPU
    # cpu_num = cpu_count()
    # logger.info(f'cpu_num: {cpu_num}')
    with ThreadPoolExecutor(max_workers=16) as executor:
        # 用于存储异步任务
        tasks = []
        total_task_num = len(files_label_dict)
        complete_task_num = 0

        # 任务放到线程池中
        for file, label in files_label_dict.items():
            # 改变正在执行任务的图标
            label["image"] = img_downloading
            # 获取文件内容
            with open(file, encoding='utf-8') as f:
                md_content = f.read()

            args = [md_content, file]
            task = executor.submit(get_pics_list, args)
            tasks.append(task)

        # 返回任务执行结果
        for task in as_completed(tasks):
            try:
                success_file = task.result()
                with open(dir_path + '/' + logfile_name, 'a', encoding='utf-8') as log:
                    log.buffer.write(f'Success: 处理完成 [{success_file}] \n'.encode())

                # 改变已完成任务的图标和进度条
                label = files_label_dict[success_file]
                label["image"] = img_success
                complete_task_num += 1
                progress["text"] = str(round(100 * complete_task_num / total_task_num)) + "%"
                progressbar["value"] = 100 * complete_task_num / total_task_num
            except MyException as ex:
                fail_file = ex.fail_file
                msg = ex.msg
                logger.error(f"Error: {ex}")
                with open(dir_path + '/' + logfile_name, 'a', encoding='utf-8') as log:
                    log.buffer.write(f'Error: 处理失败 [{fail_file}] , 错误信息 {msg} \n'.encode())
                # 改变已失败任务的图标和进度条
                label = files_label_dict[fail_file]
                label["image"] = img_failure
                complete_task_num += 1
                progress["text"] = str(round(100 * complete_task_num / total_task_num)) + "%"
                progressbar["value"] = complete_task_num / total_task_num

                # try:
                #     removedirs(f"{fail_file[:fail_file.rindex('.')]}.assets")
                #     logger.info(f"{fail_file[:fail_file.rindex('.')]}.assets")
                # except Exception:
                #     pass

            # exception = task.exception()
            # if task.exception():
            #     logger.error(f"Error: 下载文件 [{file}] 的图片失败, 错误信息 {exception}")
            #     with open(dir_path + '/' + logfile_name, 'w', encoding='utf-8') as log:
            #         log.buffer.write(f'Error: 下载文件 [{file}] 的图片失败, 错误信息 {exception}'.encode())
            #
            #     try:
            #         removedirs(f'{file}.assets')
            #     except Exception:
            #         pass
            # else:
            #     logger.info(f'{file} 处理完成。')

    logger.info("=" * 15 + " 任 务 完 成 " + "=" * 15)
    with open(dir_path + '/' + logfile_name, 'a', encoding='utf-8') as log:
        log.buffer.write(f'任务完成 -- {strftime("%Y-%m-%d %H:%M:%S", localtime())} \n'.encode())

    # 修改开始按钮为查看日志
    def open_log():
        startfile(dir_path + '/' + logfile_name)

    button_start["text"] = "查看日志"
    button_start["command"] = open_log
    button_start["state"] = constants.NORMAL


def start_gui():
    # 定义字典用于存储每个文件的选中状态
    file_dict = {}

    def all_chk():
        for value in file_dict.values():
            value.set(constants.TRUE)

    def non_chk():
        for value in file_dict.values():
            value.set(constants.FALSE)

    def inv_chk():
        for value in file_dict.values():
            value.set(1 - value.get())

    def select_dir():
        # 清空存储文件的字典
        file_dict.clear()
        # 清空先前的frame
        for widget in frame.winfo_children():
            widget.destroy()
        # 清空grid布局结构
        frame.grid_forget()
        # 隐藏进度条
        global progress
        global progressbar
        progress.pack_forget()
        progressbar.pack_forget()
        # 开始按钮
        button_start["text"] = "开始下载"
        button_start["command"] = start_job
        button_start["state"] = constants.NORMAL

        all_chk_btn = Button(frame, text="全选", width='10', font=("SimSun", 8), command=all_chk, bg='#D2CDCD')
        all_chk_btn.grid(row=0, column=0, sticky=constants.W, padx="2")
        non_chk_btn = Button(frame, text="全不选", width='10', font=("SimSun", 8), command=non_chk, bg='#D2CDCD')
        non_chk_btn.grid(row=0, column=1, sticky=constants.W, padx="2")
        inv_btn = Button(frame, text="反选", width='10', font=("SimSun", 8), command=inv_chk, bg='#D2CDCD')
        inv_btn.grid(row=0, column=2, sticky=constants.W, padx="2")

        global dir_path
        dir_path = askdirectory(initialdir=path.abspath('.'))
        # dir_path = askdirectory(initialdir=os.path.realpath(sys.argv[0]))
        # dir_path = askdirectory(initialdir=path.dirname(__file__))

        for index, file in enumerate(get_files_list()):
            # 复选框
            file_dict[file] = BooleanVar(frame)
            file_dict[file].set(constants.TRUE)
            chk = Checkbutton(frame, text=file[len(dir_path) + 1:], var=file_dict[file], bg="white")
            chk.grid(row=index + 2, column=0, columnspan=10, sticky=constants.W, padx=(10, 10))
            # 用于填充白色
            Label(frame, bg="white").grid(row=index + 2, column=10, sticky=constants.EW, ipadx=win_width)

    def start_job():
        button_descri.pack_forget()
        files_list = []
        for (key, value) in file_dict.items():
            if value.get():
                files_list.append(key)
        # print(files_list)
        # 任务开始界面
        exec_gui(files_list)

    # 开始新任务后
    # 添加选择文件夹按钮
    button_select = Button(window, text="选择文件夹", command=select_dir, width=15)
    button_select.pack(side=constants.LEFT, fill=constants.Y, pady=20, padx=15)
    # 修改按键功能为开始任务
    global button_start
    button_start["command"] = start_job
    button_start.pack(side=constants.RIGHT, fill=constants.Y, pady=20, padx=15)

    # 添加功能说明
    def function_describe():
        global description
        messagebox.showinfo("功能描述", description)

    button_descri = Button(window, text="功能描述", width=15, command=function_describe)
    button_descri.pack(fill=constants.Y, pady=20, padx=15)


def exec_gui(files_list):
    # 清空先前的frame
    for widget in frame.winfo_children():
        widget.destroy()
    # 清空grid布局结构
    frame.grid_forget()

    print(files_list)
    # 新建字典，存储文件名和label
    files_label_dict = {}

    for index, file in enumerate(files_list):
        label = Label(frame, image=img_waiting, text=file[len(dir_path) + 1:], compound=constants.LEFT,
                      bg="white")
        label.grid(column=1, row=index + 1, sticky=constants.W)
        files_label_dict[file] = label
        # 用于填充白色
        Label(frame, bg="white").grid(row=index + 2, column=10, sticky=constants.EW, ipadx=win_width)

    # 按钮改为正在运行中
    button_start["text"] = "运行中..."
    button_start["state"] = constants.DISABLED
    # 进度条
    global progressbar
    global progress
    progressbar["value"] = 0
    progressbar.pack(side=constants.BOTTOM, fill=constants.X, pady=(0, 12))
    progress["text"] = "0%"
    progress.pack(side=constants.TOP, pady=(12, 0))

    th = Thread(target=execute, args=(files_label_dict,))
    th.setDaemon(True)
    th.start()

    # execute(files_label_dict)


class MyException(Exception):
    def __init__(self, file, msg):
        self.fail_file = file
        self.msg = msg


if __name__ == '__main__':
    basicConfig(level="INFO")
    logger = getLogger()

    # 引入图片
    bundle_dir = getattr(sys, '_MEIPASS', path.abspath(path.dirname(__file__)))
    path_to_icon = path.join(bundle_dir, 'icon')


    window = Tk()
    window.title(
        "md格式文章网络图片下载                                                                                      Authored By: CJ")
    win_width = 600
    win_height = 350
    window.geometry(f"{win_width}x{win_height}+600+300")
    window.iconbitmap(path_to_icon + '/lighting64.ico')

    # 创建Frame
    item_frame = Frame(window, relief=constants.GROOVE, bd=1)
    item_frame.pack(side=constants.TOP, fill=constants.BOTH, expand=constants.TRUE)

    # 在Frame中创建画布
    canvas = Canvas(item_frame)
    canvas.pack(side=constants.LEFT, fill=constants.BOTH, expand=constants.TRUE)
    # 在Canvas中创建新的Frame
    frame = Frame(canvas, bg="white")
    frame.pack(side=constants.LEFT, fill=constants.BOTH, expand=constants.TRUE)
    # 窗口展示的是frame的左上角
    canvas.create_window(0, 0, window=frame, anchor=constants.NW)

    # 为最外层的Frame创建滚动条，用于滚动画布中的元素
    scrollV = Scrollbar(item_frame, orient=constants.VERTICAL, command=canvas.yview)
    scrollV.pack(side=constants.RIGHT, fill=constants.Y)


    def scroll_bar(event):
        canvas.configure(yscrollcommand=scrollV.set, scrollregion=canvas.bbox("all"))


    def process_wheel(event):
        canvas.yview_scroll(-1 * (round(event.delta / 60)), "units")


    # 绑定滚动条
    frame.bind("<Configure>", scroll_bar)
    # 绑定滚轮事件
    frame.bind("<MouseWheel>", process_wheel)

    # 添加进度条
    progress = Label(window, text="0%", font=("Arial Bold", 10))
    progressbar = Progressbar(window, length=200, mode="determinate", maximum=100, name="完成进度",
                              orient=constants.HORIZONTAL, value=0, variable=0)
    # 添加图片
    img_waiting = PhotoImage(Image.open(path_to_icon + "/waiting.png").resize((16, 16)))
    img_downloading = PhotoImage(Image.open(path_to_icon + "/downloading.png").resize((16, 16)))
    img_success = PhotoImage(Image.open(path_to_icon + "/success.png").resize((16, 16)))
    img_failure = PhotoImage(Image.open(path_to_icon + "/failure.png").resize((16, 16)))

    # 定义全局变量
    logfile_name = "down_img.log"
    description = "选择文件夹后会递归遍历文件夹下的所有.md结尾的文件;\n点击开始下载后会下载文件中的网络图片，并替换文件中的图片地址;\n会直接操作文件内容，建议先对文件进行备份!"
    dir_path = ''
    button_start = Button(window, text="开始下载", width=15, state=constants.NORMAL)
    # 初始界面
    start_gui()

    window.mainloop()

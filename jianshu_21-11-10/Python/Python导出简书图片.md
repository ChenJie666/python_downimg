# 一、说明
简书前几天莫名其妙的宕机让我有些后怕，数据备份提上日程。

简书虽然有导出文章的功能，但是文章中的图片还是放在简书自己的图床中，需要自己下载图片并替换掉文章中的图片地址。如果文章和图片数量少，人肉操作还可以接受；一旦数量巨大，那么费时费力还容易出错。

所以网上找了些文章，写了一个小程序并打包成了exe工具，实现这个功能。
需要先从简书下载打包的文章，解压后在目录中启动程序，就会自动下载图片并替换图片地址。


<br>
# 二、程序
安装module
```
pip install misaka==2.1.1
pip install bs4
```
misaka模块安装时需要依赖Microsoft Visual环境，可以去官网下载或找帖子解决。
如果是python2.x，还需要安装concurrent模块。

代码如下
```
from misaka import Markdown, HtmlRenderer
from os import walk, path, mkdir, removedirs
from uuid import uuid4
from bs4 import BeautifulSoup
from concurrent.futures import ThreadPoolExecutor, as_completed
from multiprocessing import cpu_count
from logging import basicConfig, getLogger
import time
import traceback


def get_files_list(dir):
    """
    获取一个目录下所有文件列表，包括子目录
    :param dir
    :return: files_list
    """
    files_list = []
    for root, dirs, files in walk(dir, topdown=True):
        for file in files:
            # 遍历所有以.md结尾的文件
            if file.endswith('md'):
                files_list.append(path.join(root, file))
    return files_list


def get_pics_list(args):
    """
    下载图片并替换地址
    :param md_content, file
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
        traceback.print_exc()
        raise MyException(file, str(exception))

    logger.info(f'处理完成：{file}')
    return file


def download_pics(url, file):
    """
    下载图片
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

    rel_location = f"{filename[:filename.rindex('.')]}.assets\\{pic_name}"
    return rel_location


class MyException(Exception):
    def __init__(self, file, msg):
        self.fail_file = file
        self.msg = msg


if __name__ == '__main__':
    basicConfig(level="INFO")
    logger = getLogger()

    with open('./downimg.log', 'w', encoding='utf-8') as log:
        log.buffer.write(f'任务开始 -- {time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())} \n'.encode())

    files_list = get_files_list(path.abspath("."))
    logger.debug(files_list)

    cpu_num = cpu_count()
    logger.debug(f'cpu_num: {cpu_num}')
    with ThreadPoolExecutor(cpu_num) as executor:
        tasks = []

        # 任务放到线程池中
        for file in files_list:
            # 获取文件内容
            with open(file, encoding='utf-8') as f:
                md_content = f.read()

            args = [md_content, file]
            task = executor.submit(get_pics_list, args)
            tasks.append(task)

        # 收集异常信息
        for task in as_completed(tasks):
            try:
                success_file = task.result()
                with open('./downimg.log', 'a', encoding='utf-8') as log:
                    log.buffer.write(f'Success: 处理完成 [{success_file}] \n'.encode())
            except MyException as ex:
                fail_file = ex.fail_file
                msg = ex.msg
                logger.error(f"Error: {ex}")
                with open('./downimg.log', 'a', encoding='utf-8') as log:
                    log.buffer.write(f'Error: 处理失败 [{fail_file}] , 错误信息 {msg} \n'.encode())
                try:
                    removedirs(f"{fail_file[:fail_file.rindex('.')]}.assets")
                    logger.info(f"{fail_file[:fail_file.rindex('.')]}.assets")
                except Exception:
                    pass

            # exception = task.exception()
            # if task.exception():
            #     logger.error(f"Error: 下载文件 [{file}] 的图片失败, 错误信息 {exception}")
            #     with open('./downimg.log', 'w', encoding='utf-8') as log:
            #         log.buffer.write(f'Error: 下载文件 [{file}] 的图片失败, 错误信息 {exception}'.encode())
            #
            #     try:
            #         removedirs(f'{file}.assets')
            #     except Exception:
            #         pass
            # else:
            #     logger.info(f'{file} 处理完成。')

    logger.info("=" * 15 + " 任 务 完 成 " + "=" * 15)
    with open('./downimg.log', 'a', encoding='utf-8') as log:
        log.buffer.write(f'任务完成 -- {time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())} \n'.encode())
```
>使用线程池进行并发处理，使用tkinter显示进度条。

<br>
# 三、打包exe文件
安装pyinstaller模块
```
pip install pyinstaller -i https://pypi.tuna.tsinghua.edu.cn/simple --trusted-host pypi.tuna.tsinghua.edu.cn
```
执行打包程序
```
pyinstaller -F -w -i .\downimg.ico --hidden-import=_cffi_backend .\downimg.py
```

**参数说明：**
1. -i 给应用程序添加图标
2. -F 指定打包后只生成一个exe格式的文件
3. -D –onedir 创建一个目录，包含exe文件，但会依赖很多文件（默认选项）
4. -c –console, –nowindowed 使用控制台，无界面(默认)
5. -w –windowed, –noconsole 使用窗口，无控制台
6. -p 添加搜索路径

**注意点：**
1. 如果启动exe文件报错No module named '_cffi_backend'，需要在打包时添加--hidden-import=_cffi_backend参数；
2. 尽量避免import整个库，如果打出的包很大，运行时可以试试带参数--exclude pandas --exclude numpy。

<br>
# 四、小工具
打包完成后获取到的exe执行文件，运行后会扫描当前目录和子目录的所有.md格式的文件，下载文件中的网络图片到本地，并替换图片地址为本地地址。

**下载地址(服务器带宽小，网速很慢)：**https://chenjie.asia/downimg.exe

**注意点：**
1. 一定要备份原数据后再使用，一定要备份原数据后再使用，一定要备份原数据后再使用，完成后再检查一下是否有错误。工具只经过简单的测试，可能会出现bug。
2. 将工具放到目录下启动，就会扫描本目录和子目录的md文件，并下载图片和替换地址。
3. 运行中可能因为网络或链接问题导致任务异常，日志信息会输出到工具所在的目录的downimg.log文件中，推荐使用notepad等工具打开。如果有错误信息，则可以看到是哪个文件出了问题，将工具放到文件所在目录下再次启动或直接自己手动下载。
4. 如果文章中有html代码，且代码中有img标签和src属性，那么这篇文章可能会失败。可能是bs解析时出现的bug。
5. 如果有问题或者建议，可以给我评论。


<br>
参考文章：https://github.com/Deali-Axy/Markdown-Image-Parser

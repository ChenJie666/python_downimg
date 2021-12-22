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

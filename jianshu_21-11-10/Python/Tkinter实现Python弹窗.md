# 一、简介
Tkinter包编写一些图形用户界面程序。Tkinter是Python的一个标准包，因此我们并不需要安装它。我们将从创建一个窗口开始，然后我们在其之上加入一些小组件，比如按钮，复选框等，并使用它们的一些属性。

# 二、基本功能使用(Python3.x)
## 2.1 基础弹窗
```
import tkinter

window = tkinter.Tk()
window.title("Hello world")
# 进入消息循环
window.mainloop()
```

<br>
## 2.2 带有文本信息的弹窗
```
window = tkinter.Tk()
window.title("Hello World")
lbl = tkinter.Label(window, text="content")
lbl.grid(column=0, row=0)
window.mainloop()
```
设置文本大小
```
lbl = tkinter.Label(window, text="content", font=("Arial Bold", 100))
```
设置窗口大小
```
window.geometry("500x200")
```

<br>
## 2.3 添加一个按钮组件
```
import tkinter

window = tkinter.Tk()
window.title("Hello World")
lbl = tkinter.Label(window, text="content", font=("Arial Bold", 100))
window.geometry("600x200")
lbl.grid(column=0, row=0)

btn = tkinter.Button(window, text="Click Me")
# column和row 决定了每个组件的相对位置
btn.grid(column=0, row=1)

window.mainloop()
```
更改按钮前景和背景颜色
```
btn = tkinter.Button(window, text="Click Me", font=("Arial Bold", 10), bg="green", fg="orange")
```
处理按钮点击事件
```
def clicked():
    lbl.configure(text="Button was clicked!")

# 绑定点击函数，点击后修改lbl中的text内容
btn = tkinter.Button(window, text="Click Me", command=clicked)
btn.grid(column=0, row=1)
```

<br>
## 2.4 添加一个文本框
```
import tkinter

window = tkinter.Tk()
window.title("Hello World")
window.geometry("600x200")
lbl = tkinter.Label(window, text="content")
lbl.grid(column=0, row=0)

# 接受输入的文本内容
txt = tkinter.Entry(width=10) # 设置输入文本框的宽度
txt.grid(column=1, row=0)

# 点击事件为修改文本内容为输入文本框的内容
def clicked():
    lbl.configure(text=txt.get())

btn = tkinter.Button(window, text="Click Me", command=clicked)
btn.grid(column=2, row=0)

window.mainloop()
```
设置输入焦点，当我们运行代码后，会发现可以直接在文本框中输入信息而不需要点击文本框。
```
txt.focus()
```

<br>
## 2.5 添加一个组合框

![image.png](https://upload-images.jianshu.io/upload_images/21580557-d8b1cb9297f71bb9.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

```
import tkinter.ttk

window = tkinter.Tk()
window.title("Hello World")
window.geometry("600x200")

combo = tkinter.ttk.Combobox(window)
combo['values'] = (1, 2, 3, 4, 5, "Text")
combo.current(2) # 下标为2的文本为默认选择
combo.grid(column=0, row=0)

window.mainloop()
```
我们可以通过get函数获取到被选中的选项。
如下，通过点击按钮将文本修改为选择框中的内容
```
import tkinter.ttk

window = tkinter.Tk()
window.title("Hello World")
window.geometry("600x200")

lbl = tkinter.Label(window, text="content")
lbl.grid(column=0, row=0)

combo = tkinter.ttk.Combobox(window)
combo['values'] = (1, 2, 3, 4, 5, "Text")
combo.current(2)
combo.grid(column=1, row=0)


def clicked():
    lbl.configure(text=combo.get())


btn = tkinter.Button(window, text='Click me', command=clicked)
btn.grid(column=2, row=0)

window.mainloop()
```

例：显示选择的选择的值
```
import tkinter

window = tkinter.Tk()
window.title("Hello World")
window.geometry("600x200")

lbl = tkinter.Label(window)
lbl.grid(column=0, row=1)

def clicked():
    lbl.configure(text=selected.get())

selected = tkinter.IntVar()
# 单选框中的第一个选项绑定一个方法，点击该选项时触发方法
rad1 = tkinter.Radiobutton(window, text="First", value=0, command=clicked, variable=selected)
rad2 = tkinter.Radiobutton(window, text="Second", value=1, command=clicked, variable=selected)
rad3 = tkinter.Radiobutton(window, text="Third", value=2, command=clicked, variable=selected)
rad1.grid(column=0, row=0)
rad2.grid(column=1, row=0)
rad3.grid(column=2, row=0)

window.mainloop()
```

<br>
## 2.6 添加复选框

![image.png](https://upload-images.jianshu.io/upload_images/21580557-eeeb37bf2e18b5b6.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

```
import tkinter

window = tkinter.Tk()
window.title("Hello World")
window.geometry("600x200")

chk_state = tkinter.BooleanVar()
chk_state.set(True)
chk = tkinter.Checkbutton(window, text="Choose", var=chk_state)
chk.grid(column=1, row=0)

window.mainloop()
```
也可以使用IntVar变量进行设置，结果和用BooleanVar一样。
```
import tkinter

window = tkinter.Tk()
window.title("Hello World")
window.geometry("600x200")

chk_state = tkinter.IntVar()
chk_state.set(1) # Check
# chk_state.set(0) # Uncheck
chk = tkinter.Checkbutton(window, text="Choose", var=chk_state)
chk.grid(column=1, row=0)

window.mainloop()
```

<br>
## 2.7 添加单选框

![image.png](https://upload-images.jianshu.io/upload_images/21580557-3d6ca13aacb82a9a.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

```
import tkinter

window = tkinter.Tk()
window.title("Hello World")
window.geometry("600x200")

rad1 = tkinter.Radiobutton(window, text="First", value=0)
rad2 = tkinter.Radiobutton(window, text="Second", value=1)
rad3 = tkinter.Radiobutton(window, text="Third", value=2)
rad1.grid(column=0, row=0)
rad2.grid(column=1, row=0)
rad3.grid(column=2, row=0)

window.mainloop()
```
给这些单选框设置command参数指定一个函数，点击它时就会运行该函数
```
rad1 = tkinter.Radiobutton(window, text="First", value=0, command=clicked, variable=selected)
```
获取单选框值
```
selected = tkinter.IntVar()
rad1 = tkinter.Radiobutton(window, text="First", value=0, command=clicked, variable=selected)
rad2 = tkinter.Radiobutton(window, text="Second", value=1, variable=selected)
rad3 = tkinter.Radiobutton(window, text="Third", value=2, variable=selected)
# 获取选择的值
text = selected.get()
```

<br>
## 2.8 添加文本区

![image.png](https://upload-images.jianshu.io/upload_images/21580557-1fc8553fe16593ab.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

```
import tkinter
from tkinter import scrolledtext

window = tkinter.Tk()
window.title("Hello world")
window.geometry("350x200")

txt = tkinter.scrolledtext.ScrolledText(window, width=40, height=10)
txt.grid(column=0, row=0)

window.mainloop()
```
用以下方法可以在文本区中插入文本：
```
txt.insert(tkinter.INSERT, "TEXT GOES HERE")
txt.insert(tkinter.INSERT, "\nNext Line")
```
用以下方法可以将文本区中的文本删除：
```
# 表示删除第一行及其之后的内容
txt.delete(1.0, END)
```

<br>
## 2.9 创建消息框

![image.png](https://upload-images.jianshu.io/upload_images/21580557-023a7bb94cacd8ab.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

```
import tkinter
import tkinter.messagebox

window = tkinter.Tk()
window.title("Hello world")
window.geometry("350x100")

def clicked():
    tkinter.messagebox.showinfo("Messge title", "Operation down")

btn = tkinter.Button(window, text="Click here", command=clicked)
btn.grid(column=0, row=0)

window.mainloop()
```

<br>
## 2.10 添加Spinbox
Spinbox是输入控件；与Entry类似，但是可以指定输入范围值。

![image.png](https://upload-images.jianshu.io/upload_images/21580557-c837a20c2b1e9a5d.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

```
import tkinter

window = tkinter.Tk()
window.title("Hello world")
window.geometry("350x150")

spin = tkinter.Spinbox(window, from_=0, to=100, width=5)
spin.grid(column=0, row=0)

window.mainloop()
```

如上代码指定了值的可变范围为0到100，也可以指定某些特定的值
```
tkinter.Spinbox(window, values=(3,8,11), width=5)
```
这样，Spinbox控件就只会显示3个数字即3，8，11。

给Spinbox控件设置默认值
```
var = tkinter.IntVar()
var.set(88)
spin = tkinter.Spinbox(window, from_=0, to=100, width=5, textvariable=var)
spin.grid(column=0, row=0)
```


<br>
## 2.11 添加进度条

![image.png](https://upload-images.jianshu.io/upload_images/21580557-712f2eeb7f86df23.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

```
from tkinter.ttk import Progressbar
import tkinter

window = tkinter.Tk()
window.title("Hello world")
window.geometry("350x200")

style = tkinter.ttk.Style()
style.theme_use('default')
style.configure("black.Horizontal.TProgressbar", background="black")
bar = Progressbar(window, length=200, style="black.Horizontal.TProgressbar")
bar['value'] = 70
bar.grid(column=0, row=0)

window.mainloop()
```

<br>
## 2.12 添加文件对话框

![image.png](https://upload-images.jianshu.io/upload_images/21580557-2b03bfb985e45930.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

选择单个文件
```
import tkinter
from tkinter import filedialog
import os

window = tkinter.Tk()
window.title("Hello world")
window.geometry("350x200")


def clicked():
    file = filedialog.askopenfilename(initialdir=os.path.dirname(__file__)) # 默认打开当前程序所在目录
    print(file)


button = tkinter.Button(window, text="添加文件", command=clicked)
button.grid(column=0, row=0)

window.mainloop()
```

选择多个文件
```
file = filedialog.askopenfilename(initialdir=os.path.dirname(__file__))
```

选择一个目录
```
file = filedialog.askdirectory(initialdir=os.path.dirname(__file__))
```

<br>
# 三、进度条进阶使用
## 3.1 设计进度条
Progressbar(父对象, options, ...)

- 第一个参数：父对象，表示这个进度条将建立在哪一个窗口内
- 第二个参数：options，参数如下

| 参数 | 含义 |
| --- | --- |
| length | 进度条的长度，默认是100像素 |
| mode | 可以有两种模式，下面作介绍 |
| maximum | 进度条的最大值，默认是100像素 |
| name | 进度条的名称，供程序参考引用 |
| orient | 进度条的方向，可以是HORIZONTAL(默认) 或者是VERTICAL |
| value | 进度条的目前值 |
| variable |	记录进度条目前的进度值 |

**mode参数:**
- determinate：一个指针会从起点移至终点，通常当我们知道所需工作时间时，可以使用此模式，这是默认模式

![image.png](https://upload-images.jianshu.io/upload_images/21580557-ca3e79a1a4c89177.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

- indeterminate：一个指针会在起点和终点间来回移动，通常当我们不知道工作所需时间时，可以使用此模式

![image.png](https://upload-images.jianshu.io/upload_images/21580557-9bd612cb49cc18e9.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

## 3.2 添加进度条动画
可以通过改变value的值并使用update方法刷新进度条的方式来使进度条动态改变。

```
import tkinter.ttk
import time

window = tkinter.Tk()
window.title("Hello world")
window.geometry("350x200")

progressbar = tkinter.ttk.Progressbar(window, length=200, mode="determinate", maximum=100, name="run bar", orient=tkinter.HORIZONTAL, value=0)

progressbar.pack(pady=20)


def run():
    for i in range(100):
        progressbar["value"] = i + 1
        window.update()
        time.sleep(0.03)


btn = tkinter.Button(window, text="run", command=run)
btn.pack(pady=5)

window.mainloop()
```

<br>
## 3.3 Progressbar 的方法 start()/step()/stop()
- start(interval)：每隔interval时间移动一次指针。interval的默认值是50ms，每次移动指针调用一次step(amount)。在step()方法内的amount参数意义就是增值量
- step(amount)：每次增加一次amount，默认值是1.0，在determinate模式下，指针不会超过maximum参数。在indeterminate模式下，当指针达到maximum参数值的前一格时，指针会回到起点
- stop()：停止start()运行

```
import tkinter.ttk

window = tkinter.Tk()
window.title("Hello world")
window.geometry("350x200")

progressbar = tkinter.ttk.Progressbar(window, length=200, mode="determinate", orient=tkinter.HORIZONTAL)
progressbar["maximum"] = 200
progressbar["value"] = 0
progressbar.pack(padx=5, pady=20)


def run():
    progressbar.start()
    progressbar.step(5)
    print(progressbar.cget("value"))


def stop():
    position = progressbar.cget("value")
    progressbar.stop()
    progressbar["value"] = position


btnr = tkinter.Button(window, text="Run", command=run)
btnr.pack(padx=10, pady=5, side=tkinter.LEFT)

btns = tkinter.Button(window, text="Stop", command=stop)
btns.pack(padx=10, pady=5, side=tkinter.RIGHT)

window.mainloop()
```

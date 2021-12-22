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
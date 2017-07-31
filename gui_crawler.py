# coding:utf-8
from Tkinter import *
from ScrolledText import ScrolledText

root = Tk()
root.title('ShouldChan_crawler')
root.geometry('+600+300')# 坐标，大小
text = ScrolledText(root, font=('微软雅黑', 10))  # 文本滚动条
text.grid()
button = Button(root, text='Start', font=('微软雅黑', 10))
button.grid()
varl = StringVar()
label = Label(root, font=('微软雅黑', 10), fg='blue',textvariable=varl)
label.grid()
varl.set('Ready...')
root.mainloop()

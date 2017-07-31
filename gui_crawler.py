# coding:utf-8
from Tkinter import *
from ScrolledText import ScrolledText

root = Tk()
root.title('ShouldChan_crawler')
text = ScrolledText(root, font=('微软雅黑', 10))# 文本滚动条
text.grid()
button = Button(root, text='Start', font=('微软雅黑', 10))
button.grid()
root.mainloop()

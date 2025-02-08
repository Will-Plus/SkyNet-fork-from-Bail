#Copyright Bail&Will&loaf0808 2025
#SkyNet:libgui 图形界面模块

from tkinter import *
from tkinter import messagebox as msgbox,ttk
from _tkinter import TclError
from abc import ABC
import libsc as sc,libfile,libclass,libstudy,logging

class Window(ABC):
    '''窗口基类'''
    def __init__(self,logger:libclass.Logger):
        self.logger = logger
    def showinfo(self,title:str,msg:str):
        '''显示提示信息
msg(str):提示信息的内容'''
        msgbox.showinfo(title,msg,parent=self)
    def showwarning(self,title:str,msg:str):
        '''显示警告信息
msg(str):警告信息的内容'''
        msgbox.showwarning(title,msg,parent=self)
    def showerror(self,title:str,msg:str):
        '''显示错误信息
msg(str):错误信息的内容'''
        msgbox.showerror(title,msg,parent=self)

class RootWindow(Tk,Window):
    def __init__(self,logger:libclass.Logger):
        Tk.__init__(self)
        Window.__init__(self,logger)
        self.title('SkyNet')
        self.geometry('800x600')
        try:
            self.iconphoto(False,PhotoImage(file=libfile.getpath('icon')))
        except TclError:
            self.logger.warning('未找到图标')

        self.lesson_choose_frame = Frame(self)
        self.lesson_choose_frame.pack(anchor=NW)
        Label(self.lesson_choose_frame,text='请选择课程').grid()
        Button(self.lesson_choose_frame,text='添加课程',command=libfile.add_lesson).grid(row=0,column=1)

        self.sccontrol_frame = Frame(RootWindow)
        self.sccontrol_frame.pack(anchor=NW)
        Button(self.sccontrol_frame,text='生词管理',command=lambda:sc.control(self)).grid(row=0,column=0)
        self.rem_need_review_label = Label(self.sccontrol_frame)
        self.rem_need_review_label.grid(row=0,column=1)
        self.wri_need_review_label = Label(self.sccontrol_frame)
        self.wri_need_review_label.grid(row=0,column=3)
        self.lessons_frame = Frame(RootWindow)
        self.lessons_frame.pack(anchor=NW)

        Label(self,text='特别感谢：Bail 对此项目的支持与帮助&对此项目的源代码的贡献！',fg='#7f7f7f').pack(side=BOTTOM,fill=X)

    def show_lessons(self, lessonlst: list[libclass.Lesson]):
        '''显示课程列表'''
        frame = self.lessons_frame
        for i, lesson in enumerate(lessonlst):
            Label(frame, text=lesson.name).grid(row=i, column=0)
            Button(frame, text=f'记忆 {lesson.progress[0]}/{len(lesson.words)}', 
                command=lambda arg=lesson: libstudy.remember(self, arg)).grid(row=i, column=1)
            Button(frame, text=f'默写 {lesson.progress[2]}/{len(lesson.words)}', 
                command=lambda arg=lesson: libstudy.write(self, arg)).grid(row=i, column=3)
            Button(frame, text='课程信息', command=lambda arg=lesson: lesson_info(self, arg)).grid(row=i, column=4)
class RememberWindow(Toplevel,Window):
    '''记忆模块界面'''
    def __init__(self,root:RootWindow,logger:libclass.Logger):
        Toplevel.__init__(self,root)
        Window.__init__(self,logger)
        self.title('记忆')

        #放置组件
        self.wordlab = Label(self);self.wordlab.pack()
        self.translab = Label(self);self.translab.pack()
        self.btnsframe = Frame(self);self.btnsframe.pack()
        self.huibtn = Button(self.btnsframe,text='会');self.huibtn.grid(row=0,column=0)
        self.buhuibtn = Button(self.btnsframe,text='不会');self.buhuibtn.grid(row=0,column=1)
        self.duibtn = Button(self.btnsframe,text='对',);self.duibtn.grid(row=1,column=0)
        self.buduibtn = Button(self.btnsframe,text='不对');self.buduibtn.grid(row=1,column=1)

        #默认隐藏按钮
        self.huibtn.grid_forget()
        self.buhuibtn.grid_forget()
        self.duibtn.grid_forget()
        self.buduibtn.grid_forget()
class WriteWindow(Toplevel,Window):
    '''默写模块界面'''
    def __init__(self,root:RootWindow,logger:libclass.Logger):
        Toplevel.__init__(self,root)
        Window.__init__(self,logger)
        self.title('默写')

        #放置组件
        self.translab = Label(self);self.translab.pack()
        entryframe = Frame(self);entryframe.pack()
        self.lenlab = Label(entryframe);self.lenlab.grid(row=0,column=0)
        self.entry = Entry(entryframe);self.entry.grid(row=0,column=1)
        self.judgelab = Label(entryframe);self.judgelab.grid(row=0,column=2)
        self.wordlab = Label(self);self.wordlab.pack()

def count_need_review(root:Tk):
    '''统计需要复习的单词数
root(tkinter.Tk):（包含三个Label属性的）根窗口'''
    remlab = root.rem_need_review_label
    wrilab = root.wri_need_review_label
    rem = sc.remlst
    wri = sc.wrilst

    for i in ('rem','wri'):
        if i == 'rem':
            sub = '记忆'
        elif i == 'wri':
            sub = '默写'

        need = sc.get_need_review_list(eval(i))
        needn = len(need)
        eval(i+'lab').config(text=f'{sub}需复习个数:{needn}')

class LessonInfoWindow(Toplevel,Window):
    '''课程信息（原为“单词本”）'''
    def __init__(self,root:RootWindow,logger:libclass.Logger):
        self.title('课程信息')

        #基本信息
        self.nameLabel = Label(self)
        self.nameLabel.pack(anchor=NW)
        self.fullNameLabel = Label(self)
        self.fullNameLabel.pack(anchor=NW)
        self.authorLabel = Label(self)
        self.authorLabel.pack(anchor=NW)
        #单词表
        self.tree = ttk.Treeview(self,columns=('词义'))
        self.tree.pack()
    
    def set_name(self,name:str):
        self.nameLabel.config(text=f'课程名称：{name}')
    def set_fullname(self,fullname:str):
        self.fullNameLabel.config(text=f'课程全称：{fullname}')
    def set_author(self,author:str):
        self.authorLabel.config(text=f'作者：{author}')
    def insert_words(self,wordlist:str):
        for i in wordlist:
            self.tree.insert('','end',text=i.word,values=(i.trans))

def show_notice(root:Tk,notice:str):
    msgbox.showinfo('公告',notice,parent=root)
def init(root:RootWindow,lessonlst:list):
    '''初始化界面
root(tkinter.Tk):根窗口
lessonlst(list):课程对象列表'''
    #初始化课程列表
    root.show_lessons(root,lessonlst)
    count_need_review(root)

#Copyright Bail&Will&loaf0808 2025
#SkyNet:libgui 图形界面模块

from tkinter import *
from tkinter import messagebox as msgbox,ttk
from _tkinter import TclError
from abc import ABC
from __future__ import annotations
import libunf,libfile,libclass,libstudy

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
        Button(self.sccontrol_frame,text='生词管理',command=lambda:libunf.control(self)).grid(row=0,column=0)
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
        self.logger = logger
        self.title('记忆')

        #放置组件
        self.wordlab = Label(self);self.wordlab.pack()
        self.translab = Label(self);self.translab.pack()
        self.btnsframe = Frame(self);self.btnsframe.pack()
        self.huibtn = Button(self.btnsframe,text='会')
        self.buhuibtn = Button(self.btnsframe,text='不会')
        self.duibtn = Button(self.btnsframe,text='对',)
        self.buduibtn = Button(self.btnsframe,text='不对')
    def show_word(self,word:libclass.Word):
        self.wordlab.config(text=word.word)
        self.translab.config(text='')
        for i in (self.duibtn,self.buduibtn):
            i.grid_forget()
        for i,j in enumerate((self.huibtn,self.buhuibtn)):
            j.grid(row=0,column=i)
    def check_right(self,word:libclass.Word):
        self.translab.config(text=word.trans)
        for i in (self.huibtn,self.buhuibtn):
            i.grid_forget()
        for i,j in enumerate((self.duibtn,self.buduibtn)):
            j.grid(row=1,column=i)
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
    def show_trans(self,word:libclass.Word):
        '''显示词义'''
        self.judgelab.config(text='')
        self.wordlab.config(text='')
        self.translab.config(text = word.trans)
        self.lenlab.config(text=f'{len(word.word)}){word.word[0]}')
        self.entry.config(state=NORMAL)
        self.entry.delete(0,END)
    def show_word(self,word:libclass.Word):
        '''显示单词'''
        self.entry.config(state=DISABLED)
        self.wordlab.config(text=word.word)
    def show_judge(self,judge_result:bool):
        '''显示判题结果'''
        sign = {True:'(v)',False:'(x)'}[judge_result]
        self.judgelab.config(text=sign)

class UnfWindow(Toplevel,Window):
    '''生词管理界面'''
    frames: list[UnfFrame]
    def __init__(self,root:RootWindow,logger:libclass.Logger):
        Toplevel.__init__(self,root)
        Window.__init__(self,logger)
        self.title('生词管理')
class UnfFrame(LabelFrame):
    '''生词模块界面中各学习模块的框架'''
    # 扩展出一个类来，是因为要自定义属性，不然IDE不认识自定义属性
    def __init__(self,title:str,unfWindow:UnfWindow):
        super().__init__(unfWindow,text=title)

        self.btnsFrame = Frame(self)
        self.reviewBtn = Button(self.btnsFrame,text='立即复习',command=lambda:review(self,'remember'))
        self.reviewBtn.grid()

        self.tree = ttk.Treeview(self,columns=('词义','学习次数','错误次数','记忆强度','复习时间'))
        self.tree.heading('词义',text='词义',command=lambda:treesort(self,'词义',False))
        self.tree.heading('学习次数',text='学习次数',command=lambda:treesort(self,'学习次数',False))
        self.tree.heading('错误次数',text='错误次数',command=lambda:treesort(self,'错误次数',False))
        self.tree.heading('记忆强度',text='记忆强度',command=lambda:treesort(self,'记忆强度',False))
        self.tree.heading('复习时间',text='复习时间',command=lambda:treesort(self,'复习时间',False))

        self.btnsFrame.pack()
        self.tree.pack()
    def intree(self,unflist:list[libunf.UnfamiliarWord]):
##    rem,lis,wri = remlst,lislst,wrilst
        for i in unflist:
            self.insert('','end',
                        text=i.word,	                    #单词
                        values=(i.trans,	                #词义
                                i.learn,i.wrong,	        #学习次数，错误次数
                                i.strenth(),	            #记忆强度
                                i.calculate_review_time()))	#复习时间

def unf_window_factory(root:RootWindow,moduleIds:tuple[str],logger:libclass.Logger)->UnfWindow:
    '''生词管理窗口工厂
moduleIds(tuple[str]):已有的学习模块id元组
--------------
学习模块id在libstudy'''
    window = UnfWindow(root,logger)
    frames:list[UnfFrame] = []
    for i in moduleIds:
        frame = UnfFrame(i,window)
        frame.pack()
        frames.append(frame)
    window.frames = frames
    return window

def count_need_review(root:Tk):
    '''统计需要复习的单词数
root(tkinter.Tk):（包含三个Label属性的）根窗口'''
    remlab = root.rem_need_review_label
    wrilab = root.wri_need_review_label
    rem = libunf.remlst
    wri = libunf.wrilst

    for i in ('rem','wri'):
        if i == 'rem':
            sub = '记忆'
        elif i == 'wri':
            sub = '默写'

        need = libunf.get_need_review_list(eval(i))
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

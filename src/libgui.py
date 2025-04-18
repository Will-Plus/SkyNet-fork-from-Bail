#Copyright Bail&Will&loaf0808 2025
#SkyNet:libgui 图形界面模块


from tkinter import *
from tkinter import messagebox as msgbox,ttk
from _tkinter import TclError
import libsc as sc,libfile,libclass,libstudy

#定义一个函数，用于在root窗口中显示课程列表
def inroot(root: Tk, lessonlst: list):
    frame = root.lessons_frame
    for i, lesson in enumerate(lessonlst):
        Label(frame, text=lesson.name).grid(row=i, column=0)
        Button(frame, text=f'记忆 {lesson.progress[0]}/{len(lesson.words)}', 
               command=lambda arg=lesson: libstudy.remember(root, arg)).grid(row=i, column=1)
        Button(frame, text=f'默写 {lesson.progress[2]}/{len(lesson.words)}', 
               command=lambda arg=lesson: libstudy.write(root, arg)).grid(row=i, column=3)
        Button(frame, text='课程信息', command=lambda arg=lesson: lesson_info(root, arg)).grid(row=i, column=4)

def root():
    root = Tk()
    root.title('SkyNet')
    root.geometry('800x600')
    try:
        root.iconphoto(False,PhotoImage(file=libfile.getpath('icon')))
    except TclError:
        print('W: 未找到图标')

    lesson_choose_frame = Frame(root)
    lesson_choose_frame.pack(anchor=NW)
    Label(lesson_choose_frame,text='请选择课程').grid()
    Button(lesson_choose_frame,text='添加课程',command=libfile.add_lesson).grid(row=0,column=1)
    root.lesson_choose_frame = lesson_choose_frame

    sccontrol_frame = Frame(root)
    sccontrol_frame.pack(anchor=NW)
    Button(sccontrol_frame,text='生词管理',command=lambda:sc.control(root)).grid(row=0,column=0)
    rem_need_review_label = Label(sccontrol_frame)
    rem_need_review_label.grid(row=0,column=1)
    wri_need_review_label = Label(sccontrol_frame)
    wri_need_review_label.grid(row=0,column=3)
    #将两个Label添加为root的属性，临时解决方案
    root.rem_need_review_label = rem_need_review_label
    root.wri_need_review_label = wri_need_review_label

    lessons_frame = Frame(root)
    lessons_frame.pack(anchor=NW)
    root.lessons_frame = lessons_frame  #把这个frame夹带出去，方便其他函数使用。后期将会把libgui用class重写，届时将不需要这样操作

    Label(root,text='特别感谢：Bail 对此项目的支持与帮助&对此项目的源代码的贡献！',fg='#7f7f7f').pack(side=BOTTOM,fill=X)
    return root
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
def remember(root:Tk):
    '''记忆模块界面
root(tkinter.Tk):根窗口
返回值：带有组件属性的记忆窗口(tkinter.Toplevel)'''
    #窗口初始化
    win = Toplevel(root)
    win.title('记忆')
    win.geometry('300x96')

    #放置组件
    win.wordlab = Label(win);win.wordlab.pack()
    win.translab = Label(win);win.translab.pack()
    win.btnsframe = Frame(win);win.btnsframe.pack()
    win.huibtn = Button(win.btnsframe,text='会');win.huibtn.grid(row=0,column=0)
    win.buhuibtn = Button(win.btnsframe,text='不会');win.buhuibtn.grid(row=0,column=1)
    win.duibtn = Button(win.btnsframe,text='对',);win.duibtn.grid(row=1,column=0)
    win.buduibtn = Button(win.btnsframe,text='不对');win.buduibtn.grid(row=1,column=1)

    #默认隐藏按钮
    win.huibtn.grid_forget()
    win.buhuibtn.grid_forget()
    win.duibtn.grid_forget()
    win.buduibtn.grid_forget()

    return win
def write(root:Tk)->list:
    '''默写模块界面
root(tkinter.Tk):根窗口
返回值:带有组件属性的默写窗口(tkinter.Toplevel)'''
    #窗口初始化
    win = Toplevel(root)
    win.title('默写')
    win.geometry('300x81')

    #放置组件
    win.translab = Label(win);win.translab.pack()
    entryframe = Frame(win);entryframe.pack()
    win.lenlab = Label(entryframe);win.lenlab.grid(row=0,column=0)
    win.entry = Entry(entryframe);win.entry.grid(row=0,column=1)
    win.judgelab = Label(entryframe);win.judgelab.grid(row=0,column=2)
    win.wordlab = Label(win);win.wordlab.pack()

    return win
    #现在问题:所有窗口(包括主窗口)都关闭后才会return
def lesson_info(root:Tk,lesson:libclass.Lesson):
    '''课程信息（原为“单词本”）
root(tkinter.Tk):根窗口
lesson(libclass.Lesson):课程'''
    book = Toplevel(root)
    book.title('课程信息')
    book.geometry('415x310')

    #基本信息
    Label(book,text=f'课程名称：{lesson.name}').pack(anchor=NW)
    Label(book,text=f'课程全称：{lesson.fullname}').pack(anchor=NW)
    Label(book,text=f'作者：{lesson.author}').pack(anchor=NW)

    #单词表
    tree = ttk.Treeview(book,columns=('词义'));tree.pack()
    for i in lesson.words:
        tree.insert('','end',text=i.word,values=(i.trans))

def show_notice(root:Tk,notice:str):
    msgbox.showinfo('公告',notice,parent=root)
def showinfo(msg:str,parent=None):
    '''显示提示信息
msg(str):提示信息的内容
parent(tkinter的窗口对象,包含Tk和Toplevel等):提示信息附属的窗口'''
    msgbox.showinfo('提示',msg,parent=parent)
def showwarning(msg:str,parent=None):
    '''显示警告信息
msg(str):警告信息的内容
parent(tkinter的窗口对象,包含Tk和Toplevel等):警告信息附属的窗口'''
    msgbox.showwarning('警告',msg,parent=parent)
    print(f'W: {msg}')
def showerror(msg:str,parent=None):
    '''显示错误信息
msg(str):错误信息的内容
parent(tkinter的窗口对象,包含Tk和Toplevel等):错误信息附属的窗口'''
    msgbox.showerror('错误',msg,parent=parent)
    print(f'E: {msg}')
def init(root:Tk,lessonlst:list):
    '''初始化界面
root(tkinter.Tk):根窗口
lessonlst(list):课程对象列表'''
    #初始化课程列表
    inroot(root,lessonlst)
    count_need_review(root)

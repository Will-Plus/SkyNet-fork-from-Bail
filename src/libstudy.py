#Copyright Bail&Will&loaf0808 2025
#SkyNet:libstudy 学习模块

from abc import ABC,abstractmethod
import libgui,libunf,libclass

class StudyModule(ABC):
    @abstractmethod
    def __call__(self)->tuple[list[libclass.Word],list[libclass.Word]]:
        '''进行课程的学习
返回值：生词和熟词各自的列表'''

class Remember(StudyModule):
    '''记忆模块'''
    def __init__(self,
            window:libgui.RememberWindow,   # 根窗口
            lesson:libclass.Lesson,         # 要学习的课程对象
            unfHandler:libunf.UnfamiliarWordHandler  # 生词处理器对象
        ):
        self.window = window
        self.lesson = lesson
        self.unfHandler = unfHandler
        self.unflist:list[libclass.Word] = []   # 生词列表
        self.famlist:list[libclass.Word] = []   # 熟词列表
    def hui4(): #会，进入看对错
        translab.config(text=current_word.trans)
        huibtn.grid_forget()
        buhuibtn.grid_forget()
        duibtn.grid(row=1,column=0)
        buduibtn.grid(row=1,column=1)
    def dui4(): #对，标为熟词并进入下一个单词
        nonlocal index
        huilst.append(current_word)
        index += 1
        nextword()
    def bu4():  #不会/不对，标为生词并进入下一个单词
        nonlocal index
        sclst.append(current_word)
        translab.config(text=current_word.trans)
        index += 1
        nextword()
    def nextword():
        nonlocal index  #防止下一行的判断出现bug
        if index == len(wlst):  #如果是最后一个单词
            libgui.showinfo(f'恭喜你学完({lesson.fullname})',parent=win)
            close()
        else:
            #隐藏按钮
            duibtn.grid_forget()
            buduibtn.grid_forget()
            translab.config(text='')

            #初始化变量
            nonlocal current_word   #index上面已经声明
            current_word = wlst[index]

            #显示
            win.title(f'记忆 {index+1}/{len(wlst)}')
            wordlab.config(text=current_word.word)
            huibtn.grid(row=0,column=0)
            buhuibtn.grid(row=0,column=1)
    def close():
        libsc.mark('remember',sclst,huilst)
        lesson.progress[0] = index
        win.destroy()
    def __call__(self):
        #初始化各种变量
        wlst = lesson.words #单词列表
        index = lesson.progress[0]  #当前学习的单词在单词列表中的索引
        sclst = []          #生词列表
        huilst = []         #熟词列表
        current_word:libclass.Word = None   #当前学习的单词

        #初始化界面
        win = self.window
        win.protocol('WM_DELETE_WINDOW',close)
        wordlab,translab,huibtn,buhuibtn,duibtn,buduibtn = win.wordlab,win.translab,win.huibtn,win.buhuibtn,win.duibtn,win.buduibtn
        huibtn.config(command=hui4)
        buhuibtn.config(command=bu4)
        duibtn.config(command=dui4)
        buduibtn.config(command=bu4)
        #recitebtn的command在recite函数里指定

        #显示第一个单词
        nextword()
def write(root:libgui.Tk,lesson:libclass.Lesson):
    '''默写模块
root(tkinter.Tk):根窗口
wlst(list):包含要学习的单词对象的列表'''
    def enter():
        nonlocal current_word,status,index,sclst

        if status == None:  #未判：判，并加入生词熟词列表
            entry.config(state=libgui.DISABLED)
            wordlab.config(text=current_word.word)
            myinput = entry.get()
            if myinput == current_word.word[1:]:
                judgelab['text'] = '(v)'
                huilst.append(current_word)
                status = True
            else:
                judgelab['text'] = '(x)'
                sclst.append(current_word)
                status = False
        elif status == True:    #已判，正确：进入下一个单词
            index += 1
            nextword()
        elif status == False:   #已判，错误：进入记忆
            judgelab.config(text='')
            entry.config(state=libgui.NORMAL)
            entry.delete(0,libgui.END)
            index += 1
            nextword()
        else:
            raise ValueError(f'错误的状态: {status}')
    def nextword():
        if index == len(wlst):    #如果是最后一个单词
            libgui.showinfo('恭喜你学完({filename})',parent=win)
            close()
        else:
            #初始化变量
            nonlocal current_word,status
            current_word = wlst[index]
            status = None

            #显示下一个单词
            win.title(f'默写 {index+1}/{len(wlst)}')
            judgelab.config(text='')
            lenlab.config(text=f'{len(current_word.word)}){current_word.word[0]}')
            entry.config(state=libgui.NORMAL)
            entry.delete(0,libgui.END)
            translab.config(text=current_word.trans)
            wordlab.config(text='')
    def close():
        libsc.mark('write',sclst,huilst)
        lesson.progress[2] = index
        win.destroy()

    #初始化各种变量
    wlst = lesson.words #单词列表
    index = lesson.progress[2]  #当前学习的单词在单词列表中的索引
    status = None   #备选：None,True,False
                    #None:未判；True:已判，正确；False:已判，错误
    sclst = []      #生词列表
    huilst = []     #熟词列表
    current_word:libclass.Word = None   #当前学习的单词

    #初始化界面
    win = libgui.write(root)
    win.protocol('WM_DELETE_WINDOW',close)
    translab,lenlab,entry,judgelab,wordlab = win.translab,win.lenlab,win.entry,win.judgelab,win.wordlab
    entry.bind('<Return>',lambda event:enter())

    #显示第一个单词
    nextword()

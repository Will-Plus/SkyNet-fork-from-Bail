#Copyright Bail&Will&loaf0808 2025
#SkyNet:libstudy 学习模块

from abc import ABC,abstractmethod
import libgui,libunf,libclass,copy

class StudyModule(ABC):
    @abstractmethod
    def __call__(self):
        '''进行课程的学习'''
    def close(self)->tuple[list[libclass.Word],list[libclass.Word]]:
        '''关闭窗口时的回调
返回值：生词和熟词各自的列表'''

class Remember(StudyModule):
    '''记忆模块'''
    unflist:list[libclass.Word] = []   # 生词列表
    famlist:list[libclass.Word] = []   # 熟词列表
    index:int = 0                      # 当前单词的索引
    current_word:libclass.Word = None  # 当前学习的单词

    def __init__(self,
            window:libgui.RememberWindow,   # 根窗口
            lesson:libclass.Lesson,         # 要学习的课程对象
            unfHandler:libunf.UnfamiliarWordHandler  # 生词处理器对象
        ):
        self.window = window
        self.lesson = lesson
        self.unfHandler = unfHandler
        self.wlst = copy.copy(self.lesson.words)
    def hui4(self): #会，进入看对错
        self.window.check_right(self.current_word)
    def dui4(self): #对，标为熟词并进入下一个单词
        self.famlist.append(self.current_word)
        self.index += 1
        self.nextword()
    def bu4(self):  #不会/不对，标为生词并进入下一个单词
        self.unflist.append(self.current_word)
        self.index += 1
        self.nextword()
    def nextword(self):
        if self.index == len(self.wlst):  #如果是最后一个单词
            self.window.showinfo('提示',f'恭喜你学完({self.lesson.fullname})')
            self.close()
        else:
            self.current_word = self.wlst[self.index]
            self.window.title(f'记忆 {self.index+1}/{len(self.wlst)}')
            self.window.show_word(self.current_word)
    def close(self):
        self.unfHandler.mark('remember',self.unflist,self.famlist)
        self.lesson.progress[0] = self.index
        self.window.destroy()
    def __call__(self):
        #初始化界面
        self.window.protocol('WM_DELETE_WINDOW',self.close)
        self.window.huibtn.config(command=self.hui4)
        self.window.buhuibtn.config(command=self.bu4)
        self.window.duibtn.config(command=self.dui4)
        self.window.buduibtn.config(command=self.bu4)
        #显示第一个单词
        self.nextword()
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
        libunf.mark('write',sclst,huilst)
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

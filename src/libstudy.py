#Copyright Bail&Will&loaf0808 2025
#SkyNet:libstudy 学习模块

from abc import ABC,abstractmethod
import libgui,libunf,libclass,copy

class StudyModule(ABC):
    studyModuleID:str                  # 学习模块的ID，如remember,write
    unflist:list[libclass.Word] = []   # 生词列表
    famlist:list[libclass.Word] = []   # 熟词列表
    def __init__(self,
                 window:libgui.Window,                    # 根窗口
                 lesson:libclass.Lesson,                  # 要学习的课程对象
                 unfHandler:libunf.UnfamiliarWordHandler  # 生词处理器对象
                ):
        '''初始化'''
        self.window = window
        self.lesson = lesson
        self.unfHandler = unfHandler
        self.wlst = copy.copy(self.lesson.words)
    @abstractmethod
    def __call__(self):
        '''进行课程的学习'''

class Remember(StudyModule):
    '''记忆模块'''
    studyModuleID = 'remember'
    current_word:libclass.Word  # 当前学习的单词

    def __init__(self,window:libgui.RememberWindow,lesson:libclass.Lesson,unfHandler:libunf.UnfamiliarWordHandler):
        super().__init__(window,lesson,unfHandler)
        self.index = lesson.progress[self.studyModuleID]    # 当前单词的索引
        self.window = window    # 临时解决vscode不认识子类的问题
        #初始化界面
        self.window.protocol('WM_DELETE_WINDOW',self.close)
        self.window.huibtn.config(command=self.know)
        self.window.buhuibtn.config(command=self.no)
        self.window.duibtn.config(command=self.right)
        self.window.buduibtn.config(command=self.no)
    def know(self): #会，进入看对错
        self.window.check_right(self.current_word)
    def right(self): #对，标为熟词并进入下一个单词
        self.famlist.append(self.current_word)
        self.index += 1
        self.nextword()
    def no(self):  #不会/不对，标为生词并进入下一个单词
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
        self.unfHandler.mark(self.studyModuleID,self.unflist,self.famlist)
        self.lesson.progress[self.studyModuleID] = self.index
        self.window.destroy()
    def __call__(self):
        self.nextword()
class Write(StudyModule):
    '''默写模块'''
    studyModuleID = 'write'
    status = None   #备选：None,True,False
                    #None:未判；True:已判，正确；False:已判，错误
    current_word:libclass.Word  # 当前学习的单词
    def __init__(self,window:libgui.WriteWindow,lesson:libclass.Lesson,unfHandler:libunf.UnfamiliarWordHandler):
        super().__init__(window,lesson,unfHandler)
        self.index = lesson.progress[self.studyModuleID]    # 当前单词的索引
        self.window = window    # 临时解决vscode不认识子类的问题
        #初始化界面
        self.window.protocol('WM_DELETE_WINDOW',self.close)
        self.window.entry.bind('<Return>',lambda event:self.enter())
    def enter(self):
        match self.status:
            case None:
                self.window.show_word(self.current_word)
                myinput = self.window.entry.get()
                isright = myinput == self.current_word.word[1:]
                self.window.show_judge(isright)
                {True:self.famlist,False:self.unflist}[isright].append(self.current_word)
                self.status = isright
            case True|False:
                self.index += 1
                self.nextword()
                self.status = None
            case invalidStatus:
                raise ValueError(f'错误的状态: {invalidStatus}')
    def nextword(self):
        if self.index == len(self.wlst):    #如果是最后一个单词
            self.window.showinfo('提示',f'恭喜你学完({self.lesson.fullname})')
            self.close()
        else:
            #初始化变量
            self.current_word = self.wlst[self.index]
            self.status = None
            #显示下一个单词
            self.window.title(f'默写 {self.index+1}/{len(self.wlst)}')
            self.window.show_trans(self.current_word)
    def close(self):
        libunf.mark(self.studyModuleID,self.unflist,self.famlist)
        self.lesson.progress[self.studyModuleID] = self.index
        self.window.destroy()
    def __call__(self):
        self.nextword()

#Copyright Bail&Will&loaf0808 2025
#SkyNet:libunf 生词模块

'''"unf"是“Unfamiliar Word”（生词）的缩写（为了避免和ufw撞名）
响应地，“fam”是“Familiar Word”(熟词)的缩写'''

from tkinter import *
from tkinter import messagebox as msgbox,ttk
import time,libclass,os,libfile,libgui,libstudy,random,json

class UnfamiliarWord(libclass.Word):
    '''生词类 继承于:单词类'''
    right:int   # **连续**正确次数
    # 以下是弃用的属性，为了主线分支能够快速重构，暂时保留
    learn:int   # 学习次数
    wrong:int   # 错误次数
    review:int  # 下次复习时间戳
    def __init__(self,word:str,trans:str):
        '''生词类初始化'''
        super().__init__(word,trans)
    def serialize(self)->dict:
        '''序列化为字典，方便保存为json'''
        dic = {
            'word': self.word,
            'right': self.right
        }
        return dic
    @classmethod
    def unserialize(cls,dic:dict,lesson:libclass.Lesson):
        '''从字典反序列化为对象'''
        '''<think>
第一个问题：反序列化时，如何通过word获得trans等Word类中的信息
先得搞清楚哪里有这种对应关系。一个是课程文件中，一个是课程对象的words属性中。
从课程文件中获取好不好？我觉得不好，因为课程文件的存储格式是csv，而且存储在磁盘中。
每次读取，不仅需要磁盘io的开销，还需要繁杂的字符串操作，给人感觉效率和鲁棒性都比较低。
那就是从课程对象的words属性中获取。
但当前的words属性是list[libclass.Word]类型，无法实现通过word快速找到对象，需要进行遍历，效率低下。
要不要更改Lesson.words的数据类型？
其实可以改成dict[str:libclass.Word]类型，这样就可以快速地通过word查找对象了。
但需要考虑一个问题：原本的list是有序的，现在改成dict是无序的。这会不会产生什么影响？
如果放在旧版本，这还真实致命的影响：因为我的进度记录全靠列表的索引进行工作。
但新版中，要求有乱序功能；在我的策划中，新的Lesson类也有能力在乱序模式下保持进度记录。
这样一来，Lesson.words的顺序显得不是那么重要了。可以安全地转变为dict类型。
所以，决定改造新版Lesson类，并通过Lesson.words获取单词对象。
这样一来，这里就需要一个新的属性：单词所属的Lesson对象。
同时，还要考虑当word对应的单词条目不存在时的处理方案。
有三条思路：报错、忽略、默认值。
报错好不好？当然不能在程序里直接raise，而是应该给用户弹个窗，让用户知道出了问题。
这样的好处是让用户能够及时知情。但报错还不能直接退出程序，还得有个处理方案。
忽略好不好？其实也行，既然找不到单词了，那就认为这个生词不存在就好了。这样也就排除了“默认值”方案。
所以，最终方案是先给用户弹个窗，然后直接忽略。
下一个问题：怎么弹窗？
根据libgui的设计思路，所有Window对象都可以调用showerror()方法弹出错误提示框。
所以，要想弹窗，需要一个Window对象。
根据依赖注入原则，Window对象需要在创建对象时作为参数传入。
但Window对象和UnfamiliarWord对象没有半毛钱关系，传进去就是徒增混乱。
或许可以作为本方法的参数传入？我个人觉得也不太好。这里是反序列化，要那么重一个窗口干什么？
那就需要在本方法外部处理。这里可以先报个错，自定义一个错误类型，调用者捕获这个错误，进行弹窗。
但如果调用者没有捕获错误，会怎样？
先需要明确本方法是在什么时候会被调用，也就是什么时候需要用到生词列表？
在打开课程的学习窗口、生词管理窗口时、在后续进行全部生词的考察时。
其实，这个“通过单词获取对象”的功能不仅在这个方法中会用到，在其他很多地方都会用到。
不如放到Lesson类中，后续处理。
</think>'''
        obj = lesson.get_word(dic['word']).to_unf()
        obj.right = dic['right']
        return obj
    def to_fam(self):
        '''变成熟词 '''
        while self in self.lesson.unf:
            self.lesson.unf.remove(self)
        self.lesson.fam.append(self.lesson.get_word(self.word))
    def strenth(self):
        '''用于计算记忆强度
word(Sc):生词对象
返回值:记忆强度(float:.2f)'''
        return round((self.learn - self.wrong)/self.learn,2)
    def calculate_review_time(self)->str:
        '''计算到该单词复习时刻的时间'''
        if self.review <= time.time():
            return '0'
        sec = self.review-time.time()
        day,sec = divmod(sec,86400)
        hour,sec = divmod(sec,3600)
        minute,sec = divmod(sec,60)
        return f'{day}天{hour}时{minute}分{sec}秒'

class UnfamiliarWordHandler:
    def __init__(self,logger:libclass.Logger):
        self.logger = logger

def readfile():
    '''读取生词文件'''
    global remlst,wrilst
    for i in ('rem','wri'):
        lst = eval(f'{i}lst')
        fn = os.path.join(libfile.getpath('sc'),f'{i}.csv')
        lst0 = libfile.readfromcsv(fn)
        lst += [libclass.UnfamiliarWord(*i) for i in lst0]
def treesort(tree:ttk.Treeview,col:str,reverse:bool):
    print(tree.get_children(''))
    l = [tree.set((k,col),k) for k in tree.get_children('')]
    l.sort(reverse)
    for i,(val,k) in enumerate(l):
        tree.move(k,'',i)
        print(k)
    tree.heading(col,command=lambda:treesort(tree,col,True))
def deltatime(word:UnfamiliarWord)->int:
    '''计算复习延后秒数
word(libclass.Sc):生词对象
返回值:距下次复习秒数(int)'''
    strenth = word.strenth()*100
    x = int(('%.d' % strenth)[-1])
    
    #增加可读性
    day = 24*3600
    hour = 3600
    minute = 60

    #分段函数
    if 0 <= strenth < 10:
        return x
    elif 10 <= strenth < 20:
        return 10*x+10
    elif 20 <= strenth < 30:
        return 60*x+60+40
    elif 30 <= strenth < 40:
        return 3600*x+11*minute+40
    elif 40 <= strenth < 50:
        return day*x+10*hour+11*minute+40
    elif 50 <= strenth < 60:
        return 7*day*x+10*day+10*hour+11*minute+40
    elif 60 <= strenth < 70:
        return 10*day*x+80*day+10*hour+11*minute+40
    elif 70 <= strenth < 80:
        return 15*day*x+180*day+10*hour+11*minute+40
    elif 80 <= strenth < 90:
        return 20*day*x+330*day+10*hour+11*minute+40
    elif 90 <= strenth <= 100:
        return 28*day*x+530*day+10*hour+11*minute+40
    else:
        raise ValueError('值超出范围')
def mark(study_type:str,sclst:list,huilst:list):
    '''处理生词与熟词
study_type(str):课程类型 备选：remember,write
sclst(list):生词列表
huilst(list):熟词列表'''
    #根据类型获取数据列表
    if study_type == 'remember':
        data = remlst
    elif study_type == 'write':
        data = wrilst
    else:
        raise ValueError(f'非法的学习类型: {study_type}')

    #处理生词
    for i in sclst:
        for j in data:
            if i == j:   #如果生词已存在
                j.learn += 1
                j.wrong += 1
                j.review = int(time.time()+deltatime(j))
                break
        else:   #如果生词不存在
            sc = libclass.UnfamiliarWord(i.word,i.trans,1,1,int(time.time()))
            data.append(sc)

    #处理熟词
    for i in huilst:
        for j in data:
            if i == j:  #如果存在对应生词
                j.learn += 1
                j.review = int(time.time()+deltatime(j))

    #删除熟记生词
    for i in data:
        if i.strenth() > 0.95:
            data.remove(i)
def get_need_review_list(lst:list):
    '''分出需要复习的词
lst(list):生词列表
返回值:需要复习的生词列表(list)'''
    need_review = []
    for i in lst:
        if i.review <= time.time():
            need_review.append(i)
    return need_review
def review(scmain:Tk,sctype:str):
    '''生词复习及处理
scmain(tkinter.Toplevel):生词管理窗口
sclst(list):要复习的单词列表
lst(list):该类型的生词列表
sctype(str:remember/write):生词类型名称，用于调用libgui的函数'''
    #获取对应列表
    if sctype == 'remember':
        data = remlst
        func = libstudy.remember
    elif sctype == 'write':
        data = wrilst
        func = libstudy.write
    else:
        raise ValueError(f'非法的学习类型: {sctype}')

    #分出需要复习的词
    sclst = get_need_review_list(data)
    random.shuffle(sclst)
    lesson = libclass.Lesson(sclst,'',[0,0,0],name='sc',fullname='sc',author='bssenglish',file_version=-1)

    #复习生词
    func(scmain,lesson)
def savefile():
    '''将生词列表保存到文件'''
    for i in ('rem','wri'):
        lst = eval(f'{i}lst')
        fn = os.path.join(libfile.getpath('sc'),f'{i}.csv')
        libfile.saveascsv(lst,fn)
def control(root):
    '''生词模块主控
root(tkinter.Tk):主窗口'''
    scmain,*trees = gui_main(root)
    intree(*trees)

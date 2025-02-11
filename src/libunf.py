#Copyright Bail&Will&loaf0808 2025
#SkyNet:libunf 生词模块

'''"unf"是“Unfamiliar Word”（生词）的缩写（为了避免和ufw撞名）
响应地，“fam”是“Familiar Word”(熟词)的缩写'''

from tkinter import *
from tkinter import messagebox as msgbox,ttk
import time,libclass,os,libfile,libgui,libstudy,random

class UnfamiliarWord(libclass.Word):
    '''生词类 继承于:单词类'''
##    learn = wrong = 1	#学习1次，错误1次
    def __init__(self,word:str,trans:str,learn:int,wrong:int,review:int):
        '''生词类初始化
word(str):单词
trans(str):词义
review(int※不可为float):复习时间戳'''
        self.word = word
        self.trans = trans
        self.learn = int(learn)
        self.wrong = int(wrong)
        self.review = int(review)
    def strenth(self):
        '''用于计算记忆强度
word(Sc):生词对象
返回值:记忆强度(float:.2f)'''
        return round((self.learn - self.wrong)/self.learn,2)
    def items(self):
        return [self.word,self.trans,
                self.learn,self.wrong,self.review]
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

def imp(lst:list):
    '''从外部csv导入生词'''
    newlst = libfile.readfromcsv()
    lst += newlst
    msgbox.showinfo('提示','导入成功，请重启程序。')
def exp(lst:list):
    '''导出生词到外部csv'''
    libfile.saveascsv(lst)
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
def intree(remtree:ttk.Treeview,writree:ttk.Treeview):
##    rem,lis,wri = remlst,lislst,wrilst
    for i in remlst:
        remtree.insert('','end',
                       text=i.word,	#单词
                       values=(i.trans,	#词义
                               i.learn,i.wrong,	#学习次数，错误次数
                               i.strenth(),	#记忆强度
                               reviewtime(i)))	#复习时间
    for i in wrilst:
        writree.insert('','end',
                       text=i.word,	#单词
                       values=(i.trans,	#词义
                               i.learn,i.wrong,	#学习次数，错误次数
                               i.strenth(),	#记忆强度
                               reviewtime(i)))	#复习时间
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

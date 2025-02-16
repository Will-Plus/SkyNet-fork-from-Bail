#Copyright Bail&Will&loaf0808 2025
#SkyNet:libwordclass 单词类模块

LOGLEVEL = 0

Word = Lesson = None   #先定义一下，防止循环依赖时报错AttributeError
                            #这个问题在d48ccdb2d22ddd2672e17d05bb1bf7d659c6c5e4已经出现，暂无更好解决方案

from __future__ import annotations
import logging,libunf,libfile,os

class Word:
    '''单词类'''
    lesson:Lesson   # 在libfile.FileHandler.read_lesson_file()中传入
    def __init__(self,word:str,trans:str):
        self.word = word
        self.trans = trans
    def __str__(self)->str:
        return self.word
    def __eq__(self,b:Word):
        return self.word == b.word
    def to_unf(self):
        '''转为生词'''
        obj = libunf.UnfamiliarWord(self.word,self.trans)
        obj.right = 0
        self.lesson.unf.append(obj)
        while self in self.lesson.fam:
            self.lesson.fam.remove(self)
class Lesson:
    '''课程类'''
    def __init__(self,fileHandler:libfile.FileHandler,words:list[Word],**info):
        '''课程类初始化
info:课程信息。包括:
- name(str):课程简称（用于显示）
- fullname(str):课程全称
- author(str):课程作者/编写者（推荐附上邮箱，如：Bail <2915289604@qq.com>）
words(list):课程中包括的单词。列表中的对象类型为Word'''
        self.name = info['name']
        self.fullname = info['fullname']
        self.author = info['author']
##        self.file_version = info['file_version']  # 感觉不需要
        self.words:dict[str,Word] = {i.word:i for i in words}
        
        # 读取课程中的生词和熟词
        self.unf:list[libunf.UnfamiliarWord] = []
        self.fam:list[Word] = []
        # 先读取生词
        fn = os.path.join(fileHandler.getpath(libfile.LESSONS),self.name,'unf.json')
        unflist:list[dict] = libfile.Utils.readjson(fn)
        for i in unflist:
            self.unf.append(libunf.UnfamiliarWord.unserialize(i),self)
        # 再处理熟词
        fn = os.path.join(fileHandler.getpath(libfile.LESSONS),self.name,'fam.json')
        famlist:list[str] = libfile.Utils.readjson(fn)
        for i in famlist:
            self.fam.append(self.get_word(i),self)
##    def __iter__(self):
##        return self.words
    def get_word(self,word:str)->Word:
        '''根据单词字符串获取单词对象
-----------
注意抛出WordNotFoundError'''
        if word not in self.words:
            raise WordNotFoundError(self,word)
        return self.words[word]
class WrongFileVersion(Exception):
    '''课程文件版本错误'''
    def __init__(self,e):
        self.e = e
    def __str__(self) -> str:
        return self.e
class WordNotFoundError(KeyError):
    '''未从课程中找到单词'''
    def __init__(self, lesson:Lesson, word:str):
        super().__init__()
        self.lesson = lesson
        self.errorWord = word
    def __str__(self):
        return f'未从课程“{self.lesson.name}”中找到单词“{self.errorWord}”'

class Logger(logging.Logger):
    def __init__(self):
        super().__init__(__name__,LOGLEVEL)

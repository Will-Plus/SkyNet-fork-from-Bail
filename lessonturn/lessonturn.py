NUMBER_OF_WORD_IN_ONE_LINE = 15 # 一行的单词数，用于判断异常

import sys,json,os,csv

class Raw2Lines:
    def __init__(self):
        self.en_lines:list[list[str]] = []
        self.zh_lines:list[list[str]] = []
        self.line_number = 0
    def input(self):
        while True:
            print('请输入下一行 >',end='')
            sys.stdout.flush()
            if not (line := sys.stdin.read()):
                break
            self.line_number += 1
            if self.line_number % 2:    # 英文
                self.en_lines.append(line.split())
            else:
                self.zh_lines.append(line.split())
    def turn(self):
        for i,j in enumerate(self.en_lines): # 每一行
            for k,l in enumerate(j): # 每一个单词
                now = ''    # 当前单词
                for m in l: # 每一个字符
                    if m.isdigit():
                       continue
                    now += m
                j[k] = now
            self.en_lines[i] = j
    def remove_spaces(self):
        for i in self.en_lines:
            while '' in i:
                i.remove('')
    def check_length(self):
        for i in self.en_lines+self.zh_lines:
            if (length := len(i)) != NUMBER_OF_WORD_IN_ONE_LINE:
                i.append(f'#########{length}')   # 数量错误，人工处理
    def save(self,filename:str):
        with open(filename,'w',encoding='utf-8') as file:
            for i in range(int(self.line_number/2)):
                print(json.dumps(self.en_lines[i]),file=file)
                print(json.dumps(self.zh_lines[i],ensure_ascii=False),file=file)
class Csv2Lines:
    def __init__(self,csvreader):
        self.reader = csvreader
        self.en_lines:list[list[str]] = []
        self.zh_lines:list[list[str]] = []
        self.line_number = 0
    @classmethod
    def open(cls,filename:str):
        file = open(filename,encoding='utf-8')
        reader = csv.reader(file)
        obj = cls(reader)
        obj.file = file
        return obj
    def turn(self):
        for i,j in enumerate(self.reader):
            if not j:
                continue
            if i%2 == 0:
                self.en_lines.append(j)
            else:
                self.zh_lines.append(j)
        if len(self.en_lines) != len(self.zh_lines):
            raise ValueError('中英文长度不同，请检查后再试')
        self.line_number = len(self.en_lines)
    def save(self,filename:str):
        with open(filename,'w') as file:
            for i in range(int(self.line_number/2)):
                print(json.dumps(self.en_lines[i]),file=file)
                print(json.dumps(self.zh_lines[i],ensure_ascii=False),file=file)
    def close(self):
        if not hasattr(self,'file'):
            raise RuntimeError('你不是以Csv2Lines.open()的方式打开的')
        self.file.close()
class Lines2Lesson:
    def __init__(self):
        self.en_lines:list[list[str]] = []
        self.zh_lines:list[list[str]] = []
        self.result_lines:list[str] = []
    @classmethod
    def from_file(cls,filename:str):
        obj = cls()
        with open(filename,encoding='utf-8') as file:
            lines = file.read().split('\n')
        for i,j in enumerate(lines):
            if not j:
                continue
            if i%2 == 0:
                obj.en_lines.append(json.loads(j))
            else:
                obj.zh_lines.append(json.loads(j))
        return obj
    def turn(self):
        en = [j for i in self.en_lines for j in i]
        zh = [j for i in self.zh_lines for j in i]
        if len(en) != len(zh):
            raise ValueError('中英文长度不同，请检查后再试')
        for i in range(len(en)):
            self.result_lines.append('\t'.join((en[i],zh[i])))
    def save(self,filename:str):
        with open(filename,'w',encoding='utf-8') as file:
            file.write('\n'.join(self.result_lines))

def interactive():
    filename = input('文件名 >')
    lines_filename = filename+'.lines'
    lesson_filename = filename+'.lesson'
    raw2lines = Raw2Lines()
    raw2lines.input()
    raw2lines.turn()
    raw2lines.remove_spaces()
    raw2lines.check_length()
    raw2lines.save(lines_filename)
    input('请手动编辑文件，按回车键继续')
    lines2lesson = Lines2Lesson.from_file(lines_filename)
    lines2lesson.turn()
    lines2lesson.save(lesson_filename)
def fromcsv():
    filename = input('csv文件名 >')
    lines_filename = filename+'.lines'
    lesson_filename = filename+'.lesson'
    csv2lines = Csv2Lines.open(filename)
    csv2lines.turn()
    csv2lines.save(lines_filename)
    csv2lines.close()
    lines2lesson = Lines2Lesson.from_file(lines_filename)
    lines2lesson.turn()
    lines2lesson.save(lesson_filename)
def main():
    print('''1. 交互式（复制粘贴pdf）
2. 自动式（需提供csv）''')
    match input('请输入转换方式 >'):
        case '1':
            interactive()
        case '2':
            fromcsv()
        case invalid_input:
            print(f'无效的输入：{invalid_input}')

if __name__ == '__main__':
    main()

NUMBER_OF_WORD_IN_ONE_LINE = 15 # 一行的单词数，用于判断异常

import sys,json,os

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
        with open(filename,'w') as file:
            for i in range(int(self.line_number/2)):
                print(json.dumps(self.en_lines[i]),file=file)
                print(json.dumps(self.zh_lines[i],ensure_ascii=False),file=file)
class Lines2Lesson:
    def __init__(self):
        self.en_lines:list[list[str]] = []
        self.zh_lines:list[list[str]] = []
        self.result_lines:list[str] = []
    @classmethod
    def from_file(cls,filename:str):
        obj = cls()
        with open(filename) as file:
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
        with open(filename,'w') as file:
            file.write('\n'.join(self.result_lines))

def main():
    filename = input('文件名 >')
    if not os.path.exists(filename):
        raw2lines = Raw2Lines()
        raw2lines.input()
        raw2lines.turn()
        raw2lines.remove_spaces()
        raw2lines.check_length()
        raw2lines.save(filename)
        input('请手动编辑文件，按回车键继续')
    lines2lesson = Lines2Lesson.from_file(filename)
    lines2lesson.turn()
    lines2lesson.save(filename)

if __name__ == '__main__':
    main()

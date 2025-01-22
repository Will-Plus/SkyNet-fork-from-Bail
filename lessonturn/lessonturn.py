NUMBER_OF_WORD_IN_ONE_LINE = 15 # 一行的单词数，用于判断异常

import sys,json,csv,pandas

class Reader(list[list[str]]):
    '''csv读取后的二维数组'''
    pass
class Lines:
    def __init__(self,en_lines:list[list[str]],zh_lines:list[list[str]]):
        if len(en_lines) != len(zh_lines):
            raise ValueError('中英文长度不同，请检查后再试')
        self.en_lines:list[list[str]] = en_lines
        self.zh_lines:list[list[str]] = zh_lines
        self.line_number = len(en_lines)
    @classmethod
    def from_reader(cls,reader:Reader):
        '''从reader读入'''
        en_lines:list[list[str]] = []
        zh_lines:list[list[str]] = []
        counter = 0 # 成功录入的行数，用于区分中文和英文
        for i in reader:
            # 去除空字符串
            while '' in i:
                i.remove('')
            # 跳过空行
            if not i:
                continue
            # 转存
            if counter%2 == 0:
                en_lines.append(i)
            else:
                zh_lines.append(i)
            # 增加计数器
            counter += 1
        return cls(en_lines,zh_lines)
    @classmethod
    def from_input(cls,filename:str):
        '''从键盘输入，filename为暂时存储用于排错的文件名'''
        # 初始化变量
        en_lines:list[list[str]] = []
        zh_lines:list[list[str]] = []
        line_number = 0
        # 输入
        while True:
            print('请输入下一行 >',end='')
            sys.stdout.flush()
            if not (line := sys.stdin.read()):
                break
            line_number += 1
            if line_number % 2:    # 英文
                en_lines.append(line.split())
            else:
                zh_lines.append(line.split())
        # 过滤英文中的数字字符
        for i,j in enumerate(en_lines): # 每一行
            for k,l in enumerate(j): # 每一个单词
                now = ''    # 当前单词
                for m in l: # 每一个字符
                    if m.isdigit():
                       continue
                    now += m
                j[k] = now
            en_lines[i] = j
        # 去除空格
        for i in en_lines:
            while '' in i:
                i.remove('')
        # 检查当前行的长度
        for i in en_lines+zh_lines:
            if (length := len(i)) != NUMBER_OF_WORD_IN_ONE_LINE:
                i.append(f'#########{length}')   # 数量错误，人工处理
        with open(filename,'w',encoding='utf-8') as file:
            for i in range(int(line_number/2)):
                print(json.dumps(en_lines[i]),file=file)
                print(json.dumps(zh_lines[i],ensure_ascii=False),file=file)
        # 提示用户手动处理
        input('请手动编辑文件，按回车键继续')
        # 再次读取，生成对象
        with open(filename,encoding='utf-8') as file:
            lines = file.read().split('\n')
        reader:Reader = []
        for i in lines:
            if i:    # 防止空行引起的bug
                try:
                    reader.append(json.loads(i))
                except json.decoder.JSONDecodeError:
                    print(f'存在错误的行：{i}')
                    raise
        return cls.from_reader(reader)
    @classmethod
    def from_csv(cls,filename:str):
        '''从csv读取'''
        file = open(filename,encoding='utf-8')
        reader = csv.reader(file)
        obj = cls.from_reader(reader)
        file.close()
        return obj
    @classmethod
    def from_xlsx(cls,filename:str):
        # 读取文件
        reader = pandas.read_excel(filename,header=None).fillna('').values.tolist()
        # 生成对象
        return cls.from_reader(reader)
    def to_lesson(self,filename:str):
        result_lines:list[str] = []
        en = [j for i in self.en_lines for j in i]
        zh = [j for i in self.zh_lines for j in i]
        if len(en) != len(zh):
            raise ValueError('中英文长度不同，请检查后再试')
        for i in range(len(en)):
            result_lines.append('\t'.join((en[i],zh[i])))
        with open(filename,'w',encoding='utf-8') as file:
            file.write('\n'.join(result_lines))

def interactive():
    filename = input('文件名 >')
    lines_filename = filename+'.lines'
    lesson_filename = filename+'.lesson'
    Lines.from_input(lines_filename).to_lesson(lesson_filename)
def fromcsv():
    filename = input('csv文件名 >')
    lesson_filename = filename+'.lesson'
    Lines.from_csv(filename).to_lesson(lesson_filename)
def fromxlsx():
    filename = input('xlsx文件名 >')
    lesson_filename = filename+'.lesson'
    Lines.from_xlsx(filename).to_lesson(lesson_filename)
def main():
    print('''1. 交互式（复制粘贴pdf）
2. 自动式（从csv）
3. 自动式（从xlsx）''')
    match input('请输入转换方式 >'):
        case '1':
            interactive()
        case '2':
            fromcsv()
        case '3':
            fromxlsx()
        case invalid_input:
            raise ValueError(f'无效的输入：{invalid_input}')

if __name__ == '__main__':
    sys.exit(main())

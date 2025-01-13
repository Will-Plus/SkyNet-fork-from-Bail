#Copyright Bail&Will&loaf0808 2025
#SkyNet:lessonturn:input 课程文件转换从输入 v1.0.0.4_5

import sys,os

if len(sys.argv) == 1:
    fn = input('要转换的文件 >')
else:
    fn = sys.argv[1]
slst = []
with open(fn) as file:
    for i in file.readlines():
        lst = i.split('\t')
        s = '\t'.join(lst)
        slst.append(s)
os.rename(fn,f'{fn}.bak')
with open(fn,'w') as file:
    file.write('file_version=3\n')
    for i in slst:
        file.write(f'{i}')

#Copyright Bail&Will&loaf0808 2021-2022
#SkyNet:lessonturn:1to2 课程文件转换v1到v2 v1.0.2_3

import sys,os

if len(sys.argv) == 1:
    fn = input('要转换的文件 >')
else:
    fn = sys.argv[1]
slst = []
with open(fn) as file:
    for i in file.readlines():
        lst = i.split()
        s = ' '.join(lst)
        slst.append(s)
os.rename(fn,f'{fn}.1bak')
with open(fn,'w') as file:
    for i in slst:
        file.write(f'{i}\n')


#Copyright Bail&Will&loaf0808 2025
#SkyNet:lessonturn:2to3 课程文件转换v2到v3 v1.0.1_3

import sys,os

if len(sys.argv) == 1:
    fn = input('要转换的文件 >')
else:
    fn = sys.argv[1]
slst = []
with open(fn) as file:
    s = file.read().replace(' ','\t')
    s = s.replace('_',' ')
os.rename(fn,f'{fn}.2bak')
with open(fn,'w') as file:
    file.write('file_version=3\n'+s)


#Copyright Bail&Will&loaf0808 2025
#SkyNet:lessonturn:3to4 课程文件转换v3到v4 v1.0_1

import sys,os,libfile

if len(sys.argv) == 1:
    fn = input('要转换的文件 >')
else:
    fn = sys.argv[1]
name = fn.split(os.sep)[-1]
os.rename(fn,f'{fn}.2bak')
with open(f'{fn}.blf','w') as file:
    file.write(libfile.LESSON_FILE_HEADER)
    file.write('{"name":"%s","fullname":"%s","author":"null","file_version":4}\n' % (name,name))
    with open(f'{fn}.2bak') as origin_file:
        origin_file.readline()
        file.writelines(origin_file.readlines())

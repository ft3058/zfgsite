__author__ = 'wxd'
import os


s = "[path=/a/b 1.txt,2.txt] | [path=/c/d 8.bak,9.bak]"


paths = filter(None, [x.strip() for x in s.split('|')])
print paths

all_files = []

for path in paths:
    # ['[path=/a/b 1.txt,2.txt]', '[path=/c/d 8.bak,9.bak]']
    path = path.replace('[path=', '').replace(']', '')
    print '-path-', path
    path_head = path.split(' ')[0]
    path_tail = path.split(' ')[-1]
    for l in path_tail.split(','):
        l = l.strip()
        if l:
            all_files.append(os.path.join(path_head, l))

for k in all_files:
    print k
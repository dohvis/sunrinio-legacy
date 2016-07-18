import os
from sunrinio.settings.base import BASE_DIR


def run():
    dic = {'.html': 0, '.py': 0, '.css': 0, '.js': 0}
    for (path, dir, files) in os.walk(BASE_DIR):
        if 'env' in path or 'static' in path or '.git' in path or '.idea' in path:
            continue
        for filename in files:
            ext = os.path.splitext(filename)[-1]
            try:
                num_lines = sum(1 for line in open(os.path.join(path, filename), encoding='utf-8'))
            except UnicodeDecodeError:
                continue
            try:
                dic[ext] += num_lines
            except KeyError:
                dic[ext] = num_lines
            print(path, filename, num_lines)

    print(dic, sum([(dic[k]) for k in dic.keys()]))

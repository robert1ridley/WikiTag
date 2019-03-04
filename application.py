import json
from flask import Flask, request
import time
from py_aho_corasick import py_aho_corasick
application = app = Flask(__name__)
tagList = []
max_length = 2


def print_time(info):
    print(info, time.localtime(time.time()))


with open('result.txt', 'r') as f:
    for line in f.readlines():
        item = line.strip()
        temp_list = item.split(' ')
        add = True
        for i in temp_list:
            if len(i) < 3 or len(i) >= 9:
                add = False
                break
        if add and 2 <= len(temp_list) <= max_length:
            tagList.append(item)


print("tag number ", len(tagList))
print_time("begin build tire tree")
A = py_aho_corasick.Automaton(tagList)
print_time("end build tire tree")


def is_letter(v):
    if 'a' <= v <= 'z' or 'A' <= v <= 'Z':
        return True
    else:
        return False


def match(query):
    print_time("begin_query")
    index, value, next_index, longest_length, longest_str = -1, None, -1, 0, None
    save = []
    for idx, k, v in A.get_keywords_found(query):
        if idx != index and k != value:
            save.append((idx, len(k), k))
            index, value = idx, k
    save.sort(key=lambda c: (c[0], c[1]))
    result, index = [], -1
    for idx, length, k in save:
        print(str(idx) + " " + k)
        '''增加匹配的最长字符串'''
        if idx != index and longest_str is not None:
            if longest_length > 0:
                result.append({"begin": next_index , "content": longest_str, "derviation": "Wikipedia", "href": "https://en.wikipedia.org/wiki/"})
            next_index += longest_length
            longest_length = 0
            longest_str = None
        '''第一次合法更新'''
        if (idx == 0 or not is_letter(query[idx-1])) and idx != index and idx >= next_index:
            next_index = idx
            last_index = idx + len(k)
            if last_index >= len(query) or not is_letter(query[last_index]):
                longest_length = len(k)
                longest_str = k
            index = idx
        ''''遇到同样开始的字符串'''
        if idx == index:
            last_index = idx + len(k)
            if last_index >= len(query) or not is_letter(query[last_index]):
                longest_length = len(k)
                longest_str = k
    if longest_str is not None:
        result.append({"begin": next_index, "content": longest_str, "derviation": "Wikipedia",
                       "href": "https://en.wikipedia.org/wiki/"})
    print_time("end_query")
    return result


@app.route("/")
def hello():
    try:
        query = request.args.get('sentence')
        page = request.args.get('page')
        try:
            per_page = request.args.get('per_page')
        except:
            pass
        result = match(query)
        data = {
            "sentence": query,
            "count": len(result),
            "page": 1,
            "perpage": len(result),
            "corpuses": result
        }
        return json.dumps({
            "errno": 0,
            "message": "成功",
            "data": data
        })
    except:
        return json.dumps({"errno": 5704, "message": "描述出错"})


if __name__ == '__main__':
    app.run(
        host='0.0.0.0'
    )
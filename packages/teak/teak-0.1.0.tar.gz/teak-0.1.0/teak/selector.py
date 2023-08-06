import json

sample = '''
{
    "list": [
        {
            "id": 200,
            "name": "abc",
            "struct": {
                "a" : 1000
            }
        },
        {
            "id": 201,
            "name": "bca",
            "struct": {
                "a" : 1000
            }
        }
    ],
    "depth": 30,
    "size" : {
        "width": 20,
        "height": 10
    }
}
'''


def select(selector, jsonstr):
    d = json.loads(jsonstr)
    node = selector.split('.')
    ptr = [d]
    
    for n in node:

        newptr = []
        if n[-2:] == '[]':
            for p in ptr:
                if n[:-2] in p:
                    arr = p[n[:-2]]
                    for a in arr:
                        newptr.append(a)
        else:
            for p in ptr:
                if n in p:
                    newptr.append(p[n])

        ptr = newptr

    return ptr



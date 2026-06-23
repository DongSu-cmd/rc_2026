
import json


def main():
    dict_a = {"a":"aa"}
    print(type(dict_a))
    dict_a["b"] = "bbb"
    print(dict_a)
    print(dict_a["a"], dict_a["b"], dict_a.get("c"))

    print(dict_a.pop("a"))
    print(dict_a)

    dict_a["a"] = "aa"
    dict_a["b"] = "bbb"
    dict_a["c"] = "cccc"
    dict_a["d"] = "ddddd"

    for key in dict_a: #순서바뀜
            print(key, dict_a[key])

    for key, value in dict_a.items():
            print(key, value)
    print(dict_a.keys())
    print(dict_a.values())

    with open("data/" + dict_a["a"], "w", encoding="utf-8") as f:
                json.dump(dict_a, f, ensure_ascii=False, indent=4)
    if __name__=="__main__":
            main()

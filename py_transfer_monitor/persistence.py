# -*- coding: utf-8 -*-
"""
数据持久化
"""
import json


def load(path: str = "data/data.json") -> dict:
    try:
        with open(path, 'r') as f:
            data = json.load(f)
        return data
    except:
        return {}


def save(data: dict, path: str = "data/data.json") -> None:
    try:
        with open(path, 'w') as f:
            json.dump(data, f)
            f.close()
        return True
    except:
        return False


if __name__ == "__main__":
    data = load()
    print(data)

    data["a"] = 1
    data["b"] = {"abc": 111}
    print(data)
    save(data)

    data = load()
    print(data)

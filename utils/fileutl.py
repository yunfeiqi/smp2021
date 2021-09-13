import pickle
import json


def save_obj(obj,path):
    path = "/data1/qyf/smp2021/dataset20210721/graph/" + path
    with open(path,'wb') as f:
        pickle.dump(obj,f)
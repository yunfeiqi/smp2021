import pickle
import json


def save_obj(obj,path):
    with open(path,'wb') as f:
        pickle.dump(obj,f)
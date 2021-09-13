
from utils.fileutl import *


def build_entity(x,prefix,entit_type):
    x = set(x)
    node_user = [prefix + str(i) for i in x]
    print("Build Entity:" + entit_type + ",Length: " + len(node_user))
    save_obj(node_user,entit_type +".pkl")


def build_relation():
    pass
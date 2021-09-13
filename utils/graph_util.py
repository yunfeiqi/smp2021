
from utils.fileutl import *


def build_entity(x,prefix,entit_type):
    '''
        x: 实体对象
        prefix: 实体前缀
        entit_type: 实体类型
    '''
    x = set(x)
    node_user = [prefix + str(i) for i in x]
    print("Build Entity:" + entit_type + ",Length: " + str(len(node_user)))
    save_obj(node_user,entit_type +".pkl")


def build_relation(x,left_name,right_name,prefix_left,prefix_right,relarray):
    '''
        x: pandas 对象
        left_name: 左实体名称
        right_name: 右实体名称
        prefix_left: 左实体前缀
        prefix_right: 右实体前缀
        relarray: 关系集合对象
    '''
    left = str(x[left_name])
    right = str(x[right_name])
    left = prefix_left + left
    right = prefix_right + right
    rel = (left,right)
    relarray.add(rel)

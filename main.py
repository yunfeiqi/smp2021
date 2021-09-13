




import json
from os import sep
import pandas as pd

# read config
with open("conf.json",'r',encoding="utf-8") as f:
    conf = json.load(f)

# 商家
pois_path = conf["base_path"] + conf["poi_name"]
# 菜品
spus_path = conf["base_path"] + conf["spus_name"]
# 用户
user_path = conf["base_path"] + conf["user_name"]

# 训练数据
spus_train_data_path = conf["base_path"] + conf["spus_train_name"]
# 训练标签
spus_train_label_path = conf["base_path"] + conf["spus_train_label"]
# 测试数据
spus_test_data_path = conf["base_path"] + conf["spus_test_name"]
# 测试标签
spus_test_label_path = conf["test_path"] + conf["spus_test_label"]


# load data
# 商家
pois = pd.read_csv(pois_path,sep="\t")
# 菜品
spus = pd.read_csv(spus_path,sep="\t")
# 用户
user = pd.read_csv(user_path,sep="\t")
# 训练数据
train_data = pd.read_csv(spus_train_data_path,sep="\t")
# 训练标签
train_label = pd.read_csv(spus_train_label_path,sep="\t")
# 测试数据
test_data = pd.read_csv(spus_test_data_path,sep="\t")
# 测试标签
test_label = pd.read_csv(spus_test_label_path,sep="\t")

# preprocess 


# build entities



# build relations

# graph embeddings

# train 


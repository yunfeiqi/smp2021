
import json
import pandas as pd

from utils.fileutl import save_obj
from utils.graph_util import *
from utils.trans import * 

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

# 加载数据

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


# 用户实体
build_entity(user.user_id.unique(),"user_id_","user")

# 价格实体
build_entity(range(0,6),"price_","price")

# 商家实体
pois = pois[~pois.wm_poi_id.isna()]
build_entity(pois.wm_poi_id.unique(),"pois_","poi")

# 订单
train_order_id = set(train_data.wm_order_id.unique())
test_order_id = set(test_data.wm_order_id.unique())

order_id = train_order_id | test_order_id
build_entity(order_id,"order_id_","order_")

# 商圈ID
aor_id = list(map(lambda x:int(x),filter(lambda x: not pd.isna(x),pois.aor_id.unique())))
build_entity(aor_id,"aor_id_","aor")

# 收餐兴趣面ID
aoi_id = list(map(lambda x:int(x),filter(lambda x: not pd.isna(x),train_data.aoi_id.astype("category").unique())))
aoi_id2 = list(map(lambda x:int(x),filter(lambda x: not pd.isna(x),test_data.aoi_id.astype("category").unique())))
aoi_id.extend(aoi_id2)

build_entity(aoi_id,"aoi_id_","aoi")

# 星期
build_entity(range(1,8),"week_","week")

# 菜品
food_id = spus.wm_food_spu_id.unique()

build_entity(food_id,"spu_id_","spu")

# 口味

taste = set(flatmap(str2array,filter(lambda x:not isinstance(x,float),spus.taste.unique())))
build_entity(taste,"taste_","taste")

# 食材
ingredients = set(flatmap(str2array,filter(lambda x:not isinstance(x,float),spus.ingredients.unique())))
build_entity(ingredients,"ingredient_","ingredient")
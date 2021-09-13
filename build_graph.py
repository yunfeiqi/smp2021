
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

def build_entities():
    print("开始构建实体。。。。。")

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
    build_entity(order_id,"order_id_","order")

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

    print("实体构建完成")

def build_relations():
    print("开始构建关系。。。。。")


    # 用户-订单
    rel_user_order = set([])
    _ = train_data.apply(build_relation,args=("user_id","wm_order_id","user_id_","order_id_",rel_user_order),axis=1)
    _ = test_data.apply(build_relation,args=("user_id","wm_order_id","user_id_","order_id_",rel_user_order),axis=1)

    save_obj(rel_user_order,"rel_user_order.pkl")

    # 用户-收餐兴趣面ID
    rel_user_aoi_id = set([])
    _ = train_data.apply(build_relation,args=("user_id","aoi_id","user_id_","aoi_id_",rel_user_aoi_id),axis=1)
    _ = test_data.apply(build_relation,args=("user_id","aoi_id","user_id_","aoi_id_",rel_user_aoi_id),axis=1)

    save_obj(rel_user_aoi_id,"rel_user_aoi_id.pkl")
    

    # 订单-商圈收餐兴趣面ID
    rel_order_id_aoi_id = set([])

    _d1 = train_data[["wm_order_id","aoi_id"]].dropna()
    _d2 = test_data[["wm_order_id","aoi_id"]].dropna()

    _ = _d1.apply(build_relation,args=("wm_order_id","aoi_id","order_id_","aoi_id_",rel_order_id_aoi_id),axis=1)
    _ = _d2.apply(build_relation,args=("wm_order_id","aoi_id","order_id_","aoi_id_",rel_order_id_aoi_id),axis=1)

    save_obj(rel_order_id_aoi_id,"rel_order_id_aoi_id.pkl")

    # 订单-商圈ID
    rel_order_id_aor_id = set([])

    _d1 = train_data[["wm_order_id","aor_id"]].dropna()
    _d2 = test_data[["wm_order_id","aor_id"]].dropna()
    
    _ = _d1.apply(build_relation,args=("wm_order_id","aor_id","order_id_","aor_id_",rel_order_id_aor_id),axis=1)
    _ = _d2.apply(build_relation,args=("wm_order_id","aor_id","order_id_","aor_id_",rel_order_id_aor_id),axis=1) 

    save_obj(rel_order_id_aor_id,"rel_order_id_aor_id.pkl")  

    # 订单-时间（星期X）
    rel_order_id_week = set([])
    train_label["week"] = list(map(conver2week,train_label.dt))
    train_label.apply(build_relation,args=("wm_order_id","week","order_id_","week_",rel_order_id_week),axis =1)
    
    test_label["week"] = list(map(conver2week,test_label.dt))
    test_label.apply(build_relation,args=("wm_order_id","week","order_id_","week_",rel_order_id_week),axis =1)

    save_obj(rel_order_id_week,"rel_order_id_week.pkl")  

    ## 商家-商圈
    rel_poi_id_aoi_id = set([])

    _d1 = train_data[["wm_poi_id","aoi_id"]].dropna()
    _d1.apply(build_relation,args=("wm_poi_id","aoi_id","pois_","aoi_id_",rel_poi_id_aoi_id),axis=1)

    save_obj(rel_poi_id_aoi_id,"rel_poi_id_aoi_id.pkl")  

    ## 菜品-口味
    rel_spu_id_taste_id= set([])

    _d1 = spus[["wm_food_spu_id","taste"]].dropna()
    _d1.apply(build_flatmap_relation,args=("wm_food_spu_id","taste","spu_id_","taste_",rel_spu_id_taste_id),axis=1)

    save_obj(rel_spu_id_taste_id,"rel_spu_id_taste_id.pkl")  

    ## 菜品-食材

    rel_spu_id_ingredients = set([])

    _d1 = spus[["wm_food_spu_id","ingredients"]].dropna()
    _d1.apply(build_flatmap_relation,args=("wm_food_spu_id","ingredients","spu_id_","ingredient_",rel_spu_id_ingredients),axis=1)

    save_obj(rel_spu_id_ingredients,"rel_spu_id_ingredients.pkl")  

    ## 菜品-价格

    rel_spu_id_price = set([])

    _d1 = spus[["wm_food_spu_id","price"]].dropna()
    _d1["level"] = map(map_pay_lavel,_d1.price)
    _d1.apply(build_relation,args=("wm_food_spu_id","level","spu_id_","price_",rel_spu_id_price),axis=1)


    save_obj(rel_spu_id_price,"rel_spu_id_price.pkl")  

    ## 菜品-商圈ID
    rel_spu_id_aoi_id =set([])

    merge_spus_train_data = train_data.merge(train_label,left_on="wm_order_id",right_on="wm_order_id")
    _d1 = merge_spus_train_data[["wm_food_spu_id","aoi_id"]].dropna()

    _d1.apply(build_relation,args=("wm_food_spu_id","aoi_id","spu_id_","aoi_id_",rel_spu_id_aoi_id),axis=1)

    save_obj(rel_spu_id_aoi_id,"rel_spu_id_aoi_id.pkl")  

    print("关系构建完毕")

# 构建实体
build_entities()

build_relations()



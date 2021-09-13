from datetime import datetime

def flatmap(f,x):
    y = []
    for _x in x:
        y.extend(f(_x))
    return y
    
def str2array(x):
    # preprocess
    x = x.replace("[","").replace("]","").replace(r" ","")
    y = x.split(",")
    return y

def conver2week(x):
    '''
        时间转星期
    '''
    dt = str(x)
    dt = datetime.strptime(dt, '%Y%m%d')
    weekday=  dt.weekday()
    return weekday
        
def map_price_lavel(x):
    
    if x  == "未知" or isinstance(x,float):
        return 0
    elif x == '<29':
        return 1
    elif x == '[29,36)':
        return 2
    elif x == '[36,49)':
        return 3
    elif x == '[49,65)':
        return 4
    elif x == '>=65':
        return 5

def map_pay_lavel(x):
    try:
        x = float(x)
        if x < 29:
            return 1
        elif x < 36:
            return 2
        elif x < 49:
            return 3
        elif x <65:
            return 4
        else:
            return 5
    except ValueError:
        pass
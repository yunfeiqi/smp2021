

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

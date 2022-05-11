def print_class_vars(cls):
    for a,b in vars(cls).items():
        print(str(a) + ":" + str(b))

        

class top1:
    a : int = 0
    
    class bot1:
        pass


class top2(top1):
    pass

a = top2()


class top3:
    def __new__(cls):
        return cls

class top4(top3):
    def __new__(cls):
        return cls

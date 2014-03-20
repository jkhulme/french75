def one(a,b,c):
    print a,b,c

def two(*args, **kwargs):
    kwargs['mname'](*args)

def three(a,b,c):
    two(a,b,c,mname=one)

three(1,2,3)

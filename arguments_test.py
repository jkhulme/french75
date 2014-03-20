def one(a,b,c):
    print a,b,c

def two(*args):
    one(*args)

def three(a,b,c):
    two(a,b,c)

three(1,2,3)

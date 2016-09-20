# coding=UTF-8
import math

def f1(x):
    return math.pow(math.pow(x,2), 1.0/3)+math.sqrt(1-x*x)

def f2(x):
    return math.pow(math.pow(x,2), 1.0/3)-math.sqrt(1-x*x)

def f3(x):
    return x*x

def calc(sx,ex,n,f):
    s=0
    dx=(ex-sx)*1.0/n
    x=sx
    for i in range(n-1):
        s+=(f(x)+f(x+dx))*dx/2.0
        x+=dx
    return s

if __name__=="__main__":
    sx=-1
    ex=1
    n=100000
    print(calc(sx, ex, n, f1)-calc(sx, ex, n, f2))
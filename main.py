
class A():
 def __init__(self,a):
  self.a=a

def fun1(a):
 print(a)

def fun2(a):
 a=A(2)
 print(a)
if __name__=='__main__' :
 a=A(1)
 fun1(a)
 fun2(a)
 fun1(a)

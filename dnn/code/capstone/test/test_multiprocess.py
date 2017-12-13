import multiprocessing as mp
import time

'''
def f(x):
  def mul():
    result = x * 10
    return result
  result = mul()
  return result

if __name__=="__main__":
  p = Pool(5)
  start = time.time()
  print p.map(f, [1, 2, 3])
  end = time.time()
  print end-start
'''

'''
class Test(object):
  def __init__(self, x, y):
    self.x = x
    self.y = y
  def calMul(self, z):
    return self.x * self.y * z

def multi_run(args):
  return inMul(*args)

def inMul(y, z):
  return 10*y*z

def main():
  t = Test(10, 5)
  x = 1
  p = Pool()
  result = p.map(multi_run, [(x,2), (2,3)])
  print result

if __name__=="__main__":
  main()
'''
def cal(tp_q):
  q, x, y = tp_q
  q.put((x,y))

if __name__=="__main__":
  p = mp.Pool(4)
  q = mp.Queue()
  p.map_async(cal, [(q,1,2), (q,2,3)])
  
  print q.get()
  

from multiprocessing import Pool
import time

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

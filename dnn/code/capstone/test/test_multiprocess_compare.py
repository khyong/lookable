import time

def f(x):
  for i in xrange(1000000):
    result = x*x*x*x*x
  return result

if __name__=="__main__":
  start = time.time()
  for c in [1,2,3]:
    print f(c)
  end = time.time()
  print end-start

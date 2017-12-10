import main_object_detection as od



def main():
  od.loadModel()
  od.loadLabelMap()
  od.getImage('front')

if __name__=="__main__":
  main()

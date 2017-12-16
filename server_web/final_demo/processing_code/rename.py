import os

folderName = 'diag'

path = "./"+folderName+"/"

cnt=0
for filename in os.listdir(path):
    os.rename(path+filename, path+folderName+'_'+str(cnt)+'.jpg')
    cnt=cnt+1

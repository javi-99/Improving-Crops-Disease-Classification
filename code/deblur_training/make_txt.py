import os
import glob
#path="/media/asim/F4A0F597A0F56092/MRIDATA/brain/Brain_resized/*.png"  
##dirList=os.listdir(path)
#fff=[]
#with open("celebA_train.txt", "w") as f:
#    for i,filename in enumerate(glob.glob(path)):
##        if i<60000:
#            fff.append(filename)
#            f.write(filename+"\n")
#        else:
#            break
#
#files = [l.strip() for l in open("celebA_train.txt").readlines()]
#print(len(files))
#if type("celebA_train.txt") is list:
#    print("list")
#
##
#path="/media/asim/F4A0F597A0F56092/MRIDATA/brain/Brain_resized_val/*.png"
##dirList=os.listdir(path)
#fff=[]
#with open("celebA_dev.txt", "w") as f:
#    for i,filename in enumerate(glob.glob(path)):
#        if i<1000:
#            fff.append(filename)
#            f.write(filename+"\n")
#        else:
#            break
#
#files = [l.strip() for l in open("celebA_dev.txt").readlines()]
#print(len(files))
#if type("celebA_dev.txt") is list:
#    print("list")
#
def make_paths(input_path,out_path):

    fff=[]
    with open(out_path, "w") as f:
        for i,filename in enumerate(glob.glob(input_path)):
            fff.append(filename)
            f.write(filename+"\n")
# files = [l.strip() for l in open("kernels_train1.txt").readlines()]
# print(len(files))
# if type("train_data.txt") is list:
#     print("list")
#
def kernels():
    path = "/media/fahad/54E6D820E6D80460/javed/agriculture/deblur_iclr_data/blur_kernels/*.png"
    #dirList=os.listdir(path)
    fff=[]
    with open("data/kernels_train.txt", "w") as f:
        for i,filename in enumerate(glob.glob(path)):
            # if i<1000:
            fff.append(filename)
            f.write(filename+"\n")
        # else:
#             break
# #
#files = [l.strip() for l in open("kernels_dev.txt").readlines()]
#print(len(files))
#if type("kernels_dev.txt") is list:
#    print("list")
if __name__=="__main__":
    out_path="/media/fahad/54E6D820E6D80460/javed/agriculture/deblur_iclr_data/server/data/data_train.txt"
    in_path="/media/fahad/54E6D820E6D80460/javed/agriculture/deblur_iclr_data/iclr_challenge/*"  
    make_paths(in_path,out_path)
    kernels()

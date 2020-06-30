import os
from PIL import Image
import os.path
import glob
import subprocess
import sys
import time

#!!!当前文件的路径
pwd = os.getcwd()
#!!!修改样本前缀
posPrefix='posx'
negPrefix='negx'
#!!!正负样本图片格式
imgformat='jpg'
#imgformat='png'
#!!!调整后正负样本大小
poswidth=40
posheight=40
negwidth=1080
negheight=1440
#预删除冲突文件
filename1 = pwd+'/bin/traincascade.txt'
filename2=pwd+'/bin/pos.txt'
filename3=pwd+'/bin/pos.vec'
filename4=pwd+'/bin/neg.txt'
filename5=pwd+'/bin/neg.vec'
filename6=pwd+'/bin/negx.txt'
filename7=pwd+'/bin/posx.txt'
if os.path.exists(filename1):
  os.remove(filename1)
if os.path.exists(filename2):
  os.remove(filename2)
if os.path.exists(filename3):
  os.remove(filename3)
if os.path.exists(filename4):
  os.remove(filename4)
if os.path.exists(filename5):
  os.remove(filename5)
if os.path.exists(filename6):
  os.remove(filename6)
if os.path.exists(filename7):
  os.remove(filename7)
#批量修改正样本名字
filepath = pwd+"/bin/posdata"
print("start pos")
if not os.path.exists(filepath):
    print("目录不存在!!")
    os._exit(1)
filenames = os.listdir(filepath)
i=1
for data in filenames:
    newname = posPrefix+str(i)+'.'+imgformat
    i=i+1
    print(newname)
    os.rename(filepath + '//' + data,filepath + '//' + newname)
#批量修改负样本名字
filepath = pwd+"/bin/negdata"

print("start neg")
if not os.path.exists(filepath):
    print("目录不存在!!")
    os._exit(1)
filenames = os.listdir(filepath)
i=1
for data in filenames:
    newname = negPrefix+str(i)+'.'+imgformat
    i=i+1
    print(newname)
    os.rename(filepath + '//' + data,filepath + '//' + newname)
#批量修改jpg正样本大小
def convertjpg(jpgfile,outdir,poswidth,posheight):
    img=Image.open(jpgfile)
    try:
        new_img=img.resize((poswidth,posheight),Image.BILINEAR)   
        new_img.save(os.path.join(outdir,os.path.basename(jpgfile)))
    except Exception as e:
        print(e)
for jpgfile in glob.glob(pwd+"/bin/posdata//*."+imgformat):
    convertjpg(jpgfile,pwd+"/bin/posdata",poswidth,posheight)
#批量修改jpg负样本大小
def convertjpg(jpgfile,outdir,negwidth,negheight):
    img=Image.open(jpgfile)
    try:
        new_img=img.resize((negwidth,negheight),Image.BILINEAR)   
        new_img.save(os.path.join(outdir,os.path.basename(jpgfile)))
    except Exception as e:
        print(e)
for jpgfile in glob.glob(pwd+"/bin/negdata//*."+imgformat):
    convertjpg(jpgfile,pwd+"/bin/negdata",negwidth,negheight)
print('修改大小成功')
#生成正负样本描述文件
child = subprocess.Popen(pwd+'/bin/pos_'+imgformat+'.bat',shell=False)
child = subprocess.Popen(pwd+'/bin/neg_'+imgformat+'.bat',shell=False)
print('生成描述文件成功')
#修改正负样本描述文件
time.sleep(1)
    # 打开旧文件
f = open(pwd+'/bin/pos.txt','r')

    # 打开新文件
f_new = open(pwd+'/bin/posx.txt','w')


# 循环读取旧文件
for line in f:
    # 进行判断
    if imgformat in line:
        line = line.replace(imgformat,imgformat+' 1 0 0 '+str(poswidth)+' '+str(posheight))
    # 如果不符合就正常的将文件中的内容读取并且输出到新文件中
    f_new.write(line)

f.close()
f_new.close()
    # 打开旧文件
f = open(pwd+'/bin/neg.txt','r')

    # 打开新文件
f_new = open(pwd+'/bin/negx.txt','w')


    # 循环读取旧文件
for line in f:
    # 进行判断
    if imgformat in line:
        line = line.replace(imgformat,imgformat+' 1 0 0 '+str(poswidth)+' '+str(posheight))
    # 如果不符合就正常的将文件中的内容读取并且输出到新文件中
    f_new.write(line)

f.close()
f_new.close()
print('修改描述文件成功')
#生成正样本vec文件
DIR = pwd+'/bin/posdata' #要统计的文件夹
a=len([name for name in os.listdir(DIR) if os.path.isfile(os.path.join(DIR, name))])
print("正样本总数："+str(a))
cmd = "cd bin&opencv_createsamples.exe -vec pos.vec -info posx.txt -num "+str(a)+" -w "+str(poswidth)+" -h "+str(posheight)
p = subprocess.Popen(cmd, shell=True)
p.wait()
#生成负样本vec文件
DIR = pwd+'/bin/negdata' #要统计的文件夹
b=len([name for name in os.listdir(DIR) if os.path.isfile(os.path.join(DIR, name))])
print("负样本总数："+str(b))
cmd = "cd bin&opencv_createsamples.exe -vec neg.vec -info negx.txt -num "+str(b)+" -w "+str(negwidth)+" -h "+str(negheight)
p = subprocess.Popen(cmd, shell=True)
print('生成vec成功')
#开始训练
    # 打开新文件
file = open(pwd+'/bin/traincascade.txt','w')
cmd = "cd bin\n opencv_traincascade.exe -data xml -vec pos.vec -bg neg.txt -numPos "+str(int(a*0.85))+" -numNeg "+str(b)+" -numStages 20 -w "+str(poswidth)+" -h "+str(posheight)+" -mode ALL\n\npause"
file.write(cmd)
file.close()
    #改成bat文件
filepath = pwd+"/bin"
print("修改bat")
if not os.path.exists(filepath):
    print("目录不存在!!")
    os._exit(1)
newname = 'traincascade.bat'
print(newname)
os.rename(filepath + '//' + 'traincascade.txt',filepath + '//' + newname)
hild = subprocess.Popen(pwd+'/bin/traincascade.bat',shell=False)

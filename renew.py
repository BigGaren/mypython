
import os
import sys
import shutil

linux_path=r"/"
source_path=input("输入需要复制的文件或文件夹: ")

if source_path==1:
    pass
elif source_path==2:
    pass
else:
    if len(source_path)<3:
        print("你有点短啊？")
        sys.exit()

# 判断是否是linux路径,如果是，则转化为windows路径，因为python不能识别
if linux_path in source_path:
    print("路径是linux路径")
    # 切割首字符/
    source_path=source_path[1:] 
    # print("linux路径被切为: "+source_path)
    source_path=source_path.replace('/',':\\',1)
    source_path=source_path.replace("/","\\")

print("你输入的文件是: "+source_path)

# sys.exit()

isExist=os.path.exists(source_path)
print("文件是否存在: "+str(isExist))
if isExist==False:
    print("文件不存在")
    sys.exit()


is_file=True
if os.path.isfile(source_path):
    is_file=True
elif os.path.isdir(source_path):
    is_file=False
else :
    print("你输入的什么玩意！")
    sys.exit()

print("这是文件吗 :"+str(is_file))

def cmd_copy(source_path,des_path):
    os.system("cp -rf "+source_path+" "+des_path)

tmp_path=str(source_path)+"_tmp"
if(os.path.exists(tmp_path)):
    if(os.path.isfile(tmp_path)):
        result=os.remove(tmp_path)
        print("tmp is exist , remove now ,result: "+str(result))
    else:
        result=shutil.rmtree(tmp_path)
        print("tmp is exist , remove now ,result: "+str(result))

if is_file:
    # shutil.copy(source_path,tmp_path)
    cmd_copy(source_path,tmp_path)
else:
    # shutil.copytree(source_path,tmp_path)
    cmd_copy(source_path,tmp_path)

if os.path.exists(tmp_path):
    print("复制成功 !")
else :
    print("复制失败!")
    sys.exit()

result=False
if is_file:
    result=os.remove(source_path)
else:
    result=shutil.rmtree(source_path)

print("删除源文件: "+str(result))

# result=os.replace(tmp_path,source_path)
# result=shutil.move(tmp_path,source_path)
# 需要使用cmd命令去执行这种特殊操作，如复制等，不然python会去读取被操作的文件，导致加密系统发现该文件
os.system("mv "+tmp_path+" "+source_path)
print("重命名tmp文件: "+str(result))



input("\n\n按任意键退出\n")

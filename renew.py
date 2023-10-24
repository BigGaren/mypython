
import os
import sys
import shutil

import my_file

VSCODE_PATH=r"D:\software\Microsoft VS Code"
VSCODE_CONFIG_PATH=r"C:\Users\0\.vscode"

print("输入1:去加密vscode")
print("输入2:去加密vscode配置")
source_path=input("输入去加密的文件或文件夹: ")

if source_path=="1":
    source_path=VSCODE_PATH
elif source_path=="2":
    source_path=VSCODE_CONFIG_PATH
else:
    if len(source_path)<3:
        input("\n 输入数据过短 \n")
        sys.exit()

# 检查输入的文件路径问题
source_path=my_file.check_input_file_name(source_path)

is_file=True
if os.path.isfile(source_path):
    is_file=True
elif os.path.isdir(source_path):
    is_file=False
else :
    input("\n\n 无法识别文件类型 \n")
    sys.exit()

print("这是文件吗 :"+str(is_file))

def cmd_copy(source_path,des_path):
    from my_file import add_separate_at_blank_space
    source_path=add_separate_at_blank_space(source_path)
    des_path=add_separate_at_blank_space(des_path)

    os.system("cp -rf "+source_path+" "+des_path)

def cmd_mv(source_path,des_path):
    from my_file import add_separate_at_blank_space
    source_path=add_separate_at_blank_space(source_path)
    des_path=add_separate_at_blank_space(des_path)

    os.system("mv "+source_path+" "+des_path)

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
    input(" 复制失败!")
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
cmd_mv(tmp_path,source_path)

print("重命名tmp文件: "+str(result))



input("\n\n按任意键退出\n")

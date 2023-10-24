
# 这里主要是为了实现自己的函数
import os
import sys

def check_input_file_name(source_path):
    linux_path=r"/"
    
    # 判断是否是linux路径,如果是，则转化为windows路径，因为python不能识别
    if linux_path in source_path:
        print("路径是linux路径")
        # 切割首字符/
        source_path=source_path[1:] 
        # print("linux路径被切为: "+source_path)
        source_path=source_path.replace('/',':\\',1)
        source_path=source_path.replace("/","\\")

    print("你输入的文件是: "+source_path)

    isExist=os.path.exists(source_path)
    print("文件是否存在: "+str(isExist))
    if isExist==False:
        print("文件不存在")
        input("按下继续")
        sys.exit()

    return source_path


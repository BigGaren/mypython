
# 这里主要是为了实现自己的函数
import os
import sys

def check_input_file_name(source_path):
    linux_path=r"/"
    null_path=r" "
    quotation_mark="\""
    Single_quotation_mark="\'"
    
    print("原路径:"+source_path)

    # 判断是否是linux路径,如果是，则转化为windows路径，因为python不能识别
    if linux_path in source_path:
        print("路径是linux路径")
        # 切割首字符/
        source_path=source_path[1:] 
        # print("linux路径被切为: "+source_path)
        source_path=source_path.replace('/',':\\',1)
        source_path=source_path.replace("/","\\")
    
    if null_path in source_path : 
        
        if quotation_mark in source_path :
            print("带空格 且带引号")
            source_path=source_path.replace(quotation_mark,"")
            print("处理路径后:"+source_path)
        elif Single_quotation_mark in source_path:
            print("带空格 且带单引号")
            source_path=source_path.replace(Single_quotation_mark,"")
            print("处理路径后:"+source_path)
        # 都没有引号！
        else:
            print("路径带空格 且不带引号")
            # source_path=add_separate_at_blank_space(source_path)
            # path=os.path.join(source_path)
            # print("path:"+source_path)


    print("你输入的文件是: "+source_path)

    isExist=os.path.exists(source_path)
    print("文件是否存在: "+str(isExist))
    if isExist==False:
        print("文件不存在")
        input("按下继续")
        sys.exit()

    return source_path

def add_separate_at_blank_space(source_path):
    if ' ' in source_path:
        source_path='\''+source_path+'\''
    return source_path
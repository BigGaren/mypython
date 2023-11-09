
import sys
import os
import my_file

print("默认提取转换出来的数据都存放在当前脚本路径下的A.txt!!!\n")
print("输入1:默认当前py脚本路径下的A.CSV")
print("输入2:默认桌面路径下的A.CSV")
source_path=input("或者输入需要提取的csv文件: ")

if source_path=="1":
    source_path=r".\A.CSV"
elif source_path=="2":
    source_path = os.path.join(os.path.expanduser("~"), "Desktop")+"\\A.CSV"
else:
    if len(source_path)<3:
        input("输入的文件长度过短!")
        sys.exit()

source_path=my_file.check_input_file_name(source_path)


csv_filename=source_path
# 把提取出来的数据存在哪里
write_filename=r".\test.txt"
csv_head="Timestamp,Mode,Action,VC,DT,WC,DCS,D0,D1,D2,D3,D4,D5,D6,D7,ECC,CRC,Transaction Type,STOP\n"
enable_high_speed=True
enable_BTA_speed=True
# tab_idex=[]
csv_list=[]
first_line=[]
with open(csv_filename,"r") as f:
    # 读取信息头
    line=f.readline()
    print("first line:"+line)
    if line=="" :
        print("读取的文件没有任何信息")
        exit()
    # elif line.strip()!= csv_head.strip() :
    elif line != csv_head :
        print("文件头不对:"+line)
        print("line:"+str(type(line))+" head:"+str(type(csv_head)))
        exit()
    first_line=line

    # 读取每一行信息
    while True :
        line=f.readline()
        if line=="" :
            break

        # 切割出每一行的关键字
        split_string=line.split('"')
        if(split_string=="") :
            print("读取csv数据时候出错,出现空")
            sys.exit()
        # print("split_string:"+str(split_string[7:15]))
        # 数据是以"为分割，""中间的数据要提取出来，所以是1::2是从第"1"个下标开始提取，隔开2个"中间的数据是需要的
        # ="15:15:05.402.616.820 (Apr-15-2022)",="LP_ESC",="LPDT",="00",="DCS Long Write/write_LUT Command Packet (39)",\
        # ="0003",=" ",="9F",="A5",="A5",=" ",=" ",=" ",=" ",=" ",="09",="D96D",="Host processor to peripheral",="Mark-1",
        split_string=split_string[1::2]
        
        csv_list.append(split_string)
        # print("split:"+str(csv_list[-1]))


# 以下开始提取数据！处理数据！组合数据！
# 提取数据采用列表下标法
#Timestamp,Mode,Action,VC,DT,WC,DCS,D0,D1,D2,D3,D4,D5,D6,D7,ECC,CRC,Transaction Type,STOP
Timestamp_index=0
Mode_index=1
Action_index=2
VC_index=3
DT_index=4
WC_index=5
DCS_index=6
DATA_index=7
ECC_index=15
CRC_index=16
Trans_Type_index=17
STOP_index=18


# 不同的数据占的长度不一样
_87_length=1
DT_length=1
WC_length=2
ECC_length=1
DATA_length=8
CRC_length=2
_87_data="87"

DT_list=[""]

# need_data_index=[DT_index,WC_index,ECC_index,CRC_index,Mode_index,DATA_index]
combination_list=[]
for list in csv_list:
    DT=list[DT_index]
    DT_string=""
    WC=list[WC_index]
    ECC=list[ECC_index]
    CRC=list[CRC_index]
    Mode=list[Mode_index]
    Action=list[Action_index]

    DATA=list[DATA_index:DATA_index+8]
    # 去掉空元素
    DATA = [x for x in DATA if x.strip()]

    combination_data=[]

    DATA_length=len(DATA)
    # print("data_length:"+str(len(DATA)))

    # print("source dt:"+DT)
    if DT==" ":
        # print("fff DT:"+DT)
        pass
    else:
        # 把()里的dt提取出来
        DT=DT.split("(")
        # print("DT:"+DT[1])
        DT_string=DT[0]
        DT=DT[1].split(")")
        DT=DT[0]
        # print("DT:"+str(DT))
        # break

    if WC=="":
        pass
    else:
        # 比如"0004"就是04 00
        WC1=WC[0:2]
        WC2=WC[2:]
        WC=[WC2,WC1]
        # print("WC:"+str(WC))

    if CRC==" ":
        pass
    else:
        CRC1=CRC[0:2]
        CRC2=CRC[2:]
        CRC=[CRC2,CRC1]
    # print("CRC:"+str(CRC))

    # 不同数据格式，长度是不一样的，懂吗弟弟
    data_total=0
    if DT =="05":
        data_total=_87_length+DT_length+DATA_length+ECC_length
        data_total=hex(data_total)
        data_total=(data_total.split("0x"))[1].upper()

        combination_data.append(str(data_total))
        combination_data.append(_87_data)
        combination_data.append(DT)
        for num in range(2):
            combination_data.append(DATA[num])
        # print("combin:"+str(combination_data))

        if ECC !=" ":
            combination_data.append(ECC)

    elif DT=="15":
        data_total=_87_length+DT_length+DATA_length+ECC_length
        data_total=hex(data_total)
        data_total=(data_total.split("0x"))[1].upper()

        combination_data.append(str(data_total))
        combination_data.append(_87_data)
        combination_data.append(DT)
        for num in range(2):
            combination_data.append(DATA[num])

        if ECC !=" ":
            combination_data.append(ECC)

    elif DT=="39":
        data_total=_87_length+DT_length+WC_length+ECC_length+DATA_length+CRC_length
        data_total=hex(data_total)
        data_total=(data_total.split("0x"))[1].upper()

        combination_data.append(str(data_total))
        combination_data.append(_87_data)
        combination_data.append(DT)

        for tmp in WC:
            combination_data.append(tmp)
        
        if ECC !=" ":
            combination_data.append(ECC)

        for num in range(DATA_length):
            combination_data.append(DATA[num])

        # crc有可能为空，是中间那行
        if CRC!=" ":
            for tmp in CRC:
                combination_data.append(tmp)
    # DCS Short READ Response, 1 byte returned
    elif DT=="21":
        continue
    # Generic Short WRITE, 2 parameters (23)
    elif DT=="23":
        continue
    # Generic Long Write (29)
    elif DT=="29":
        continue
    # 主机无参数读取从机数据，不用理会
    elif DT=="06":
        continue
    # 从机返回错误的信息，不理会
    elif DT=="02":
        continue
    # 主机请求读一个字节 Generic READ, 1 parameter (14)
    elif DT=="14":
        continue
    # 从机返回一个字节 Generic Short READ Response, 1 byte returned (11)
    elif DT=="11":
        continue
    # 主机设置最大返回包数
    elif DT_string=="Set Maximum Return Packet Size ":
        continue
    # 好像也是无用的意思
    elif Action=="ULPS":
        continue

    # 长包的尾包
    elif Mode==" " and \
        DT==" " :
        
        for num in range(DATA_length):
            combination_data.append(DATA[num])
        # 进入这里，且crc不空，才能把crc写进去
        if CRC!=" ":
            for tmp in CRC:
                combination_data.append(tmp)

        list_tmp=combination_list[-1]
        list_tmp+=combination_data

        # print("list_tmp0:"+list_tmp[0])
        list_tmp[0]=hex(int(list_tmp[0],16)+DATA_length)
        # print("a list_tmp0:"+list_tmp[0])
        list_tmp[0]=((list_tmp[0]).split("0x"))[1].upper()
        combination_data=list_tmp
        # 因为要把多行的超大一组数据拼接起来，所以要删掉最后一个，后面再更新它
        combination_list.pop()
        # print("list_tmp:"+str(list_tmp))
        # print("combination_list:"+str(combination_list[-1]))
        
       
    elif Mode=="HS" :
        print("Mode:"+Mode+" \n\n\n")
        # continue
        if enable_high_speed:
            continue
        else:
            break
    elif Mode=="LP_BTA":
        print("Mode:"+Mode+" \n\n\n")
        if enable_BTA_speed:
            continue
        else:
            break
    else :
        print("Mode:"+Mode+" -DT:"+DT+" -WC:"+str(WC))
        
        print("你这DT 数据格式不对，问题很大，好好查查什么情况")
        sys.exit()

    print("combination_data:"+str(combination_data),end="\n\n")
    combination_list.append(combination_data)
    tmp_combination_data=combination_data



"""
# 提取数据采用字典法
def get_list_form_tuple(need_list,tuple_list):
    target_list=[]
    for tuple in tuple_list:
        tmp_list=[]
        for list in need_list:
            tmp_list.append(tuple[list])
        target_list.append(tmp_list)
    return target_list

# 从提取的第一行数据里，去掉换行符，里面有所有的数据格式
first_line=first_line.replace("\n","")
first_line=first_line.replace("\r\n","")
# 把总数据头拆分成列表，以便组成字典
tmp_list=first_line.split(",")
head_data_index=tmp_list

# 需要的数据头
need_data_list=['DT', 'WC', 'ECC', 'D0', 'D1', 'D2', 'D3', 'D4', 'D5', 'D6', 'D7', 'CRC']
# print("need:"+str(need_data_list))

vaild_tuple_list=[]

# 从有效数据里组合成字典
for list in csv_list:
    tmp_zip=zip(head_data_index,list)
    tmp_tuple=dict(tmp_zip)
    vaild_tuple_list.append(tmp_tuple)

# # 从字典里提取出的需要的列表
# target_tuple_list=get_list_form_tuple(need_data_list,vaild_tuple_list)
# print("target list:"+str(target_tuple_list))



combination_list=[]
# 不同的数据占的长度不一样
_87_length=1
DT_length=1
WC_length=2
ECC_length=1
DATA_length=8
CRC_length=2
_87_data="87"
# 从 csv_head头+有效数据列表 组成的有效字典里 一个个处理数据
for tuple in vaild_tuple_list :
    DATA_length=8

    DT=tuple["DT"]
    WC=tuple["WC"]
    ECC=tuple["ECC"]
    CRC=tuple["CRC"]
    Mode=tuple["Mode"]
    # print("DT:"+DT)

    D8_list=[]
    for num in range(8):
        index_tmp="D"+str(num)
        data_tmp=tuple[index_tmp]
        if(data_tmp!=" "):
            D8_list.append(data_tmp)
    print("D8_list:"+str(D8_list))
    DATA=D8_list

    combination_data=[]

    DATA_length=len(DATA)
    print("data_length:"+str(len(DATA)))

    # print("source dt:"+DT)
    if DT==" ":
        # print("fff DT:"+DT)
        pass
    else:
        # 把()里的dt提取出来
        DT=DT.split("(")
        # print("DT:"+DT[1])
        DT=DT[1].split(")")
        DT=DT[0]
        print("DT:"+str(DT))
        # break

    if WC=="":
        pass
    else:
        # 比如"0004"就是04 00
        WC1=WC[0:2]
        WC2=WC[2:]
        WC=[WC2,WC1]
        print("WC:"+str(WC))

    if CRC==" ":
        pass
    else:
        CRC1=CRC[0:2]
        CRC2=CRC[2:]
        CRC=[CRC2,CRC1]
    print("CRC:"+str(CRC))

    # 不同数据格式，长度是不一样的，懂吗弟弟
    data_total=0
    if DT =="05":
        data_total=_87_length+DT_length+DATA_length+ECC_length
        data_total=hex(data_total)
        data_total=(data_total.split("0x"))[1].upper()

        combination_data.append(str(data_total))
        combination_data.append(_87_data)
        combination_data.append(DT)
        for num in range(2):
            combination_data.append(DATA[num])
        # print("combin:"+str(combination_data))

        if ECC !=" ":
            combination_data.append(ECC)

    elif DT=="15":
        data_total=_87_length+DT_length+DATA_length+ECC_length
        data_total=hex(data_total)
        data_total=(data_total.split("0x"))[1].upper()

        combination_data.append(str(data_total))
        combination_data.append(_87_data)
        combination_data.append(DT)
        for num in range(2):
            combination_data.append(DATA[num])

        if ECC !=" ":
            combination_data.append(ECC)

    elif DT=="39":
        data_total=_87_length+DT_length+WC_length+ECC_length+DATA_length+CRC_length
        data_total=hex(data_total)
        data_total=(data_total.split("0x"))[1].upper()

        combination_data.append(str(data_total))
        combination_data.append(_87_data)
        combination_data.append(DT)

        for tmp in WC:
            combination_data.append(tmp)
        
        if ECC !=" ":
            combination_data.append(ECC)

        for num in range(DATA_length):
            combination_data.append(DATA[num])

        # crc有可能为空，是中间那行
        if CRC!=" ":
            for tmp in CRC:
                combination_data.append(tmp)
        
    # 长包的尾包
    elif Mode==" " and \
        DT==" " :
        
        for num in range(DATA_length):
            combination_data.append(DATA[num])
        # 进入这里，且crc不空，才能把crc写进去
        if CRC!=" ":
            for tmp in CRC:
                combination_data.append(tmp)

        list_tmp=combination_list[-1]
        list_tmp+=combination_data

        print("list_tmp0:"+list_tmp[0])
        list_tmp[0]=hex(int(list_tmp[0],16)+DATA_length)
        print("a list_tmp0:"+list_tmp[0])
        list_tmp[0]=((list_tmp[0]).split("0x"))[1].upper()
        combination_data=list_tmp
        # 因为要把多行的超大一组数据拼接起来，所以要删掉最后一个，后面再更新它
        combination_list.pop()
        print("list_tmp:"+str(list_tmp))
        print("combination_list:"+str(combination_list[-1]))
        
        # if CRC!=" ":
        #     combination_list.append(combination_data)
        #     print("com:"+str(combination_list))
        #     sys.exit()
    elif Mode=="HS" :
        print("Mode:"+Mode+" \n\n\n")
        # continue
        break
    elif Mode=="LP_BTA":
        print("Mode:"+Mode+" \n\n\n")
        break
    else :
        print("Mode:"+Mode+"-DT:"+DT+"-WC:"+str(WC))
        
        print("你这DT 数据格式不对，问题很大，好好查查什么情况")
        sys.exit()

    print("combination_data:"+str(combination_data),end="\n\n")
    combination_list.append(combination_data)
    

# print("com:"+str(combination_list))
# input("key")
# sys.exit(0)

"""

# 把提取出来的数据加上0x,首个代表长度的字节如果只有比如0xA,那改成0x0A
add_0x_list=[]
for list in combination_list:

    if len(list[0])==1:
        list[0]="0"+list[0]

    tmp_list=[]
    for data in list:
        tmp_list.append("0x"+data)
    add_0x_list.append(tmp_list)


with open(write_filename,"w+") as f:
    
    for list in add_0x_list:
        isFirst=True
        for num in list:
            if(isFirst):
                f.write(num)
                isFirst=False
            else:
                f.write(",")
                f.write(num)
        else:
            f.write(",\n")
        


# 暂停
input("\n\n 请按enter键继续...")
print("继续执行")
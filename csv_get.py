
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
# 是否需要bta数据
need_BTA_data=True
# 是否需要主机发送给从机的初始化数据
need_host_data=True
# 当主机发送11 00 , 29 00给从机，以开启屏幕后，是否直接结束提取数据
exit_when_2911=False


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

Trans_Type_Host="Host processor to peripheral"
Trans_Type_Peripheral="Peripheral to host processor"
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

# 把csv上的一行数据，改变成mcu发送出去的数据格式
def csv_data_to_mcu(list):

    DT=list[DT_index]
    WC=list[WC_index]
    ECC=list[ECC_index]
    CRC=list[CRC_index]
    DATA=list[DATA_index]
    Transfer_type=list[Trans_Type_index]

    DATA_length=len(DATA)
    tmp_list=[]
    # print("csv_data_to_mcu list:"+str(list))

    if DATA_length<=2 and DATA_length>=0 and DT!="39":
        data_total=_87_length+DT_length+DATA_length+ECC_length
        data_total=hex(data_total)
        data_total=(data_total.split("0x"))[1].upper()

        tmp_list.append(str(data_total))
        tmp_list.append(_87_data)
        tmp_list.append(DT)
        for num in range(DATA_length):
            tmp_list.append(DATA[num])

        if ECC !=" ":
            tmp_list.append(ECC)
        
    
    else:
        data_total=_87_length+DT_length+WC_length+ECC_length+DATA_length+CRC_length
        data_total=hex(data_total)
        data_total=(data_total.split("0x"))[1].upper()

        tmp_list.append(str(data_total))
        tmp_list.append(_87_data)
        tmp_list.append(DT)

        for tmp in WC:
            tmp_list.append(tmp)
        
        if ECC !=" ":
            tmp_list.append(ECC)

        for num in range(DATA_length):
            tmp_list.append(DATA[num])

        # crc有可能为空，是中间那行
        if CRC!=" ":
            for tmp in CRC:
                tmp_list.append(tmp)
    # print("tmp_list:"+str(tmp_list))
    return tmp_list

host_to_Peripheral_list=["03","13","23","04","14","24","05","15","06","13","29","39"]
Peripheral_to_host_list=["11","12","1A","1C","21","22"]
BTA_list=[]
BTA_host_list=[]

BTA_status="end"
# need_data_index=[DT_index,WC_index,ECC_index,CRC_index,Mode_index,DATA_index]
combination_list=[]
tmp_combination_data=[]
tmp_list=[]
for list in csv_list:
    DT=list[DT_index]
    DT_string=""
    WC=list[WC_index]
    ECC=list[ECC_index]
    CRC=list[CRC_index]
    Mode=list[Mode_index]
    Action=list[Action_index]
    Transfer_type=list[Trans_Type_index]

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
    list[DATA_index]=DATA
    list[CRC_index]=CRC
    list[WC_index]=WC
    list[DT_index]=DT

    if exit_when_2911:
        if DT=="15" and DATA[0]=="11" and DATA[1]=="00" :
            print("开屏！")
            break

    # 数据方向是从机发往主机
    if Transfer_type==Trans_Type_Peripheral:
        if  DT in Peripheral_to_host_list:
            if BTA_status=="start":
                BTA_status="processing"
            else:
                input("bta not good status!! "+"status:"+BTA_status+" \n\n")
                sys.exit()

            bta_tmp_data=csv_data_to_mcu(list)
            
            BTA_list.append(bta_tmp_data)
            # print("bta:"+str(BTA_list))
            # 上一个是高速信号，那么这里抓取不到
            if storage_last_list[Mode_index]!="HS":
                BTA_host_list.append(tmp_combination_data)
            else:
                # print("上一个是hs")
                string="HS"
                BTA_host_list.append((string))
            # print("tmp_combination_data:"+str(tmp_combination_data))
        else :
            print("从机返回的数据DT!!!:"+DT)
    else:
        # 不同数据格式，长度是不一样的，懂吗弟弟
        if DT in host_to_Peripheral_list:
            combination_data=csv_data_to_mcu(list)
        
        elif DT=="37":
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

            # 修改数据的第一个代表总长度的字节
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
            tmp_list=list
            continue
        elif Mode=="LP_BTA":
            # print("Mode:"+Mode)
            if BTA_status=="end":
                BTA_status="start"
                storage_last_list=tmp_list
                # print("storage:"+str(storage_last_list))
            elif BTA_status=="processing":
                BTA_status="end"
                storage_last_list=[]
            else:
                input("BTA start error!!! "+"bta status:"+BTA_status)
                sys.exit()
            continue
        elif DT_string=="Acknowledge and Error Report ":
            print("从机返回数据失败！")
            continue
        else :
            print("Mode:"+Mode+" -DT:"+DT+" -WC:"+str(WC))
            
            print("你这DT 数据格式不对，问题很大，好好查查什么情况")
            continue
            # sys.exit()

        # print("combination_data:"+str(combination_data),end="\n\n")
        combination_list.append(combination_data)
        tmp_combination_data=combination_data
        tmp_list=list
    
# 把列表都加上0x
def list_add_0x(source_list):
    add_0x_list=[]
    if len(source_list)<=0:
        print("source list has not data!")
        sys.exit()
        # return add_0x_list
    
    for list in source_list:
        if len(list)<=0:
            print("list has not data!")
            # print("source list:"+str(source_list))
            sys.exit()
            # return add_0x_list
        
        if list=="HS":
            add_0x_list.append(list)
            continue
        if len(list[0])==1:
            list[0]="0"+list[0]

        tmp_list=[]
        for data in list:
            tmp_list.append("0x"+data)
        add_0x_list.append(tmp_list)
    return add_0x_list

if need_BTA_data:
    BTA_list=list_add_0x(BTA_list)
    BTA_host_list=list_add_0x(BTA_host_list)

if need_host_data:
    combination_list=list_add_0x(combination_list)

def list_to_mcu_string(list):
    isFirst=True
    target_string=""

    if list=="HS":
        return list+"\n"

    for data in list:
        if(isFirst):
            target_string+=data
            isFirst=False
        else:
            target_string+=","
            target_string+=data
    else:
        target_string+=",\n"
    # print("string:"+target_string)
    return target_string

with open(write_filename,"w+", encoding =" UTF -8") as f:

    if need_BTA_data:
        f.write("bta数据: \n")
        for list in BTA_list:
            string=list_to_mcu_string(list)
            f.write(string)
        f.write("\n\n")

        if len(BTA_host_list)== len(BTA_list):
            len=len(BTA_host_list)
            for num in range(len):
                f.write("host: \n")
                string=list_to_mcu_string(BTA_host_list[num])
                f.write(string)

                f.write("peripheral: \n")
                string=list_to_mcu_string(BTA_list[num])
                f.write(string)
                f.write("\n")
                
        else:
            print("bta 与主机的数据数量不一样！")
    
    
    if need_host_data:
        f.write("主机发往从机的初始化数据:\n")
        for list in combination_list:
            string=list_to_mcu_string(list)
            f.write(string)
        f.write("\n")

print("成功！")
# 暂停
input("\n\n 请按enter键继续...")
print("继续执行")
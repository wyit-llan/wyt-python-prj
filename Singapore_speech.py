import pandas as pd
from sqlalchemy import create_engine, text
import os
from fpdf import FPDF
from PIL import Image
from datetime import datetime
from RunSql import RunSql
import csv
import ast
from google_translate import google_translate
from itertools import islice

# engine_crawl = create_engine('mysql+pymysql://report:x3m0u8X#M)U*@dltrade308.mysql.rds.aliyuncs.com:3306/report_crawl')
# engine_report=create_engine('mysql+pymysql://report:x3m0u8X#M)U*@am-wz9px62t6t2c32dv3131930o.ads.aliyuncs.com:3306/report')
yy_mm=datetime.now().strftime("%Y-%m")
full_base_path="F:/www/full/pdf/20/" + yy_mm + "/"
part_base_path="D:/www/index/partFile/20/" + yy_mm + "/"
def insert_report_label_dict_12():
    name_ori="Ministry Of Finance"
    name=google_translate(name_ori,"zh-CN")
    name_en=name_ori
    query1=f"INSERT INTO report_label_dict_12 (name, pid, stage, name_en,name_ori, areaId) VALUES (\'{name}\', -1,2,\'{name_en}\', \'{name_ori}\', 702)"
    query2=f"INSERT INTO report_label_dict_12 (name, pid, stage, name_en,name_ori, areaId) VALUES ('不知道', 4, 2,'不知道', \'{name_ori}\', 702)"
    query3=f"INSERT INTO report_label_dict_12 (name, pid, stage, name_en,name_ori, areaId) VALUES ('程序', -1, 1,'Program', 'Program', 702)"
    #  try:
    #     with engine_crawl() as conn:
    #             conn.execute(query1)
    #  except Exception as e:
    #      print(f"Failed to update ")
    RunSql(query1,None,False,1)
    print(query1)
 
def main():
    base_path="D:/full/pdf/12/702/2024-12/"
    with open("C:/Users/wtt/Desktop/Singapore_finance_ministry_public-consultations.csv", mode='r', encoding='utf-8') as file:
        reader = csv.reader(file)  # 创建 CSV 阅读器
        cnt=0
        repeat=0
        file_dict={}
        # for row in islice(reader, 0, None):
        #     cnt+=1
        #     print(cnt)
        #     if(cnt==2): print(row)
        classify=0
        for row in reader:
            if(len(row)<1):continue
            cnt+=1
            if(row[0]!="Title" and cnt>4):    #跳过字段行
            # #if(cnt==3):
                #print(reformat_date(row[1]))
                #r_department=row[2].replace('_', ' ')
                r_department="Ministry Of Finance"
                #r_type=row[3].replace('_', ' ')
                r_type="Public Consultations"
                title=row[0].replace('"', '\\"')
                time=''
                if (row[1]!="xx-xx-xx") :
                    time=reformat_date(row[1])
                country=702
                
                if(classify==0):
                    classify= find_classify(r_type,r_department)
                path_list=[]
                file_url=''
                if(len(row)==5):
                    if row[4] in file_dict.keys():
                        print("rp" + row[4])
                        repeat+=1
                        continue
                    path_list.append(row[4]) 
                    file_dict[row[4]]=1
                else:
                    if row[5] in file_dict.keys():
                        print("rp" + row[5])
                        repeat+=1
                        continue
                    path_list.append(row[5])
                    file_dict[row[5]]=1
                    file_url=row[4]
                l=path_list[0].rfind('/')  # 找出文件名
                r=path_list[0].find('.pdf')
                file_name = path_list[0][l+1:r+4]
                full_path=base_path + file_name
                #formated_file_name='12_' +str( RunSql("select MAX(id) from report_file_12",None,True,1)[0]['MAX(id)']+1) + '.pdf'
                formated_file_name='12_' +str( cnt+12837) + '.pdf'
                
                formated_path=base_path+formated_file_name
                print(full_path + "----" + formated_path)
                if(file_name==''):
                    print("empty" )
                    full_path=''
                    continue
                else:
                    if os.path.exists(full_path):
                        if  os.path.exists(base_path+formated_file_name):
                            continue
                        else:
                            os.rename(full_path, base_path+formated_file_name)
                    else:
                        print("Not found")
                        continue
                # if file_url!='':
                #     print(f"{title} {time} {classify} {country} {file_url} {full_path}")
                #     print("---------------------------------------------------------")
                insert_query=f"insert into report_file_12 (title,publish_date,classify,country,path,url) values(\"{title}\",\"{time}\",{classify},{country},\"{full_path}\",\"{file_url}\")"
                #RunSql(insert_query,None,False,1)
                #print(insert_query)
                print(cnt)
                #print("------------------------------------------------------------------------------")
        #print(repeat)
def test1():
    print(RunSql("select MAX(id) from report_file_12",None,True,1)[0]['MAX(id)'])
def reformat_date_zero(date_str):
    date_obj = datetime.strptime(date_str, "%Y-%m-%d")
    # 将 datetime 对象转换为新的格式字符串
    formatted_date = date_obj.strftime("%Y-%m-%d")
    return formatted_date    
def reformat_date1(date_str):
    # 定义输入的日期格式
    input_format = "%d %B %Y"
    # 定义输出的日期格式
    output_format = "%Y-%m-%d"
    # 解析并重新格式化日期
    formatted_date = datetime.strptime(date_str, input_format).strftime(output_format)
    
    return formatted_date
def reformat_date(date_str):
    # 定义支持的日期格式
    formats = [
        "%d-%b-%y",    # 28-Aug-23
        "%d %b %Y",    # 22 OCT 2024
        "%d %B %Y",    # 19 October 2024
    ]
    
    # 检查输入是否已经是目标格式
    try:
        # 如果可以成功解析为 YYYY-MM-DD 格式，则直接返回
        datetime.strptime(date_str, "%Y-%m-%d")
        return reformat_date_zero(date_str)
    except ValueError:
        pass  # 不符合目标格式则继续尝试其他格式

    # 尝试其他支持的格式
    for fmt in formats:
        try:
            # 尝试解析日期
            parsed_date = datetime.strptime(date_str, fmt)
            # 如果成功，返回目标格式的日期
            return reformat_date_zero( parsed_date.strftime("%Y-%m-%d"))
        except ValueError:
            continue  # 如果解析失败，尝试下一个格式
    
    # 如果所有格式都无法解析，抛出异常
    raise ValueError(f"无法解析日期格式: {date_str}")
def find_classify(r_type,r_department):
    s=f"""SELECT id 
        FROM report_label_dict_12 s1 
        WHERE LOWER(s1.name_ori) = LOWER(\'{r_department}\')
        AND s1.pid = (
        SELECT id 
        FROM report_label_dict_12 s2 
        WHERE LOWER(s2.name_ori) = LOWER(\'{r_type}\')
        );"""
    res=RunSql(s,None,True,1)
    if(len(res)>0):
        return res[0]['id']
    else:
        return 0
if __name__=="__main__":
    main()
#    print(reformat_date("2024-01-1"))
    
#    test()
#    test1()
#    print(trans_to_cn("Infocomm Media Development Authority"))
#    name_ori="Ministry of Home Affairs"
#    print(google_translate(name_ori,"zh-CN"))
    # for i in range(0,7):  
    #     insert_report_label_dict_12()
#    print(find_classify('spe','ministry of education'))
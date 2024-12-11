import pandas as pd
from sqlalchemy import create_engine, text
import os
from fpdf import FPDF
from PIL import Image
from datetime import datetime
from RunSql import RunSql
import csv
import ast
engine_crawl = create_engine('mysql+pymysql://report:x3m0u8X#M)U*@dltrade308.mysql.rds.aliyuncs.com:3306/report_crawl')
engine_report=create_engine('mysql+pymysql://report:x3m0u8X#M)U*@am-wz9px62t6t2c32dv3131930o.ads.aliyuncs.com:3306/report')
newspaper_cn_dict = pd.read_sql('SELECT * FROM newspaper_cn',engine_crawl )
yy_mm=datetime.now().strftime("%Y-%m")
full_base_path="F:/www/full/pdf/20/" + yy_mm + "/"
part_base_path="D:/www/index/partFile/20/" + yy_mm + "/"


def test():
    query1="INSERT INTO report_label_dict_12 (id,name, pid, stage, name_en,name_ori, areaId) VALUES (6,'不知道', 4, 2,'不知道', 'MINISRY OF TRADE AND INDUSTRY SINGAPORE', 702)"
    #  try:
    #     with engine_crawl() as conn:
    #             conn.execute(query1)
    #  except Exception as e:
    #      print(f"Failed to update ")
    RunSql(query1,None,False,1)
def main():
    base_path="D:/full/pdf/12/2024-11/"
    with open("csv\Singapore_publications.csv", mode='r', encoding='utf-8') as file:
        reader = csv.reader(file)  # 创建 CSV 阅读器
        cnt=0
        repeat=0
        file_dict={}
        for row in reader:
            cnt+=1
            if(cnt>1):
                r_department=row[3]
                r_type=row[2]
                #print(r_department + " " + r_type)
                path_list=ast.literal_eval(row[5])
                #print(path_list[0])
                l=path_list[0].rfind('/')  # 找出文件名
                r=path_list[0].find('.pdf')
                file_name = path_list[0][l+1:r+4]
                full_path=base_path + file_name
                formated_file_name='12_' +str( RunSql("select MAX(id) from report_file_12",None,True,1)[0]['MAX(id)']+1) + '.pdf'
                formated_path=base_path+formated_file_name
                # if  os.path.exists(base_path+formated_file_name):
                #     continue
                # else:
                #     os.rename(full_path, base_path+formated_file_name)
                title=row[0].replace('"', '\\"')
                time=row[1]
                #find_classify_query=f"select id from report_label_dict_12 s1 where s1.name_ori = \"{r_department}\" and s1.pid=(select id from report_label_dict_12 s2 where s2.name_ori=\"{r_type}\")"
                #classify= RunSql(find_classify_query,None,True,1)[0]['id']
                classify=2
                country=702
                print(f"{title} {time} {classify} {country} {path_list} {formated_path}")
                print("---------------------------------------------------------")
                #insert_query=f"insert into report_file_12 (title,publish_date,classify,country,path) values(\"{title}\",\"{time}\",{classify},{country},\"{formated_path}\")"
                #RunSql(insert_query,None,False,1)
                #print(query1)
                

         
def test1():
    print(RunSql("select MAX(id) from report_file_12",None,True,1)[0]['MAX(id)'])
if __name__=="__main__":
#   main()
    main()
#    test1()
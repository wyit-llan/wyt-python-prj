import pandas as pd
from sqlalchemy import create_engine, text
import os
from fpdf import FPDF
from PIL import Image
from datetime import datetime
from RunSql import RunSql
engine_crawl = create_engine('mysql+pymysql://report:x3m0u8X#M)U*@dltrade308.mysql.rds.aliyuncs.com:3306/report_crawl')
engine_report_20=create_engine('mysql+pymysql://report:x3m0u8X#M)U*@am-wz9px62t6t2c32dv3131930o.ads.aliyuncs.com:3306/report')

yy_mm=datetime.now().strftime("%Y-%m")
# full_base_path="F:/www/full/pdf/20/" + yy_mm + "/"
# part_base_path="D:/www/index/partFile/20/" + yy_mm + "/"

#print(report_media_dict)
def main():
    find_max_query=f"select count(id) from report_content_12"
    cur_offset=RunSql(find_max_query,None,True,2)[0]['count(id)']
    #print(cur_offset)
    crawl_cn_dict = pd.read_sql(f"SELECT * FROM report_file_12 LIMIT 10000 OFFSET {cur_offset}",engine_crawl )
    base_fullUrl="full/pdf/702/2024-11/"
    for index,row in crawl_cn_dict.iterrows():

        
                          #对每一个ID进行操作
        rptcn_id=row['id']
        srcId=row["id"]
        title=row['title'].replace('"', '\\"')
        
        date=row['publish_date'].replace('-', '')
        print(date)
        path="reportFile/"+ base_fullUrl +'12_'+ str(rptcn_id) + '.pdf'
        area_name="新加坡"
        area_name_en="Singapore"
        areaId=702
        label_id=row['classify']
        label_name=RunSql(f"select name from report_label_dict_12 where id = {label_id}",None,True,2)[0]['name']
        label_name_en=RunSql(f"select name_en from report_label_dict_12 where id = {label_id}",None,True,2)[0]['name_en']
        
        #print(f"{rptcn_id}-{title}-{date}-{path}-{area_name}-{areaId}-{label_name}-{label_name_en}-{label_id}")
        insert_content_query=f"""insert into report_content_12 
                    (id,title_ori,fullUrl_ori,label_name,label_name_en,area_name,area_name_en,particularDate,srcId,areaId,labelId)
                    values({rptcn_id},\"{title}\",\"{path}\",\"{label_name}\",\"{label_name_en}\",\"{area_name}\",\"{area_name_en}\",{date},{rptcn_id},{areaId},{label_id})
                    """
        insert_area_query=f"insert into report_area_12 (reportId,areaId1) values({rptcn_id},{areaId})"
        #print(insert_content_query)
        RunSql(insert_content_query,None,False,2)
        RunSql(insert_area_query,None,False,2)
        print(rptcn_id)
        
        #print(insert_area_query)
def test():
    #s="reportFile/full/pdf/12/2024-11/12_32.pdf"
    #s1=s[0:23]+"702/"+s[23:]
    #print(s1)
    # for cur_id in range(32,3805):
    #     select_query=f"select fullUrl_ori from report_content_12 where id = {cur_id}"
    #     s=RunSql(select_query,None,True,2)[0]['fullUrl_ori']
    #     s1=s[0:23]+"702/"+s[23:]
    #     update_query=f"update report_content_12 set fullUrl_ori=\"{s1}\" where id ={cur_id}"
    #     RunSql(update_query,None,False,2)
    #     print(cur_id)
    label_dict= pd.read_sql('SELECT * FROM report_label_dict_12',engine_crawl )
    cnt=1
    for index,row in label_dict.iterrows():
        cur_id=row['id']
        cur_pid=row['pid']
        name=row['name']
        name_ori=row['name_ori']
        name_en=row['name_en']
        stage=row['stage']
        areaId=row['areaId']
        find_fa_name_query=f"select name from report_label_dict_12 where id = {cur_pid}"
        fa_name=''
        description=row['name']
        if(cur_pid!=-1):
            fa_name= RunSql(find_fa_name_query,None,True,1)[0]['name']
            description=row['name'] + '-' + fa_name
            #print(description)
        insert_report_query=f"""insert into report_label_dict_12(id,name,pid,stage,description,areaId,name_ori,name_en)
                            values({cur_id},\"{name}\",{cur_pid},{stage},\"{description}\",{areaId},\"{name_ori}\",\"{name_en}\")    """
        RunSql(insert_report_query,None,False,2)
        print(cur_id)
def reformat_date_zero(date_str):
    date_obj = datetime.strptime(date_str, "%Y-%m-%d")
    # 将 datetime 对象转换为新的格式字符串
    formatted_date = date_obj.strftime("%Y-%m-%d")
    return formatted_date
def update_date_formated():
    for id in range(7980,11754):
        find_cur_date_query=f"SELECT publish_date from report_file_12 WHERE id ={id}"
        cur_date=RunSql(find_cur_date_query,None,True,1)[0]['publish_date']
        new_date=reformat_date_zero(cur_date)
        update_date_query=f"UPDATE report_file_12 SET publish_date=\"{new_date}\" WHERE id={id}"
        RunSql(update_date_query,None,False,1)
        new_date_to_report=new_date.replace('-', '')
        update_report_query=f"UPDATE report_content_12 SET particularDate={new_date_to_report} WHERE id={id}"
        RunSql(update_report_query,None,False,2)
        print(id)
       # print(update_report_query+'\n------------------------')

if __name__=="__main__":
#    main()
#    test()
#    find_max_query=f"select count(id) from report_content_12"
#    print()
#    main()
#    print(reformat_date_zero("2024-1-1"))
#    print(reformat_date_zero("2024-8-01"))
    update_date_formated()
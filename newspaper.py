import pandas as pd
from sqlalchemy import create_engine, text
import os
from fpdf import FPDF
from PIL import Image
from datetime import datetime
engine_newspaper = create_engine('mysql+pymysql://report:x3m0u8X#M)U*@dltrade308.mysql.rds.aliyuncs.com:3306/report_crawl')
engine_report_20=create_engine('mysql+pymysql://report:x3m0u8X#M)U*@am-wz9px62t6t2c32dv3131930o.ads.aliyuncs.com:3306/report')
newspaper_cn_dict = pd.read_sql('SELECT * FROM newspaper_cn',engine_newspaper )
yy_mm=datetime.now().strftime("%Y-%m")
full_base_path="F:/www/full/pdf/20/" + yy_mm + "/"
part_base_path="D:/www/index/partFile/20/" + yy_mm + "/"

#print(report_media_dict)
def main():
    for index,row in newspaper_cn_dict.iterrows():
        #print(row['id'])                  #对每一个ID进行操作
        cur_id=row['id']
    
        query=f"SELECT * FROM newspaper_cn_imgs WHERE newspaper_cn_id={cur_id}"
        newspaper_imgs_dict=pd.read_sql(query,engine_newspaper)
        # print(newspaper_imgs_dict)
        # break
        if newspaper_imgs_dict.empty:
            print(f"No images found for id: {cur_id}")
            continue
        full_pdf_path=os.path.join(full_base_path,f"20_{cur_id}.pdf")
        #print("full:" + full_pdf_path)
        part_pdf_path=os.path.join(part_base_path,f"20_{cur_id}.pdf")
        #print( "part:" + part_pdf_path)
        full_pdf=FPDF()
        part_pdf=FPDF()
        for img_idx,img_row in newspaper_imgs_dict.iterrows():
            #img_path="D:/www/index/library/" + cur_id + img_row['img']
            img_path=f"D:/www/index/library/{cur_id}/{img_row['img']}"
            #print(img_path)
            if not os.path.exists(img_path):
                print(f"Image not found: {img_path}")
                continue
            try:
                # 确保图片可以打开
                with Image.open(img_path) as img:
                    # 添加图片到 PDF
                    full_pdf.add_page()
                    full_pdf.image(img_path, x=10, y=10, w=190)  # 调整位置和尺寸适配 PDF 页面
                    if img_idx<2:
                        part_pdf.add_page()
                        part_pdf.image(img_path, x=10, y=10, w=190)  # 调整位置和尺寸适配 PDF 页面
            except Exception as e:
                print(f"Error processing image {img_path}: {e}")
        full_pdf.output(full_pdf_path)
        print(f"Saved PDF: {full_pdf_path}")
        part_pdf.output(part_pdf_path)
        print(f"SavedPDF: {part_pdf_path}")


        country = row.get('country', '国家未知') or '国家未知'
        newspaper = row.get('newspaper', '新闻未知') or '新闻未知'
        
        # 构建 URL 和标题
        partUrl = f"/index/partFile/20/{yy_mm}/20_{cur_id}.pdf"
        fullUrl = f"/full/pdf/20/{yy_mm}/20_{cur_id}.pdf"
        fullUrl_cn = 'unknown'
        title = f"{country} {newspaper}"
        update_query="""
        UPDATE report_content_20
        SET partUrl = %s,
            fullUrl = %s,
            fullUrl_cn = %s,
            title = %s
        WHERE id = %s
        """
        params = (partUrl, fullUrl, fullUrl_cn, title, cur_id)
        try:
            with engine_report_20.connect() as conn:
                conn.execute(update_query, params)
            print(f"Updated report_content_20 for id {cur_id}")
        except Exception as e:
            print(f"Failed to update id {cur_id}: {e}")

if __name__=="__main__":
    main()
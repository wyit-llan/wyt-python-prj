import PyPDF2
import json
from sortDirectoryJson import sort_json
from pdf2image import convert_from_path
# 示例用法
input_pdf = "input.pdf"  # 输入 PDF 文件路径
output_pdf = "extractedPDF/extracted_pages2.pdf"  # 输出 PDF 文件路径
start_page = 1  # 起始页面（第 2 页，索引从 0 开始）
end_page = 4    # 结束页面（第 5 页，索引从 0 开始）
def extract_pages_from_pdf(input_pdf_path, output_pdf_path, start_page, end_page):
    """
    从 PDF 中提取指定范围的页面并保存为新的 PDF 文件。
    
    :param input_pdf_path: 输入 PDF 文件的路径
    :param output_pdf_path: 输出 PDF 文件的路径
    :param start_page: 起始页面索引（从 0 开始）
    :param end_page: 结束页面索引（从 0 开始）
    """
    # 打开原始 PDF 文件
    start_page-=1
    end_page-=1
    with open(input_pdf_path, "rb") as input_pdf_file:
        # 创建 PDF 阅读器对象
        pdf_reader = PyPDF2.PdfReader(input_pdf_file)
        
        # 创建 PDF 写入器对象
        pdf_writer = PyPDF2.PdfWriter()
        
        # 提取指定范围的页面
        for page_number in range(start_page, end_page + 1):
            if 0 <= page_number < len(pdf_reader.pages):
                page = pdf_reader.pages[page_number]
                pdf_writer.add_page(page)
            else:
                print(f"Page number {page_number + 1} is out of range.")
        
        # 保存提取的页面为新的 PDF 文件
        with open(output_pdf_path, "wb") as output_pdf_file:
            pdf_writer.write(output_pdf_file)
        print(f"Pages {start_page + 1} to {end_page + 1} extracted successfully and saved to {output_pdf_path}")


def find_directory_base_page(full_pdf_path):
      base_page=0  
      pdf_file=open(full_pdf_path,'rb')
      pdf_reader=PyPDF2.PdfReader(pdf_file)
      num_pages=len(pdf_reader.pages)
      flag=0
      pages = convert_from_path(full_pdf_path, 300, first_page=1, last_page=60)   #选择需要转换为图片的范围
      for i, page in enumerate(pages):
         page_totxt=pdf_reader.pages[i]
         p_text=page_totxt.extract_text()
         #print(str(i) + p_text)
         #print("------------------------------------------------------------------------------------")
         ts=p_text.lower().replace('\n', '').replace(' ', '')
         if(ts.startswith("note")):
                #flag=1
                base_page=i+1
                break
        #  if flag==1:
        #       #if(p_text.lower().startswith('i\ntreaties and international agreements\nregistered') or p_text.lower().startswith('treaties and international agreements\nregistered') ):   
        #       if(ts.startswith("itreatiesandinternationalagreementsregistered") or ts.startswith("treatiesandinternationalagreementsregistered")):
        #            base_page=i+1
        #            break
        #  if(i==7):
        #         print(p_text.lower().startswith("note  by"))
                
        #  if(i==9):
        #         ts=p_text.lower().replace('\n', '').replace(' ', '')
        #         print(p_text.lower().replace('\n', '').replace(' ', ''))
        #         print(ts.startswith("itreatiesandinternationalagreementsregistered") or ts.startswith("treatiesandinternationalagreementsregistered"))
        #         #print(p_text.lower().replace('\n', '').replace(' ', '').startswith('i\n\n\n\ntreaties and international agreements\nregistered') or p_text.lower().startswith('itreatiesandinternationalagreementsregistered') )
        #         break
      return base_page
        #  if i<=4:
        #      if(i%2!=0):    
                
        #        #print(f'Page {i + 1} saved as {output_image_path}')   
        #  elif( len(p_text)>0 and not p_text.lower().startswith("note")):
        #     if(i%2!=0):    

  
        #        #print(f'Page {i + 1} saved as {output_image_path}')
        #  else:
        #      break
def testbasepage():
    base_path="H:/volumn/volumn_pdf/v"
    for idx in range(845,3165):
        try:
            full_path=base_path+str(idx)+".pdf"
            base_page=find_directory_base_page(full_path)
            print(f"pdf{idx}:{base_page}")
            with open('v_1.json', 'r', encoding='utf-8') as file:
                base_page_json = json.load(file)
            base_page_json[f'pdf{idx}'] = base_page
            with open('v_1.json', 'w', encoding='utf-8') as file:
                json.dump(base_page_json, file, ensure_ascii=False, indent=4)
        except Exception as e:
            print(e)
        
def solv_zero(input_path):
    with open('base_page_zero.json','r',encoding='utf-8') as file:
        data_zero=json.load(file)        
    ls=data_zero.keys()
    base_path="H:/volumn/volumn_pdf/v"
    for it in ls:
        try:
            if(data_zero[it]!=0) :continue
            full_path=base_path + it[3:] + '.pdf'
            base=find_directory_base_page(full_path)
            print(it[3:] + ':' +str(base))
            data_zero[it]=base
            with open('base_page_zero.json','w',encoding='utf-8') as file:
                json.dump(data_zero,file,ensure_ascii=False,indent=4)
        except Exception as e:
            print(e)


if __name__ == "__main__":
    #extract_pages_from_pdf("H:/volumn/volumn_pdf/v1.pdf", output_pdf, 15, 16)
    #testbasepage()
    #find_directory_base_page("H:/volumn/volumn_pdf/v254.pdf")  
    solv_zero('base_page.json')
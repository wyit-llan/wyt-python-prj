# 这是一个 DMXAPI 调用 API 的 Python 例子
import requests
import json
from pdf2image import convert_from_path
import os
import datetime
import fitz
import base64
import shutil
import PyPDF2
# ------------------------------------------------------------------------------------
#         3秒步接入 DMXAPI ：  修改 Key 和 Base url (https://www.dmxapi.com)
# ------------------------------------------------------------------------------------
def text_gptTest():
   url = "https://www.dmxapi.com/v1/chat/completions"   # 这里不要用 openai base url，需要改成DMXAPI的中转 https://www.dmxapi.com ，下面是已经改好的。

   payload = json.dumps({
      "model": "gpt-4o-mini",  # 这里是你需要访问的模型，改成上面你需要测试的模型名称就可以了。
      "messages": [
         {
            "role": "system",
            "content": "You are a helpful assistant."
         },
         {
            "role": "user",
            "content": "周树人和鲁迅是兄弟吗？"
         }
      ]
   })
   headers = {
      'Accept': 'application/json',
      'Authorization': 'sk-7mxNVRq0krz4bAHMuCePETGwbDfCppkja5a7hJ2NYNhEJk44', # 这里放你的 DMXapi key
      'User-Agent': 'DMXAPI/1.0.0 (https://www.dmxapi.com)',  # 这里也改成 DMXAPI 的中转URL https://www.dmxapi.com，已经改好
      'Content-Type': 'application/json'
   }

   response = requests.request("POST", url, headers=headers, data=payload)
   print(response.text)
def encode_image(image_path):
    """
    读取本地图片并编码为Base64字符串。
    """
    with open(image_path, "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read()).decode("utf-8")
    return encoded_string
def pdf_to_img(pdf_no):
      Base_path="H:/volumn/volumn_pdf/"
      
      my_mkdir(pdf_no)
      output_folder="images/images_for_pdf_v"+str(pdf_no)
      full_pdf_path=Base_path+"v"+str(pdf_no)+".pdf"
      pdf_file=open(full_pdf_path,'rb')
      pdf_reader=PyPDF2.PdfReader(pdf_file)
      num_pages=len(pdf_reader.pages)
      pages = convert_from_path(full_pdf_path, 300, first_page=1, last_page=20)   #选择需要转换为图片的范围
      for i, page in enumerate(pages):
         page_totxt=pdf_reader.pages[i]
         p_text=page_totxt.extract_text()
         #print(str(i) + p_text)
         #print("------------------------------------------------------------------------------------")
         if i<=4:
             if(i%2!=0):    
               output_image_path = os.path.join(output_folder, f'page_{i + 1}.png')
               page.save(output_image_path, 'PNG')  # 保存为 PNG 格式
               #print(f'Page {i + 1} saved as {output_image_path}')   
         elif( len(p_text)>0 and not p_text.lower().startswith("note")):
            if(i%2!=0):    
               output_image_path = os.path.join(output_folder, f'page_{i + 1}.png')
               page.save(output_image_path, 'PNG')  # 保存为 PNG 格式
               #print(f'Page {i + 1} saved as {output_image_path}')
         else:
             break
             
      print(full_pdf_path)
def generate_query(pdf_no):
      content=[{"type": "text", "text": """把图片中目录部分的文本准确的给我，尤其是页码和内容的对应({
title: '',
page:'',})"""}, ] # 发送文本消息  在此给出对gpt的提问
      pdf_no=2
      dir_path="images/images_for_pdf_v" + str(pdf_no)
      imgs=''
      base64_imgs=[]
      for files in os.walk(dir_path):
         imgs = files
      for it in imgs[2]:
         full_img=dir_path + "/" +str(it)
         base64_imgs.append(encode_image(full_img))
      for idx in range(0, len(base64_imgs)):
              
             message={
                  "type":"image_url",
                  "image_url":{
                       "url":f"data:image/png;{base64_imgs[idx]}" 
                  },
             }
          
             content.append(message)
      print(content)
      return(content)       
def handle_img(pdf_no):
      content=[{"type": "text", "text": """把图片中目录部分的文本准确的给我，尤其是页码和内容的对应({
title: '',
page:'',})"""}, ] # 发送文本消息  在此给出对gpt的提问
      dir_path="images/images_for_pdf_v" + str(pdf_no)
      imgs=''
      base64_imgs=[]
      for files in os.walk(dir_path):
         imgs = files
      for it in imgs[2]:
         full_img=dir_path + "/" +str(it)
         base64_imgs.append(encode_image(full_img))
      for idx in range(0, len(base64_imgs)):
              
             message={
                  "type":"image_url",
                  "image_url":{
                       "url":f"data:image/png;{base64_imgs[idx]}" 
                  },
             }
          
             content.append(message)
      
      域名 = "https://www.dmxapi.com/"  # 定义API的基础域名
      API_URL = 域名 + "v1/chat/completions"  # 完整的API请求URL
      API_KEY = "sk-7mxNVRq0krz4bAHMuCePETGwbDfCppkja5a7hJ2NYNhEJk44"  # <--------------------------------------------- 请替换为你的 DMXAPI 令牌
      # 本地图片路径
        # <--------------------------------------------- 本地图片路径
      # base64_image = encode_image('images/images_for_pdf_v2/page_2.png')  # 编码本地图片
      # base64_image_1 = encode_image('images/images_for_pdf_v2/page_4.png')
      # base64_image_2 = encode_image('images/images_for_pdf_v2/page_6.png')
      # base64_image_3 = encode_image('images/images_for_pdf_v2/page_8.png')
      #content=generate_query(2)
      # 创建请求数据payload，包括所需的模型和消息内容
      my_query1="请解释图片里目录中所指出的每一部分分别在哪一页，我需要准确的页码和每一部分的对应关系"
      my_query="把图片中目录部分的文本准确的给我，尤其是页码和内容的对应，最好在输出时目录的格式也与图片一致"
      payload = {
         "model": "gpt-4o-mini",  # 指定使用的多模态AI模型，除了gpt-4o 也推荐使用 claude-3-5-sonnet系列
         "messages": [
            {
                  "role": "system",  # 系统角色信息，可以为空
                  "content": "",
            },
            {
                  "role": "user",  # 用户角色的消息内容
                  "content": 
                    [
                     {"type": "text", "text": """把每个图片中目录部分的文本给我,目录后面的ANNEX也要（只需要返回一个json），目录内容按照格式：
```json
{
    "list":[{"No.":"","title": "","page":"",}]}
```
list 内每一项是一条目录条目(No.  title (大标题和小标题都要)  page)，list 每一项按 page 排序，page 小的放在大的前面，page 的值是数字类型"""},  # 发送文本消息  在此给出对gpt的提问
                     # {"type": "text", "text": """把每个图片中目录部分的文本的给我（只需要返回一个json），目录内容按照格式：({
                     #  "list":[{No.:'',title: '',page:'',}]}) ，一张图片对应一个大的obj,obj内有两项内容1:一个列表：列表内每一项是一条目录条目(No.  title (大标题和小标题都要)  page) 2：page_num 当前图片是第几张"""},  # 发送文本消息  在此给出对gpt的提问
                     # {
                     #    "type": "image_url",  # 发送图片URL
                     #    "image_url": {
                     #          # 使用Base64编码的本地图片
                     #          "url": f"data:image/png;base64,{base64_imgs[0]}"
                     #    },
                     # },
                     # {
                     #    "type": "image_url",  # 发送图片URL
                     #    "image_url": {
                     #          # 使用Base64编码的本地图片
                     #          "url": f"data:image/png;base64,{base64_imgs[1]}"
                     #    },
                     # },
                     # {
                     #    "type": "image_url",  # 发送图片URL
                     #    "image_url": {
                     #          # 使用Base64编码的本地图片
                     #          "url": f"data:image/png;base64,{base64_imgs[2]}"
                     #    },
                     # },
                     # {
                     #    "type": "image_url",  # 发送图片URL
                     #    "image_url": {
                     #          # 使用Base64编码的本地图片
                     #          "url": f"data:image/png;base64,{base64_imgs[3]}"
                     #    },
                     # },
                  ],
            },
         ],
         "temperature": 0.1,  # 设置生成文本的随机性，越低输出越有确定性
         "user": "DMXAPI",  # 发送请求的用户标识
      }
      for idx in range(0,len(base64_imgs)):
          payload["messages"][1]["content"].append({
            "type": "image_url",
            "image_url": {
                  "url": f"data:image/png;base64,{base64_imgs[idx]}"
            },
         })       
      # 定义HTTP请求头，包括内容类型和身份验证信息
      headers = {
         "Content-Type": "application/json",  # 设置内容类型为JSON
         "Authorization": f"Bearer {API_KEY}",  # 使用 f-string 动态插入 API_KEY，进行身份验证
         "User-Agent": f"DMXAPI/1.0.0 ({域名})",  # 自定义的User-Agent，用于识别客户端信息
      }

      # 发送POST请求，将请求数据和头信息传入API，获取响应
      response = requests.post(API_URL, headers=headers, json=payload)

      # 输出API的响应内容
      #print(json.loads(response.text)["choices"][0]["message"]["content"])
      res=json.loads(response.text.replace("```", "").replace('json', ''))
      content_data=json.loads(res["choices"][0]["message"]["content"])
      with open("directoryTxt/v_"+ str(pdf_no) + ".json","w",encoding="utf-8") as file:
         json.dump(content_data, file, indent=4, ensure_ascii=False)
def my_mkdir(cnt):
      # os.mkdir("D:/volumn/new_directory_"+str(cnt))
      os.mkdir("images/images_for_pdf_v"+str(cnt))
def delete_dir(pdf_no):
       delete_path="images/images_for_pdf_v"+ str(pdf_no)
       shutil.rmtree(delete_path)  # 删除非空目录及其中的所有文件和子目录
def main():
   
   #pdf_to_img(2)
   #base_img_path="images/images_for_pdf_v"+str(pdf_no)+"/"
   # for idx in range(4,5):
   #       img_path=base_img_path+"page_"+str(idx)+".png"
   #       #print(img_path)
   #       handle_img(img_path)
   #       print("----------------------------------------------")
   #for basic_index in range(900, 2701, 300):
      for pdf_no in range(928, 929):
         try:    
            pdf_to_img(pdf_no)
            handle_img(pdf_no)
            #delete_dir(pdf_no)
         except Exception as e:
            print(e)
      # 
         # s = s.replace('```json\n', '').replace('```', '')
         # print(json.loads(s))
if __name__ == "__main__":
#     test()
#   pdf_to_img(2)
#   my_mkdir(1)
#   delete_dir("new_directory_1")
#   main()
#   my_print()
#   print(0.005 * 3012 * 5)
#    generate_query(2)    
#    handle_img()  
#   generate_query(2)
#    my_print()
#   delete_dir(2)
   main()
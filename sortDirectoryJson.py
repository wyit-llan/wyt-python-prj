import json

# 读取原始 JSON 文件
def sort_json(input_path):
    with open(input_path, 'r', encoding='utf-8') as file:
        data = json.load(file)

    # 对 'list' 按照 'page' 的值进行排序
    data['list'].sort(key=lambda x: x['page'])

    # 将排序后的数据写回到原文件
    with open(input_path, 'w', encoding='utf-8') as file:
        json.dump(data, file, ensure_ascii=False, indent=4)

    print(f"JSON 文件{input_path}已排序并重新写入。")
def find_zero(input_path):
    with open(input_path,'r',encoding='utf-8') as file:
        data=json.load(file)
    keys=data.keys()
    res={}
    for it in keys:
        if(data[it]==0):
            res[it]=0
    with open('base_page_zero1.json','w',encoding='utf-8') as file:
        json.dump(res,file,ensure_ascii=False,indent=4)
def main():
    for idx in range(173,174):
        input_path="directoryTxt/v_"+str(idx)+".json"
        sort_json(input_path)
def update_zero(input,output):
    with open(input,'r',encoding='utf-8') as file:
        data_up=json.load(file)
    with open(output,'r',encoding='utf-8') as file:
        data_ori=json.load(file)
    for it in data_up.keys():
        data_ori[it]=data_up[it]
    with open(output,'w',encoding='utf-8') as file:
        json.dump(data_ori,file,ensure_ascii=False,indent=4)
def update_basepage_sub1(input):
    with open(input,'r',encoding='utf-8') as file:
        data=json.load(file)
    #for it in data.keys():
        #data[it]-=1
    #with open(input,'w',encoding='utf-8') as file:
    #    json.dump(data,file,ensure_ascii=False,indent=4)    
    ls=list(data.keys())
    s_count=0
    for idx in range(0,len(ls)):
        if idx<1000:
            idx+=1
        s_count+=data[ls[idx]]
        #print(ls[idx])    
    print((s_count/5)*0.02)
if __name__ == "__main__":
    #main()        
   # find_zero('base_page_zero.json')
   #update_zero('base_page_zero.json','base_page.json')
   #update_basepage_sub1('base_page.json')
   update_basepage_sub1('base_page.json')
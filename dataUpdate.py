import pandas as pd
from sqlalchemy import create_engine, text

# 创建数据库连接
engine_content = create_engine('mysql+pymysql://report:x3m0u8X#M)U*@am-wz9px62t6t2c32dv3131930o.ads.aliyuncs.com:3306/report')
engine_asean = create_engine('mysql+pymysql://report:x3m0u8X#M)U*@dltrade308.mysql.rds.aliyuncs.com:3306/report_crawl')

# 读取 media 字典
report_media_dict = pd.read_sql('SELECT * FROM report_media_dict', engine_content)
media_dict = report_media_dict.set_index('name')['id'].to_dict()

# 每次处理的记录数
batch_size = 10000
offset = 0

while True:
    # 查询 batch_size 条数据
    report_content_8 = pd.read_sql(f'SELECT * FROM report_content_8 LIMIT {batch_size} OFFSET {offset}', engine_content)

    if report_content_8.empty:
        break  # 如果没有数据则退出循环

    # 更新 mediaId
    report_content_8['mediaId'] = report_content_8['media'].map(media_dict)

    # 读取 srcId 和 url
    asean_news = pd.read_sql('SELECT id, url FROM asean_news', engine_asean)
    url_dict = asean_news.set_index('id')['url'].to_dict()

    # 更新 srcUrl
    report_content_8['srcUrl'] = report_content_8['srcId'].map(url_dict)
    print("BEGIN")
    # 批量更新 srcUrl 和 mediaId
    with engine_content.connect() as connection:
        for _, row in report_content_8.iterrows():
            print("INSERTED")
            update_query = text("""
                UPDATE report_content_8 
                SET mediaId = :mediaId, srcUrl = :srcUrl 
                WHERE srcId = :srcId
            """)
            connection.execute(update_query, {'mediaId': row['mediaId'], 'srcUrl': row['srcUrl'], 'srcId': row['srcId']})

    # 增加 offset
    print("OVER")
    offset += batch_size
    
   
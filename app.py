import pandas as pd
from sqlalchemy import create_engine

# 创建数据库连接
engine = create_engine('mysql+pymysql://report:x3m0u8X#M)U*@am-wz9px62t6t2c32dv3131930o.ads.aliyuncs.com:3306/report')

# 读取 CSV 文件
df = pd.read_csv('newsSrc.csv')

# 新增自增id列
df.insert(0, 'id', range(1, len(df) + 1))

# 导入数据到数据库
df.to_sql('report_media_dict', con=engine, if_exists='append', index=False)
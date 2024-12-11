import time
import pymysql
from dbutils.pooled_db import PooledDB

# 连接配置信息
config3 = {
    'creator': pymysql,

    # 服务器--开始
    'host': 'chinaasean.mysql.rds.aliyuncs.com',
    'port': 3306,  # MySQL默认端口
    'user': 'chinaaseanocean',  # mysql默认用户名
    'password': 'x3m0u8X#M)U*',
    'db': 'chinaaseanocean',  # 数据库
    # 服务器--结束

    'maxconnections': 10,
    'charset': 'utf8mb4',
    'cursorclass': pymysql.cursors.DictCursor,
}

config1 = {
    'creator': pymysql,

    # # 服务器--开始
    # 'host': 'dinglingtrade.mysql.rds.aliyuncs.com',
    'host': 'dltrade308.mysql.rds.aliyuncs.com',  # 内
    'port': 3306,  # MySQL默认端口
    'user': 'report',  # mysql默认用户名
    'password': 'x3m0u8X#M)U*',
    'db': 'report_crawl',  # 数据库
    # # 服务器--结束

    'maxconnections': 10,
    'charset': 'utf8mb4',
    'cursorclass': pymysql.cursors.DictCursor,
}

# 大数据
config2 = {
    'creator': pymysql,
    # # 服务器--开始  大数据库 'am-wz9px62t6t2c32dv3131930o.ads.aliyuncs.com'
    'host': 'am-wz9px62t6t2c32dv3131930o.ads.aliyuncs.com',
    # 'host': 'am-wz9px62t6t2c32dv3131930o.ads.aliyuncs.com',
    'port': 3306,  # MySQL默认端口
    'user': 'report',  # mysql默认用户名
    'password': 'x3m0u8X#M)U*',
    'db': 'report',  # 数据库
    # # 服务器--结束

    'maxconnections': 10,
    'charset': 'utf8mb4',
    'cursorclass': pymysql.cursors.DictCursor,
}

# pool1 = PooledDB(**config3)  # 海洋数据库
pool1 = PooledDB(**config1)  # crawl数据库
pool2 = PooledDB(**config2)  # 大数据


# con = pymysql.connect(**config1)
# con.ping(reconnect=True)
# cursor = con.cursor()
# cursor.execute(sql)

# 处理可能丢失链接
def SuccessSql(sql, param=None, isSelect=True, pool_config=1, error_times=0):
    # print("SQL: ", sql)
    try:
        return RunSql(sql, param, isSelect, pool_config)
    except Exception as e:
        time.sleep(10)
        error_times += 1
        if error_times < 5:
            return SuccessSql(sql, param, isSelect, pool_config, error_times)
        else:
            raise Exception(sql + '执行失败\n error:' + str(e))


def RunSql(sql, param=None, isSelect=True, pool_config=1):
    """
    执行一条sql语句
    :param sql: sql字符串 ，注意如果使用like查询请直接sql拼串，不要传入param
    :param param: 如果sql中使用占位符则该参数必填（多个占位符则组成元组或者列表形式）
    :param isSelect: 是否为查询操作，默认为True
    :return: 查询操作返回查询结果， 其他执行成功返回True，否则抛出异常
    """
    con = None
    cur = None
    if pool_config == 1:
        pool = pool1
    elif pool_config == 2:
        pool = pool2
    try:
        con = pool.connection()
        cur = con.cursor()
        cur.execute(sql, param)

        if isSelect:
            result = cur.fetchall()
            return result
        else:
            con.commit()
            return True
    except Exception as e:
        if con:
            con.rollback()
            print("sql出错", str(e), sql)
        else:
            print("数据库连接出错")
        # raise e
        return False

    finally:
        if con is not None:
            cur.close()
        if cur is not None:
            con.close()


def RunManySql(sql, params=None, isSelect=True, pool_config=1):
    """
    执行多条sql语句(批量增加更新删除)
    :param sql: sql字符串  注意如果使用like查询请直接sql拼串，不要传入param
    :param params: 如果sql中使用占位符则该参数必填（多个占位符则组成元组或者列表形式[[],[]...], ((),()...), [(), ()...], ([],[]...)）
    :param isSelect: 是否为查询操作，默认为True
    :return: 查询操作返回查询结果， 其他执行成功返回True，否则抛出异常
    """
    con = None
    cur = None
    if pool_config == 1:
        pool = pool1
    elif pool_config == 2:
        pool = pool2
    try:
        con = pool.connection()
        cur = con.cursor()
        cur.executemany(sql, params)

        if isSelect:
            result = cur.fetchall()
            return result
        else:
            con.commit()
            return True
    except Exception as e:
        if con:
            con.rollback()
            print("sql出错", str(e), sql)
        else:
            print("数据库连接出错")
        raise e
        # return False

    finally:
        if con is not None:
            cur.close()
        if cur is not None:
            con.close()


# def insert_sql_with_id(insert_sql, data_list):
#     inserted_ids = []
#     connection = pymysql.connect(
#         host='dltrade308.mysql.rds.aliyuncs.com',
#         port=3306,
#         user='report',
#         password='x3m0u8X#M)U*',
#         database='report_crawl',
#         charset='utf8mb4',
#         cursorclass=pymysql.cursors.DictCursor
#     )
#     try:
#         with connection.cursor() as cursor:
#             # 逐条插入数据
#             for data in data_list:
#                 cursor.execute(insert_sql, data)
#                 # 如果插入成功，获取插入的ID
#                 if cursor.rowcount > 0:
#                     inserted_ids.append(cursor.lastrowid)
#             # 提交事务
#             connection.commit()
#     except Exception as e:
#         print(f"An error occurred: {e}")
#         connection.rollback()
#     finally:
#         cursor.close()
#
#     return inserted_ids


def insert_sql_with_id(insert_sql, select_sql, data_list):
    # inserted_data_ids = {}
    inserted_data_ids = []
    connection = pymysql.connect(
        host='dltrade308.mysql.rds.aliyuncs.com',
        port=3306,
        user='report',
        password='x3m0u8X#M)U*',
        database='report_crawl',
        charset='utf8mb4',
        cursorclass=pymysql.cursors.DictCursor
    )
    try:
        with connection.cursor() as cursor:
            # 逐条处理数据
            for data in data_list:
                # 首先检查是否已存在
                cursor.execute(select_sql, data[:1])
                result = cursor.fetchone()

                if result:
                    # 数据已存在，将数据和现有的 ID 对应起来
                    # inserted_data_ids[data] = result['id']
                    temp = [result['id']] + [item for item in data]
                    inserted_data_ids.append(temp)
                else:
                    # 尝试插入数据
                    cursor.execute(insert_sql, data)
                    # 如果插入成功，获取插入的 ID
                    if cursor.rowcount > 0:
                        temp = [cursor.lastrowid] + [item for item in data]
                        inserted_data_ids.append(temp)
                        # inserted_data_ids[data[0]] = cursor.lastrowid

            # 提交事务
            connection.commit()
    except Exception as e:
        print(f"An error occurred: {e}")
        connection.rollback()
    finally:
        cursor.close()
        connection.close()

    return inserted_data_ids


if __name__ == '__main__':
    sql1 = "select * from asean_news limit 1"
    sql2 = "select * from report_content_1 limit 1"

    res = RunSql(sql2, pool_config=2)
    print(res)

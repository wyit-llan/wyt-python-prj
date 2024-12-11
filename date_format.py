from datetime import datetime

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
        return date_str
    except ValueError:
        pass  # 不符合目标格式则继续尝试其他格式

    # 尝试其他支持的格式
    for fmt in formats:
        try:
            # 尝试解析日期
            parsed_date = datetime.strptime(date_str, fmt)
            # 如果成功，返回目标格式的日期
            return parsed_date.strftime("%Y-%m-%d")
        except ValueError:
            continue  # 如果解析失败，尝试下一个格式
    
    # 如果所有格式都无法解析，抛出异常
    raise ValueError(f"无法解析日期格式: {date_str}")

# 示例输入
dates = [
    "2023-10-19",     # 已经是目标格式
    "28-Aug-23",      # 需要转换
    "22 OCT 2024",    # 需要转换
    "19 October 2024" # 需要转换
]

# 测试
for date in dates:
    try:
        print(f"原日期: {date} -> 转换后: {reformat_date(date)}")
    except ValueError as e:
        print(e)

import os
import shutil

def move_files(source_folder, destination_folder):
    # 确保目标文件夹存在，不存在则创建
    if not os.path.exists(destination_folder):
        os.makedirs(destination_folder)
    
    # 遍历源文件夹中的所有文件
    for filename in os.listdir(source_folder):
        source_path = os.path.join(source_folder, filename)
        destination_path = os.path.join(destination_folder, filename)
        
        # 确保是文件才移动（忽略子文件夹）
        if os.path.isfile(source_path):
            shutil.move(source_path, destination_path)
            print(f"Moved: {source_path} -> {destination_path}")

# 示例
#source_folder = "path/to/source_folder"  # 替换为源文件夹路径
#destination_folder = "path/to/destination_folder"  # 替换为目标文件夹路径
if __name__=="__main__":
    move_files("D:/SingaporePDF/manpower/Speeches","D:/full/pdf/12/702/2024-11")

import os
import requests

# 設定文件路徑
UUID_MAP_FILE = "uuid_map.txt"
HASH_MAP_FILE = "hash_map.txt"
NAME_MAP_FILE = "name_map.txt"
OK_FILE = "ok.txt"
BASE_URL = "https://asset.crimsonyouma.com/adult/pc/A/assets/All/native"
DOWNLOAD_FOLDER = "downloads"

# 確保下載資料夾存在
os.makedirs(DOWNLOAD_FOLDER, exist_ok=True)

# 確保映射文件存在
for file in [UUID_MAP_FILE, HASH_MAP_FILE, NAME_MAP_FILE, OK_FILE]:
    if not os.path.exists(file):
        open(file, "w", encoding="utf-8").close()

# 讀取映射文件
def read_map_file(filename):
    mapping = {}
    with open(filename, "r", encoding="utf-8") as file:
        for line in file:
            index, value = line.strip().split(",")
            mapping[index] = value
    return mapping

uuid_map = read_map_file(UUID_MAP_FILE)
hash_map = read_map_file(HASH_MAP_FILE)
name_map = read_map_file(NAME_MAP_FILE)

# 讀取已下載文件
if os.path.exists(OK_FILE):
    with open(OK_FILE, "r", encoding="utf-8") as file:
        downloaded_files = set(line.strip() for line in file)
else:
    downloaded_files = set()

# 下載文件
def download_file(url, save_path):
    os.makedirs(os.path.dirname(save_path), exist_ok=True)  # 確保目錄存在
    response = requests.get(url, stream=True)
    if response.status_code == 200:
        with open(save_path, "wb") as file:
            for chunk in response.iter_content(1024):
                file.write(chunk)
        return True
    return False

# 遍歷 UUID 並下載對應文件
for index, uuid in uuid_map.items():
    if index in hash_map and index in name_map:
        folder = uuid[:2]  # 取 UUID 前兩位作為文件夾
        hash_value = hash_map[index]
        filename = name_map[index].replace("\"", "") + ".jpg"
        save_path = os.path.join(DOWNLOAD_FOLDER, filename)
        url = f"{BASE_URL}/{folder}/{uuid}.{hash_value}.jpg"
        
        if save_path in downloaded_files:
            print(f"跳過: {filename} 已下載")
            continue
        
        print(f"下載: {url} -> {save_path}")
        if download_file(url, save_path):
            with open(OK_FILE, "a", encoding="utf-8") as file:
                file.write(f"{save_path}\n")
            print(f"成功: {filename}")
        else:
            print(f"失敗: {filename}")

print("所有下載任務完成！")
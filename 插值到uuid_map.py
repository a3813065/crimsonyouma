# 讀取 uuid_map.txt
with open("uuid_map.txt", "r", encoding="utf-8") as file:
    lines = file.readlines()

# 在 651 行插入新值
new_index = 4509
insert_position = 4509  # 651 行的索引位置是 650（索引從 0 開始）

# 插入新條目，並將後面的條目往後移
lines.insert(insert_position, f"{new_index},0\n")

# 更新行的索引
for i in range(insert_position + 1, len(lines)):
    current_index, value = lines[i].strip().split(",")
    new_index = int(current_index) + 1
    lines[i] = f"{new_index},{value}\n"

# 寫回文件
with open("uuid_map.txt", "w", encoding="utf-8") as file:
    file.writelines(lines)

print("更新 uuid_map.txt 完成")

import pandas as pd
import glob

# Đường dẫn tới các tệp CSV cần gộp
file_paths = ['mal1_table.csv', 'mal2_table.csv', 'mal4_table.csv', 'mal5_table.csv']

# Tạo danh sách để lưu trữ các DataFrame từ các tệp CSV
data_frames = []

# Đọc từng tệp CSV và lưu trữ vào danh sách
for file_path in file_paths:
    df = pd.read_csv(file_path)
    data_frames.append(df)

# Gộp các DataFrame thành một DataFrame duy nhất
merged_df = pd.concat(data_frames)

# Ghi kết quả gộp ra tệp CSV mới
merged_df.to_csv('mal_infor.csv', index=False)
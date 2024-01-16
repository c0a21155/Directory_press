import os
import datetime
import pandas as pd
import csv

def get_directory_age(directory_path):
    try:
        # ディレクトリの最終修正日時を取得
        modification_time = os.path.getmtime(directory_path)

        # 現在の日時を取得
        current_time = datetime.datetime.now().timestamp()

        # 経過した秒数から日数に変換
        age_in_days = (current_time - modification_time) / (60 * 60 * 24)

        return age_in_days
    except FileNotFoundError:
        print(f"Directory not found: {directory_path}")
        return None

if __name__ == "__main__":
    target_directory = "/home/ken/test"
    csv_file = "/home/ken/important_csv/count.csv"
    csv_file2 = "/home/ken/important_csv/実験.csv"  # CSVファイルのパスを指定

    # CSVファイルを読み込み
    with open(csv_file, encoding='utf8', newline='') as f:
        reader = csv.reader(f, delimiter='\t')
        data_list = [row[0].split(',') for row in reader]

    directory_data = []

    for data in data_list:
        dir_name = data[0]
        dir_path = os.path.join(target_directory, dir_name)
        print(f"Checking directory: {dir_path}")

        if os.path.isdir(dir_path):
            age_in_days = get_directory_age(dir_path)
            print(f"Age in days for {dir_name}: {age_in_days}")

            if age_in_days is not None:
                access_count = int(data[1])
                update_count = int(data[2])

                # (アクセス回数 + 更新回数) / ディレクトリが作成されてからの日数を計算
                if round(age_in_days) != 0:
                    ratio = round((access_count + update_count) / round(age_in_days), 3)
                else:
                    # ゼロで割り算を避けるための適切な処理をここに追加する
                    # 例えば、エラーメッセージを表示してプログラムを終了するなど
                    ratio = 0

                # 辞書にデータを追加
                directory_data.append({
                    "Directory": dir_name,
                    "Age (days)": round(age_in_days),
                    "Access Count": access_count,
                    "Update Count": update_count,
                    "Ratio": ratio
                })
            else:
                print(f"Skipping {dir_name} due to missing age information.")
        else:
            print(f"Directory not found: {dir_path}")

    # directory_data を Ratio の値でソート
    sorted_data = sorted(directory_data, key=lambda x: x['Ratio'])

    # Pandas DataFrameに変換
    result_df = pd.DataFrame(directory_data)

    # ソートしたデータを DataFrame に変換   
    sorted_df = pd.DataFrame(sorted_data)

    # 結果を表示
    print(result_df)
    print("-" * 20)
    # print(directory_data)
    for s_data in sorted_data:
        print(s_data)
    print("-" * 20)

    # Directory_ratio_valuesにディレクトリ名とRatioの辞書を取り出す
    Directory_ratio_values = [{'Directory': s_data['Directory'], 'Ratio': s_data['Ratio']} for s_data in sorted_data]

    # 'Directory'と'Ratio'の値を表示
    for directory_ratio in Directory_ratio_values:
        print(f"{directory_ratio['Directory']}|{directory_ratio['Ratio']}")
    print("-" * 20)

   # 新しいDataFrameを作成
    result_df = pd.DataFrame(Directory_ratio_values, columns=['Directory', 'Ratio'])

    # CSVファイルに書き込み (mode='w'で新規書き込み)
    result_df.to_csv(csv_file2, mode='w', header=True, index=False, encoding='utf-8', sep='\t')





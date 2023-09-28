import pandas as pd
import sys

def get_cell_value(csv_file_path, row_number, column_number):
    try:
        df = pd.read_csv(csv_file_path)

        if row_number < 0 or row_number >= len(df) or column_number < 0 or column_number >= len(df.columns):
            print("Ошибка: Некорректные номера строки или столбца.")
            return

        cell_value = df.iloc[row_number-1, column_number-1]
        print(f"Значение ячейки ({row_number}, {column_number}): {cell_value}")

    except Exception as e:
        print(f"Произошла ошибка: {str(e)}")

if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Укажите путь к файлу, номер строки и номер столбца")
    else:
        csv_file_path = sys.argv[1]
        row_number = int(sys.argv[2])
        column_number = int(sys.argv[3])
        get_cell_value(csv_file_path, row_number, column_number)

import pandas as pd
import sqlite3
from classifier import MockProvider
from  db import tao_bang, luu_giao_dich, xoa_du_lieu_cu

def main():
    tao_bang("classifier.db")
    xoa_du_lieu_cu("classifier.db")
    provider = MockProvider()

    df = pd.read_csv("giao_dich_chua_phan_loai.csv")

    for index, row in df.iterrows():
        # TODO: bạn tự viết:
        # 1. Gọi provider.classify(...) với đúng cột description của dòng này
        ket_qua = provider.classify(row["description"])
        # 2. Gọi luu_giao_dich(...) để lưu date, description, amount, và kết quả phân loại vào database
        luu_giao_dich("classifier.db", row["date"], row["description"], row["amount"], ket_qua)

    print("Đã xử lý xong", len(df), "giao dịch")

if __name__ == "__main__":
    main()
    conn = sqlite3.connect("classifier.db")
    cur = conn.cursor()
    cur.execute("SELECT * FROM transactions")
    for row in cur.fetchall():
        print(row)
    conn.close()    



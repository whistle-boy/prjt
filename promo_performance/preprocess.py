# 3. 데이터 전처리
import pandas as pd


def preprocess(df):
    # 작업용 df를 선언한다.
    df = df[
        [
            "create_date",
            "pid_id",
            "count",
            "orders_id",
            "price",
            "sid_id",
            "price_sum",
            "product_cate",
            "rawname",
        ]
    ]

    # dt.normalize()
    df["create_date"] = df.create_date.dt.normalize()
    # create_date -> "order_date"로 컬럼명을 변경한다.
    df.rename({"create_date": "order_date"}, axis=1, inplace=True)

    return df

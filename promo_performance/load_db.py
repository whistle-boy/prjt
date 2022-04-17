# 2. db 데이터 로드
import mysql.connector
import pandas as pd
from xbarx_connection_setting import connection_setting


def load_db(date_promo_start, date_promo_end):
    cnx = mysql.connector.connect(**connection_setting)
    # cursor(commander) 객체를 가져온다.
    cursor = cnx.cursor()

    # query를 선언한다.
    # 주문일 -> from (promo - 2개월) to (promo + 1개월)
    # 가입일 -> from (promo - 1개월)

    order_start = date_promo_start - pd.Timedelta(days=60)  # 주문일
    order_end = date_promo_end + pd.Timedelta(days=30)  # 주문일
    registration = date_promo_start - pd.Timedelta(days=30)  # 가입일

    qry = f"""
    SELECT
        ro.*,
        xms.product_cate,
        xms.rawname
    FROM
        ople.rest_order ro
    JOIN ople.rest_store rs ON
        ro.sid_id = rs.id
    JOIN prd_master2.xprd_master_source xms ON
        ro.pid_id = xms.pid
    WHERE
        ro.create_date BETWEEN '{order_start}' AND '{order_end}'
        AND ro.is_sid_temp = 0
        AND ro.status = 'Done'
        AND rs.is_statistics = 1
        AND rs.is_test = 0
        AND rs.create_date < '{registration}'
    """

    # df로 만든다.
    df = pd.read_sql(qry, cnx)
    # db 연결을 닫는다.
    cnx.close()

    # return db 파일
    return df

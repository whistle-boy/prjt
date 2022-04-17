# 1. promo csv 데이터 로드
import calendar
from datetime import date, timedelta
import pandas as pd


def load_csv(file, year, month):
    promo = pd.read_excel(file)
    date_promo_start = date(year=year, month=month, day=1)  # target month 시작일
    days_in_month = timedelta(
        calendar.monthrange(date_promo_start.year, date_promo_start.month)[1]
    )
    # days in target month
    date_promo_end = date_promo_start + days_in_month  # target month 종료일
    # return -> (promo 시작일, promo 종료일, promo csv 파일)
    return date_promo_start, date_promo_end, promo


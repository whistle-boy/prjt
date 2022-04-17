import pandas as pd
from tqdm import tqdm

# list of dicts
def calculate(promo, df):
    data = []
    for index, pid_ori in tqdm(enumerate(promo["기존 pid"].drop_duplicates())):
        data.append(dict())
        d = data[index]
        d["pid_ori"] = pid_ori
        # pid_promo는 list에 넣어야 한다. -> pid_promo가 pid_ori별 1~3개씩 있기 때문이다.
        pid_promo = promo[promo["기존 pid"] == pid_ori]["프로모션용 pid"].tolist()
        d["pid_promo"] = pid_promo
        for columns, key in (
            ("product_cate", "cate"),
            ("rawname", "name"),
        ):
            try:
                value = df[df["pid_id"] == pid_ori][columns].values[0]
                d[key] = value
            except:
                d[key] = None
        try:
            # 기간을 정의한다. -> promo excel sheet를 참조한다.
            # promo
            date_promo_start = promo[promo["기존 pid"] == pid_ori]["시작일"].iloc[0]
            d["date_promo_start"] = date_promo_start
            date_promo_end = promo[promo["기존 pid"] == pid_ori]["종료일"].iloc[0]
            d["date_promo_end"] = date_promo_end
            date_promo_duration = (
                date_promo_end - date_promo_start + pd.Timedelta(days=1)
            )
            d["date_promo_duration"] = date_promo_duration

            # promo 전
            date_prev_end = date_promo_start
            d["date_prev_end"] = date_prev_end
            date_prev_start = date_prev_end - date_promo_duration
            d["date_prev_start"] = date_prev_start

            # promo 후
            date_next_start = date_promo_end
            d["date_next_start"] = date_next_start
            date_next_end = date_next_start + date_promo_duration
            d["date_next_end"] = date_next_end

            # func1 : pid별 판매량|판매액의 변화를 구한다.
            # promo 전 quantity
            qty_prev = df[
                (df["order_date"] >= date_prev_start)
                & (df["order_date"] <= date_prev_end)
                & (df["pid_id"] == pid_ori)
            ]["count"].sum()
            d["qty_prev"] = qty_prev

            # promo quantity
            qty_promo = df[
                (df["order_date"] >= date_promo_start)
                & (df["order_date"] <= date_promo_end)
                & (df["pid_id"].isin(pid_promo))
            ]["count"].sum()
            d["qty_promo"] = qty_promo

            # promo 후 quantity
            qty_next = df[
                (df["order_date"] > date_next_start)
                & (df["order_date"] <= date_next_end)
                & (df["pid_id"] == pid_ori)
            ]["count"].sum()
            d["qty_next"] = qty_next

            # prev revenue
            rev_prev = df[
                (df["order_date"] >= date_prev_start)
                & (df["order_date"] < date_prev_end)
                & (df["pid_id"] == pid_ori)
            ]["price_sum"].sum()
            d["rev_prev"] = rev_prev
            # promo revenue
            rev_promo = df[
                (df["order_date"] >= date_promo_start)
                & (df["order_date"] <= date_promo_end)
                & (df["pid_id"].isin(pid_promo))
            ]["price_sum"].sum()
            d["rev_promo"] = rev_promo
            # next quantity
            rev_next = df[
                (df["order_date"] > date_next_start)
                & (df["order_date"] <= date_next_end)
                & (df["pid_id"] == pid_ori)
            ]["price_sum"].sum()
            d["rev_next"] = rev_next

            # 4-2. func2 : pid별 가격 민감도를 구한다.
            # prev cate revenue
            rev_prev_cate = df[
                (df["order_date"] >= date_prev_start)
                & (df["order_date"] < date_prev_end)
                & (df["product_cate"] == d["cate"])
            ]["price_sum"].sum()
            d["rev_prev_cate"] = rev_prev_cate
            # promo cate revenue
            rev_promo_cate = df[
                (df["order_date"] >= date_promo_start)
                & (df["order_date"] <= date_promo_end)
                & (df["product_cate"] == d["cate"])
            ]["price_sum"].sum()
            d["rev_promo_cate"] = rev_promo_cate
            # next cate revenue
            rev_next_cate = df[
                (df["order_date"] > date_next_start)
                & (df["order_date"] <= date_next_end)
                & (df["product_cate"] == d["cate"])
            ]["price_sum"].sum()
            d["rev_next_cate"] = rev_next_cate

            # 4-3. func3 : pid_cate별 경쟁력을 구한다.
            # 기존고객 : promo 전(from - 1개월)에도 이미 pid_cate를 구매한 sid
            list_sid_ori = (
                df[
                    (df["order_date"] >= date_prev_start)
                    & (df["order_date"] < date_prev_end)
                    & (df["product_cate"] == d["cate"])
                ]["sid_id"]
                .drop_duplicates()
                .tolist()
            )
            d["sid_ori_count"] = len(list_sid_ori)
            # 유입고객 : 기존고객을 제외한 고객 중에서 pid를 구매한 sid
            # <- promo 전에는 pid_cate를 구매한 적이 없다.
            list_sid_new = (
                df[
                    (df["order_date"] >= date_promo_start)
                    & (df["order_date"] <= date_promo_end)
                    & (df["pid_id"].isin(pid_promo))
                    & (~df["sid_id"].isin(list_sid_ori))
                ]["sid_id"]
                .drop_duplicates()
                .tolist()
            )
            d["sid_new_count"] = len(list_sid_new)
            # 잔존고객 : promo 후(from + 1개월)에도 pid_cate를 구매하는 sid
            list_sid_left = (
                df[
                    (df["order_date"] > date_next_start)
                    & (df["order_date"] <= date_next_end)
                    & (df["product_cate"] == d["cate"])
                    & (df["sid_id"].isin(list_sid_new))
                ]["sid_id"]
                .drop_duplicates()
                .tolist()
            )
            d["sid_left_count"] = len(list_sid_left)

        except:
            d["cate"] = None
            d["name"] = None
            d["date_promo_start"] = None
            d["date_promo_end"] = None
            d["date_promo_duration"] = None
            d["date_prev_end"] = None
            d["date_prev_start"] = None
            d["date_next_start"] = None
            d["date_next_end"] = None
            d["qty_prev"] = None
            d["qty_promo"] = None
            d["qty_next"] = None
            d["rev_prev"] = None
            d["rev_promo"] = None
            d["rev_next"] = None
            d["rev_promo_cate"] = None
            d["rev_prev_cate"] = None
            d["rev_next_cate"] = None
            d["sid_ori_count"] = None
            d["sid_new_count"] = None
            d["sid_left_count"] = None

    return data


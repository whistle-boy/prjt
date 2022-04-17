import load_csv
import load_db
import preprocess
import calculate
import report


def execute(load_csv, load_db, preprocess, calculate, report):
    date_promo_start, date_promo_end, promo = load_csv(file, year, month)
    df_ori = load_db(date_promo_start, date_promo_end)
    df = preprocess(df_ori)
    df = calculate(promo, df)
    return report(df)


# file, year, month을 입력해야 작동합니다.

if __name__ == "__main__":
    execute(
        load_csv.load_csv(file, year, month),
        load_db.load_db,
        preprocess.preprocess,
        calculate.calculate,
        report.report,
    )
# function() -> ()는 실행의 의미를 가진다.

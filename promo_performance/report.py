# 5. report 저장
import pandas as pd


def report(data):
    report = pd.DataFrame(data)
    report.to_excel("./report/report_21-06.xlsx")

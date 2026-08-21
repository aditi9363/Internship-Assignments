import pandas as pd
import sweetviz as sv

df = pd.read_csv("Master_DF.csv")

report = sv.analyze(df)

report.show_html(
    "profiling_report.html",
    open_browser=True
)

print("=" * 60)
print("Sweetviz EDA Profiling Report Generated Successfully!")
print("Output File: profiling_report.html")
print("=" * 60)
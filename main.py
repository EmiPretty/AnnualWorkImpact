import pandas as pd

def get_clean_work_time(work_time_path):
    return (
        pd.read_csv(work_time_path, sep=";", encoding="utf-8")
        .drop_duplicates()
        .fillna(
            {
                "Temps annuel de travail (SNCF)": 0,
                "Temps annuel de travail (France)": 0,
                "Commentaires": "",
            }
        )
        .astype(
            {
                "Date": int,
                "Temps annuel de travail (SNCF)": int,
                "Temps annuel de travail (France)": int,
            }
        )
        .assign(Commentaires=lambda x: x["Commentaires"].str.strip())
    )

def get_interesting_columns(df, columns):
    missing_columns = [col for col in columns if col not in df.columns]
    if missing_columns:
        print(f"Colonnes manquantes : {missing_columns}")
        return pd.DataFrame()
    return df[columns]

def filter_work_time_rows(df):
    return df[df["Date"].isin([2017, 2018])]

def filter_frequentation_rows(df):
    filtered_df = df[df["Code postal"].astype(str).str.startswith("7")]
    return filtered_df.head(3)

work_time_file = get_clean_work_time("data/temps-de-travail-annuel-depuis-1851.csv")
frequentation_file = pd.read_csv("data/frequentation-gares.csv", sep=";")

work_time_columns = ["Date", "Temps annuel de travail (SNCF)", "Temps annuel de travail (France)"]
frequentation_columns = [
    "Nom de la gare",
    "Code postal",
    "Total Voyageurs + Non voyageurs 2017",
    "Total Voyageurs + Non voyageurs 2018",
]

work_time_filtered_columns = get_interesting_columns(work_time_file, work_time_columns)
frequentation_filtered_columns = get_interesting_columns(frequentation_file, frequentation_columns)

work_time_final = filter_work_time_rows(work_time_filtered_columns)
frequentation_final = filter_frequentation_rows(frequentation_filtered_columns)

print(work_time_final)
print(frequentation_final)

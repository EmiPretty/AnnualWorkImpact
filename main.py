import pandas as pd
import matplotlib.pyplot as plt

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
    return df[(df["Date"] >= 2014) & (df["Date"] <= 2018)]

def filter_frequentation_rows(df):
    return df.head(10)

def get_frequentation_diagram(frequentation):
    frequentation_df = pd.DataFrame(frequentation)
    frequentation_df.set_index('Nom de la gare')[
        ['Total Voyageurs + Non voyageurs 2017', 'Total Voyageurs + Non voyageurs 2018']
    ].plot(kind='bar', figsize=(12, 6))
    plt.title('Comparaison fréquentation des gares entre 2017 et 2018')
    plt.ylabel('Total voyageurs')
    plt.xlabel('Nom de la gare')
    plt.xticks(rotation=45)
    plt.grid(axis='y')
    plt.legend(title="Année")
    plt.savefig("frequentation_comparaison.png")
    plt.show()

def get_time_series_diagram(work_time):
    plt.figure(figsize=(10, 6))
    plt.plot(work_time["Date"], work_time["Temps annuel de travail (SNCF)"], label="SNCF", color="blue")
    plt.plot(work_time["Date"], work_time["Temps annuel de travail (France)"], label="France", color="red")
    
    plt.title("Courbes temporelles du temps de travail annuel")
    plt.xlabel("Année")
    plt.ylabel("Temps de travail annuel (en heures)")
    plt.legend()
    plt.grid(True)
    
    plt.savefig("courbes_temporelles.png")
    plt.show()

work_time_file = get_clean_work_time("data/temps-de-travail-annuel-depuis-1851.csv")
frequentation_file = pd.read_csv("data/frequentation-gares.csv", sep=";")

work_time_columns = [
    "Date", 
    "Temps annuel de travail (SNCF)", 
    "Temps annuel de travail (France)",
]

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

print("WORK TIME")
print(work_time_final)
print("\n\n\n")
print("FREQUENTATION")
print(frequentation_final)

get_frequentation_diagram(frequentation_final)
get_time_series_diagram(work_time_final)

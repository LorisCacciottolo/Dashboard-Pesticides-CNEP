import numpy as np
import pandas as pd


def clean_and_merge(df_sites, df_conc):
    df = df_conc.copy()
    sites = df_sites.copy()

    ## Conversion of the date and extraction of the month to see the time evolution.
    df["date_debut"] = pd.to_datetime(df["date de début de prélèvement"], errors="coerce")
    df["mois_annee"] = df["date_debut"].dt.to_period("M").astype(str)

    ## Clearer name for the different substances so that they are easier to read on the graphs
    df["substance_courte"] = (df["substance"].astype(str).str.replace(" total (phase gazeuse + particulaire dans les PM10)", "", regex=False).str.strip())

   ## To avoid having noise, we only keep strictly quantified measurements. For any value below the threshold (< LQ or < LD), we set the real concentration to 0.0 ng/m³.
    df["statut_mesure"] = df["quantification"].fillna("Quantifié").astype(str).str.strip()
    df["est_quantifie"] = ~df["statut_mesure"].isin(["< LQ", "< LD"])

    ## Here if the concentration is below to the threshold, we set it to 0 ng/m3
    df["valeur brute"] = pd.to_numeric(df["valeur brute"], errors="coerce").fillna(0.0)
    df["conc_reelle"] = np.where(df["est_quantifie"], df["valeur brute"], 0.0)

    ## We merge the concentration and site tables on 'code site'
    colonnes_sites = [
        "code site",
        "latitude",
        "longitude",
        "typologie du site",
        "culture dominante autour du site",
        "distance à la parcelle la plus proche (m)",
        "nombre d'habitants résidant dans un rayon de 5 km autour du site",
    ]
    sites_reduit = sites[colonnes_sites].drop_duplicates(subset=["code site"])

    df_final = pd.merge(df, sites_reduit, on="code site", how="left")

    ## We finally rename the main columns to have a lighter display
    df_final = df_final.rename(
        columns={
            "nom de la région": "region",
            "nom du département": "departement",
            "nom site": "nom_site",
            "typologie du site": "typologie",
            "culture dominante autour du site": "culture_dominante",
            "distance à la parcelle la plus proche (m)": "distance_parcelle_m",
            "nombre d'habitants résidant dans un rayon de 5 km autour du site": "pop_5km",
        }
    )

    df_final["typologie"] = df_final["typologie"].astype(str).str.strip()
    df_final["culture_dominante"] = df_final["culture_dominante"].astype(str).str.strip()

    return df_final
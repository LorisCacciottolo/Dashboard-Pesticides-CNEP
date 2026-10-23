import streamlit as st
from utils.io import load_data
from utils.prep import clean_and_merge
from sections.intro import show_intro
from sections.overview import show_overview
from sections.deep_dives import show_deep_dives
from sections.conclusions import show_conclusions

st.set_page_config(
    page_title="Data Storytelling: Pesticides in Ambient Air",
    layout="wide",
)

st.title("Surveillance of Pesticide Residues in Ambient Air (France)")
st.caption(
    "Source: National Exploratory Campaign for Pesticides (CNEP 2018-2019) — "
    "LCSQA / Ineris / Anses / Atmo France | Open License (Etalab 2.0)"
)


df_sites, df_conc = load_data()
df = clean_and_merge(df_sites, df_conc)

# Sidebar Filters
with st.sidebar:
    st.header("Exploration Filters")

    # Filter 1: Region
    toutes_regions = sorted(df["region"].dropna().unique())
    regions_choisies = st.multiselect(
        "Regions:",
        options=toutes_regions,
        default=toutes_regions,
    )

    # Filter 2: Site Typology
    toutes_typos = sorted(df["typologie"].dropna().unique())
    typos_choisies = st.multiselect(
        "Site Typology:",
        options=toutes_typos,
        default=toutes_typos,
    )

    # Filter 3: Dominant Culture
    toutes_cultures = sorted(df["culture_dominante"].dropna().unique())
    cultures_choisies = st.multiselect(
        "Dominant Culture (5 km radius):",
        options=toutes_cultures,
        default=toutes_cultures,
    )

    # Filter 4: Date Range
    date_min = df["date_debut"].min().date()
    date_max = df["date_debut"].max().date()
    plage_dates = st.date_input(
        "Sampling Period:",
        value=(date_min, date_max),
        min_value=date_min,
        max_value=date_max,
    )

# 5. Filter Application
masque = (
    df["region"].isin(regions_choisies)
    & df["typologie"].isin(typos_choisies)
    & df["culture_dominante"].isin(cultures_choisies)
)

if len(plage_dates) == 2:
    debut, fin = plage_dates
    masque = masque & (df["date_debut"].dt.date >= debut) & (df["date_debut"].dt.date <= fin)

df_filtre = df[masque]

show_intro()
st.divider()

if len(df_filtre) == 0:
    st.error("No data matches the selected filters. Please broaden your selection in the left menu.")
else:
    show_overview(df_filtre)
    st.divider()
    show_deep_dives(df_filtre)
    st.divider()
    show_conclusions(df_filtre)
import plotly.express as px


## Monthly evolution of the concentrations by the type of culture
def line_chart_saisonnalite(df):
    df_mois = (
        df.groupby(["mois_annee", "culture_dominante"], as_index=False)["conc_reelle"]
        .mean()
        .sort_values("mois_annee")
    )

    fig = px.line(
        df_mois,
        x="mois_annee",
        y="conc_reelle",
        color="culture_dominante",
        markers=True,
        title="Monthly Evolution of Average Pesticide Concentration (ng/m³)",
        labels={
            "mois_annee": "Sampling Month",
            "conc_reelle": "Average Concentration (ng/m³)",
            "culture_dominante": "Dominant Culture",
        },
    )
    fig.add_vrect(
        x0="2019-04",
        x1="2019-07",
        fillcolor="orange",
        opacity=0.15,
        line_width=0,
        annotation_text="Peak Spraying Season (Spring-Summer)",
        annotation_position="top left",
    )
    return fig


## France map of the sites
def map_chart_sites(df):
    df_carte = (
        df.groupby(
            ["code site", "nom_site", "region", "typologie", "culture_dominante", "latitude", "longitude"],
            as_index=False,
        )
        .agg(
            conc_moyenne=("conc_reelle", "mean"),
            taux_detection=("est_quantifie", lambda x: round(x.mean() * 100, 1)),
        )
        .dropna(subset=["latitude", "longitude"])
    )

    fig = px.scatter_map(
        df_carte,
        lat="latitude",
        lon="longitude",
        color="culture_dominante",
        size="conc_moyenne",
        size_max=22,
        zoom=4.5,
        center={"lat": 46.6, "lon": 2.4},
        map_style="open-street-map",
        hover_name="nom_site",
        hover_data=["region", "typologie", "conc_moyenne", "taux_detection"],
        title="Map of Monitoring Stations (Size = average concentration in ng/m³)",
        labels={
            "culture_dominante": "Dominant Culture",
            "conc_moyenne": "Average (ng/m³)",
            "taux_detection": "% Quantified",
        },
    )
    fig.update_layout(height=500, margin={"r": 0, "t": 40, "l": 0, "b": 0})
    return fig


## Classification of the top substances detected in the air
def bar_chart_top_substances(df, top_n=10):
    df_sub = (
        df.groupby("substance_courte", as_index=False)
        .agg(
            frequence_quantif=("est_quantifie", lambda x: round(x.mean() * 100, 1)),
            conc_moyenne=("conc_reelle", "mean"),
        )
        .sort_values("frequence_quantif", ascending=True)
        .tail(top_n)
    )

    fig = px.bar(
        df_sub,
        x="frequence_quantif",
        y="substance_courte",
        orientation="h",
        color="conc_moyenne",
        title=f"Top {top_n} Most Frequently Quantified Substances in Ambient Air (%)",
        labels={
            "frequence_quantif": "Quantification Frequency (%)",
            "substance_courte": "Active Substance",
            "conc_moyenne": "Avg. Conc. (ng/m³)",
        },
    )
    return fig


## Audit of the data quality
def bar_chart_qualite(df):
    df_qual = (
        df.groupby(["typologie", "statut_mesure"], as_index=False)
        .size()
        .rename(columns={"size": "nombre_mesures"})
    )

    fig = px.bar(
        df_qual,
        x="typologie",
        y="nombre_mesures",
        color="statut_mesure",
        barmode="group",
        title="Distribution of Samples by Laboratory Analytical Thresholds",
        labels={
            "typologie": "Site Typology",
            "nombre_mesures": "Number of Samples",
            "statut_mesure": "Quantification Status",
        },
    )
    return fig
import streamlit as st


def show_intro():
    st.markdown("## 1. Framing the Atmospheric Pesticide Problem")

    st.markdown(
        ">**Hook:** *While pesticide residues are strictly regulated in tap water and food across Europe, "
        "the air we breathe currently has zero binding regulatory thresholds in France.*"
    )

    st.write(
        """
        Every year, tens of thousands of tons of herbicides, fungicides and insecticides are applied across French 
        agricultural basins. Through spray drift during application and secondary volatilization from treated soils 
        and leaves days later, these active substances travel through the atmosphere and go far beyond the boundaries 
        of agricultural plots.

        To analyse this blind spot, Anses, Ineris, LCSQA, and the **Atmo France (AASQA) network 
        launched the National Exploratory Campaign for Pesticides (CNEP) between June 2018 and June 2019. 
        For the first time, 50 monitoring stations sampled ambient air weekly across metropolitan France and 
        overseas territories, tracking 75 active substances.
        """
    )

    col1, col2, col3 = st.columns(3)

    with col1:
        st.info(
            "**Target Audience & Objective**\n\n"
            "This dashboard transforms nearly 100,000 raw laboratory records into an interactive investigation:\n"
            "1. **When** does atmospheric exposure peak?\n"
            "2. **Where** are populations most exposed (and are cities truly safe)?\n"
            "3. **Which** molecules dominate the air we breathe?"
        )

    with col2:
        st.warning(
            "**Sampling Protocol (150m Rule)**\n\n"
            "To measure background ambient exposure rather than direct plume spraying inside a tractor's path, "
            "all 50 CNEP sensors were positioned at least **150 meters away** from the nearest agricultural parcel. "
            "Stations cover diverse environments: **Urban, Peri-urban, and Rural** zones surrounded by vineyards, "
            "arboriculture, or large cereal crops."
        )

    with col3:
        st.error(
            "**Limit of Detection & Limit of Quantification (< LD & < LQ)**\n\n"
            "In trace air chemistry, over 80% of weekly samples fall below the laboratory Limit of Detection (< LD) "
            "or Limit of Quantification (< LQ). However, they still record a mathematical number for them. "
            "To avoid this laboratory noise, we isolate quantified concentrations."
        )
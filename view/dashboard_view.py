import streamlit as st

from controller.dashboard_controller import DashboardController
from view.dashboard_header import render_dashboard_header
from view.dashboard_metriken import render_dashboard_metriken
from view.dashboard_kurse import (
    render_module_in_bearbeitung,
    render_offene_module,
    render_abgeschlossene_module,
)


def render(controller: DashboardController) -> None:
    """
    Rendert die komplette Dashboard-Seite: Header, Metriken und Modul-Listen
    """
    _render_page_style()

    daten = controller.lade_dashboard_daten()

    studium = daten["studium"]
    module_in_bearbeitung = daten["module_in_bearbeitung"]
    offene_module = daten["offene_module"]
    abgeschlossene_module = daten["abgeschlossene_module"]

    if studium is None:
        st.info("Bitte unter \"Studium & Module\" → \"Stammdaten Studium\" ein Studium erfassen")
        return

    render_dashboard_header(studium)

    if "notendurchschnitt" in daten and "gesamt_ects_bestanden" in daten:
        render_dashboard_metriken(
            studium=studium,
            notendurchschnitt=daten["notendurchschnitt"],
            gesamt_ects_bestanden=daten["gesamt_ects_bestanden"],
            voraussichtliches_enddatum=daten["voraussichtliches_enddatum"],
            ects_pro_semester=daten["ects_pro_semester"]
        )

    render_module_in_bearbeitung(
        controller=controller,
        module_in_bearbeitung=module_in_bearbeitung,
    )

    st.markdown("")

    col_links, col_rechts = st.columns(2)

    with col_links:
        render_offene_module(
            controller=controller,
            offene_module=offene_module,
        )

    with col_rechts:
        render_abgeschlossene_module(
            abgeschlossene_module=abgeschlossene_module,
        )


def _render_page_style() -> None:
    """Anpassung der Layout Einstellungen in Streamlit"""
    st.markdown("""
    <style>
        .block-container {
            max-width: 100%;
            padding-left: 2rem;
            padding-right: 2rem;
            padding-top: 3rem;
        }
    </style>
    """, unsafe_allow_html=True)
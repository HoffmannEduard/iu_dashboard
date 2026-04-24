from datetime import date

import streamlit as st

from controller.eingabe_controller import EingabeController
from models.enums import Studienabschluss, Zeitmodell


def render(controller: EingabeController) -> None:
    """
    Rendert die Eingabe-Elemente für Modul- und Studium-Eingabe, sowie Informationen über Fehleingaben
    """
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

    st.title("Studium & Module")

    # Module-Eingabe
    with st.container(border=True):
        st.subheader("Modul hinzufügen")

        col1, col2= st.columns(2)
        # Modul-Code
        with col1:
            modul_code = st.text_input("Modulcode")
        # Modul-ECTS
        with col2:
            ects = st.number_input(
                "ECTS",
                min_value=1,
                step=1,
                value=5
            )

        modul_titel = st.text_input("Modultitel")

        st.markdown("")

        if st.button("Modul speichern", use_container_width=True):
            try:
                controller.speichere_modul(
                    modul_code=modul_code,
                    modul_titel=modul_titel,
                    ects=ects
                )
                st.success("Modul wurde gespeichert.")
            except Exception as e:
                st.error(str(e))

    # Studium-Eingabe
    with st.container(border=True):
        st.subheader("Stammdaten Studium")

        col1, col2, col3 = st.columns(3)
        # Studiengang
        with col1:
            studiengang = st.text_input("Studiengang")
        # Studienabschluss
        with col2:
            studienabschluss = st.selectbox(
                "Studienabschluss",
                options=list(Studienabschluss),
                format_func=lambda x: x.value
            )
        # Gesamt-ECTS des Studiums
        with col3:
            gesamt_ects = st.number_input(
                "Gesamt-ECTS",
                min_value=1,
                step=1,
                value=180
            )

        col4, col5 = st.columns(2)
        # Startdatum des Studiums
        with col4:
            startdatum = st.date_input("Startdatum", value=date.today())
        # Wahl des Zeitmodells (Enum)
        with col5:
            zeitmodell = st.selectbox(
                "Zeitmodell",
                options=list(Zeitmodell),
                format_func=lambda x: x.value
            )

        st.markdown("")

        if st.button("Studium speichern", use_container_width=True):
            try:
                controller.speichere_studium(
                    studiengang=studiengang,
                    studienabschluss=studienabschluss,
                    startdatum=startdatum,
                    zeitmodell=zeitmodell,
                    gesamt_ects=gesamt_ects
                )
                st.success("Studium wurde gespeichert.")
            except Exception as e:
                st.error(str(e))
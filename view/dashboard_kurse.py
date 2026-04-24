import streamlit as st

from controller.dashboard_controller import DashboardController
from models.enums import Pruefungsart


def render_module_in_bearbeitung(
    controller: DashboardController,
    module_in_bearbeitung: list
) -> None:
    """
    Rendert alle Module, die sich aktuell in Bearbeitung befinden,
    inklusive Eingabefeldern zur Erfassung der Prüfungsleistung und Abschluss Aktion.
    """
    with st.container(border=True):
        st.subheader("Gestartete Kurse")

        if not module_in_bearbeitung:
            st.info("Es befinden sich aktuell keine Module in Bearbeitung.")
            return

        for buchung in module_in_bearbeitung:
            modul = buchung.modul

            st.markdown("")

            col1, col2, col3, col4, col5, col6 = st.columns([2, 3, 1, 2, 2, 2])

            # Modul-Code
            with col1:
                st.write(f"**{modul.modul_code}**")
            # Modul-Titel
            with col2:
                st.write(modul.modul_titel)
            # Modul-ECTS
            with col3:
                st.write(f"{modul.ects} ECTS")
            # Prüfungsart (Enum)
            with col4:
                pruefungsart = st.selectbox(
                    "Prüfungsart",
                    options=list(Pruefungsart),
                    format_func=lambda x: x.value,
                    key=f"pruefungsart_{buchung.id}"
                )
            # Note
            with col5:
                note = st.number_input(
                    "Note",
                    min_value=1.0,
                    max_value=5.0,
                    step=0.1,
                    key=f"note_{buchung.id}"
                )
            # Abschließen-Button
            with col6:
                st.write("")
                st.write("")
                if st.button("Abschließen", key=f"abschliessen_{buchung.id}"):
                    try:
                        controller.modul_abschliessen(
                            modulbuchung_id=buchung.id,
                            pruefungsart=pruefungsart,
                            note=note
                        )
                        st.success(f"Modul '{modul.modul_titel}' wurde abgeschlossen.")
                        st.rerun()
                    except ValueError as e:
                        st.error(str(e))


def render_offene_module(
    controller: DashboardController,
    offene_module: list
) -> None:
    """Rendert alle offenen Module und ermöglicht das Starten oder Löschen eines Moduls"""
    with st.container(border=True):
        st.subheader("Offene Module")

        if not offene_module:
            st.info("Es sind keine offenen Module vorhanden.")
            return

        for modul in offene_module:
            col1, col2, col3, col4, col5 = st.columns([2, 5, 2, 2, 2])
            # Modul-Code
            with col1:
                st.write(f"**{modul.modul_code}**")
            # Modul-Titel
            with col2:
                st.write(modul.modul_titel)
            # Modul-ECTS
            with col3:
                st.write(f"{modul.ects} ECTS")
            # Modul-Starten-Button
            with col4:
                if st.button("Start", key=f"start_modul_{modul.id}"):
                    try:
                        controller.modul_starten(modul.id)
                        st.rerun()
                    except ValueError as e:
                        st.error(str(e))
            # Löschen Button
            with col5:
                if st.button("❌", key=f"delete_modul_{modul.id}"):
                    try:
                        controller.modul_loeschen(modul.id)
                        st.rerun()
                    except ValueError as e:
                        st.error(str(e))


def render_abgeschlossene_module(abgeschlossene_module: list) -> None:
    """Rendert Rendert alle abgeschlossenen Module, inkl. Anzeige der Prüfungsleistung"""
    with st.container(border=True):
        st.subheader("Abgeschlossene Module")

        if not abgeschlossene_module:
            st.info("Es sind noch keine Module abgeschlossen.")
            return

        for buchung in abgeschlossene_module:
            modul = buchung.modul
            pruefungsleistung = buchung.pruefungsleistung

            col1, col2, col3 = st.columns([2, 5, 2])
            # Modul-Code
            with col1:
                st.write(f"**{modul.modul_code}**")
            # Prüfungsleistung
            with col2:
                st.write(modul.modul_titel)

                if pruefungsleistung is not None:
                    st.caption(
                        f"{pruefungsleistung.pruefungsart.value} • "
                        f"Note: {pruefungsleistung.note}"
                    )
            # Erreichte ECTS
            with col3:
                st.write(f"{modul.ects} ECTS")
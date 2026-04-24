import streamlit as st

from database.db import create_connection, create_tables
from repositories.modul_repository import ModulRepository
from repositories.modulbuchung_repository import ModulbuchungRepository
from repositories.studium_repository import StudiumRepository
from controller.eingabe_controller import EingabeController
from controller.dashboard_controller import DashboardController
from services.dashboard_metriken_service import DashboardMetrikenService
from services.validierungs_service import ValidierungsService
from services.modul_verwaltungs_service import ModulVerwaltungsService
from view.eingabe_view import render as render_eingabe_view
from view.dashboard_view import render as render_dashboard_view


def get_connection():
    if "db_conn" not in st.session_state:
        conn = create_connection()
        create_tables(conn)
        st.session_state["db_conn"] = conn
    return st.session_state["db_conn"]


def main() -> None:
    conn = get_connection()

    # Initialisierung der Repositories
    studium_repo = StudiumRepository(conn)
    modul_repo = ModulRepository(conn)
    buchung_repo = ModulbuchungRepository(
        conn, 
        studium_repository=studium_repo,
        modul_repository=modul_repo
        )

    # Initialisierung der Services
    validierungsservice = ValidierungsService()
    modulverwaltungsservice = ModulVerwaltungsService(
        modul_repository=modul_repo,
        modulbuchung_repository=buchung_repo
        )
    dashboardmetrikenservice = DashboardMetrikenService(
        modulbuchung_repository=buchung_repo
    )

    # Initialisierung der Controller
    eingabe_controller = EingabeController(
        studium_repository=studium_repo,
        modul_repository=modul_repo,
        validierungsservice=validierungsservice
        )
    
    dashboard_controller = DashboardController(
        studium_repository=studium_repo,
        modul_verwaltungs_service=modulverwaltungsservice,
        dashboard_metriken_service=dashboardmetrikenservice
        )

    # Aufrufen der Streamlit Anwendung
    seite = st.sidebar.radio(
        "Navigation",
        ["Dashboard", "Studium & Module"]
    )

    if seite == "Dashboard":
        render_dashboard_view(dashboard_controller)
    else:
        render_eingabe_view(eingabe_controller)


if __name__ == "__main__":
    main()
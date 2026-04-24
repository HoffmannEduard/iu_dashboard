from repositories.studium_repository import StudiumRepository
from services.dashboard_metriken_service import DashboardMetrikenService
from services.modul_verwaltungs_service import ModulVerwaltungsService


class DashboardController:
    """Lädt und zeigt Module und berechnete, studienabhängige Metriken"""
    def __init__(
        self,
        studium_repository: StudiumRepository,
        modul_verwaltungs_service: ModulVerwaltungsService,
        dashboard_metriken_service: DashboardMetrikenService
    ):
        self.studium_repository = studium_repository
        self.modul_verwaltungs_service = modul_verwaltungs_service
        self.dashboard_metriken_service = dashboard_metriken_service

    def lade_dashboard_daten(self) -> dict:
        """
        Lädt die Daten zur Anzeige auf dem Dashboard. 

        Returns:
            Studium,
            Drei Listen: Offene Module, Module in Bearbeitung und Abgeschlossene Module. 
            Relevante Metriken zum Studium: Notendurchschnitt, bisher erreichte ECTS,
            vorraussichtliches Enddatum und die durchschnittlich erreichten ECTS pro Semester.

        """
        studium = self.studium_repository.lade()

        if studium is None:
            return {
                "studium": None,
                "offene_module": [],
                "module_in_bearbeitung": [],
                "abgeschlossene_module": [],

                "notendurchschnitt": None,
                "gesamt_ects_bestanden": 0,
                "voraussichtliches_enddatum": None,
                "ects_pro_semester": None,
            }
        
        metriken = self.dashboard_metriken_service.berechne_dashboard_metriken(studium)

        return {
            "studium": studium,
            "module_in_bearbeitung": self.modul_verwaltungs_service.lade_module_in_bearbeitung(studium),
            "offene_module": self.modul_verwaltungs_service.lade_offene_module(studium),
            "abgeschlossene_module": self.modul_verwaltungs_service.lade_abgeschlossene_module(studium),

            "notendurchschnitt": metriken["notendurchschnitt"],
            "gesamt_ects_bestanden": metriken["gesamt_ects_bestanden"],
            "voraussichtliches_enddatum": metriken["voraussichtliches_enddatum"],
            "ects_pro_semester": metriken["ects_pro_semester"],
        }

    def modul_starten(self, modul_id: int) -> None:
        """
        Startet ein Modul, das bereits in der Datenbank gespeichert ist. Vorraussetzung: Ein Studium wurde gestartet

        Args:
            Id des Moduls, das gestartet werden soll
        Returns:
            -
        Raises:
            Value Error: Falls noch kein Studium gestartet wurde.
        """
        studium = self.studium_repository.lade()

        if studium is None:
            raise ValueError("Es wurde noch kein Studium erfasst.")

        self.modul_verwaltungs_service.modul_starten(
            studium=studium,
            modul_id=modul_id
        )

    def modul_abschliessen(self, modulbuchung_id, pruefungsart, note) -> None:
        """
        Schließt eine Modulbuchung ab. Speichert dafür eine Prüfungsleistung und setzt den Status auf "Abgeschlossen".

        Args:
            Id der Modulbuchung
            Enum: Prüfungsart
            Note der Prüfungsleistung
        Returns:
            -
        Raises:
            -
        
        """
        self.modul_verwaltungs_service.modul_abschliessen(
            modulbuchung_id=modulbuchung_id,
            pruefungsart=pruefungsart,
            note=note
        )

    def modul_loeschen(self, modul_id: int) -> None:
        """
        Löscht ein Modul. Nur möglich, wenn es noch nicht gestartet wurde.
        
        Args: 
            Id des Moduls
        """
        self.modul_verwaltungs_service.modul_loeschen(modul_id=modul_id)
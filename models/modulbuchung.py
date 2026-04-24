from dataclasses import dataclass
from models.enums import Modulstatus
from models.modul import Modul
from models.pruefungsleistung import Pruefungsleistung
from models.studium import Studium

@dataclass
class Modulbuchung:
    id: int | None
    studium: Studium
    modul: Modul
    status: Modulstatus
    pruefungsleistung: Pruefungsleistung | None = None

    def ist_abgeschlossen(self) -> bool:
        return self.status == Modulstatus.ABGESCHLOSSEN

    def ist_in_bearbeitung(self) -> bool:
        return self.status == Modulstatus.IN_BEARBEITUNG

    def abschliessen(self, pruefungsleistung: Pruefungsleistung) -> None:
        if not self.ist_in_bearbeitung():
            raise ValueError("Nur Module in Bearbeitung können abgeschlossen werden.")

        if not pruefungsleistung.ist_bewertet():
            raise ValueError("Nur bewertete Prüfungsleistungen können abgeschlossen werden.")

        if pruefungsleistung.ist_nicht_bestanden():
            raise ValueError("Ein Modul mit Note 5.0 oder schlechter kann nicht abgeschlossen werden.")

        self.pruefungsleistung = pruefungsleistung
        self.status = Modulstatus.ABGESCHLOSSEN
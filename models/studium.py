from dataclasses import dataclass
from datetime import date
from models.enums import Studienabschluss, Zeitmodell

@dataclass
class Studium:
    id: int | None
    studiengang: str
    studienabschluss: Studienabschluss
    startdatum: date
    zeitmodell: Zeitmodell
    gesamt_ects: int

    def __post_init__(self) -> None:
        if not self.studiengang or not self.studiengang.strip():
            raise ValueError("Studiengang darf nicht leer sein")
        
        if self.gesamt_ects <= 0:
            raise ValueError("Gesamt-ECTS muss größer als 0 sein")

    @property
    def enddatum(self) -> date:
        if self.zeitmodell == Zeitmodell.VOLLZEIT:
            jahre = 3
        elif self.zeitmodell == Zeitmodell.TEILZEIT_1:
            jahre = 4
        elif self.zeitmodell == Zeitmodell.TEILZEIT_2:
            jahre = 6
        else:
            raise ValueError("Unbekanntes Zeitmodell")

        return date(self.startdatum.year + jahre,
                    self.startdatum.month,
                    self.startdatum.day)
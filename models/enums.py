from enum import Enum

class Studienabschluss(Enum):
    BACHELOR = "Bachelor"
    MASTER = "Master"


class Zeitmodell(Enum):
    VOLLZEIT = "Vollzeit (6 Semester)"
    TEILZEIT_1 = "Teilzeit 1 (8 Semester)"
    TEILZEIT_2 = "Teilzeit 2 (12 Semester)"


class Modulstatus(Enum):
    IN_BEARBEITUNG = "In Bearbeitung"
    ABGESCHLOSSEN = "Abgeschlossen"


class Pruefungsart(Enum):
    KLAUSUR = "Klausur"
    PROJEKT = "Projekt"
    HAUSARBEIT = "Hausarbeit"
    SONSTIGES = "Sonstiges"
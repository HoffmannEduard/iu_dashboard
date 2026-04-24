from dataclasses import dataclass
from models.enums import Pruefungsart

@dataclass
class Pruefungsleistung:
    pruefungsart: Pruefungsart
    note: float | None = None

    def ist_bewertet(self) -> bool:
        return self.note is not None

    def ist_bestanden(self) -> bool:
        return self.ist_bewertet() and self.note < 5.0

    def ist_nicht_bestanden(self) -> bool:
        return self.ist_bewertet() and self.note >= 5.0
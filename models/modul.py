from dataclasses import dataclass

@dataclass
class Modul:
    id: int | None
    modul_code: str
    modul_titel: str
    ects: int

    def __post_init__(self) -> None:
        if not self.modul_titel or not self.modul_titel.strip():
            raise ValueError("Modultitel darf nicht leer sein")
        
        if not self.modul_code or not self.modul_code.strip():
            raise ValueError("Modulcode darf nicht leer sein")
        
        if self.ects <= 0:
            raise ValueError("ECTS müssen größer als 0 sein")
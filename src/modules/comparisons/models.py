from dataclasses import dataclass, field
from decimal import Decimal
from typing import Dict, Any, Optional

@dataclass
class RecordDTO:
    origin: str
    quadra: str
    lote: str
    area: Optional[Decimal] = None
    perimeter: Optional[Decimal] = None
    front: str = ""
    street: str = ""
    latitude: Optional[Decimal] = None
    longitude: Optional[Decimal] = None
    latitude_places: Optional[int] = None
    longitude_places: Optional[int] = None
    beneficiary: str = ""
    cpf: str = ""
    process_status: str = ""
    restriction: str = ""
    source_row: Any = ""
    extra: Dict[str, Any] = field(default_factory=dict)

    @property
    def key(self) -> tuple[str, str]:
        from .comparators.utils import normalize_quadra, normalize_lote
        return normalize_quadra(self.quadra), normalize_lote(self.lote)

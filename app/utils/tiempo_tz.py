from datetime import datetime
from zoneinfo import ZoneInfo
from ..core.config import settings


DEFAULT_TZ = ZoneInfo(settings.TZ_INFO)

def to_localtime(dt: datetime, tz: ZoneInfo = DEFAULT_TZ) -> datetime | None:
    """
    Convierte un datetime con zona horaria (tz-aware) a la zona especificada.
    Si el datetime no tiene zona, se asume UTC.
    """
    if dt is None:
        return None
    
    # Si no tiene tzinfo, asumimos que viene en UTC
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=ZoneInfo("UTC"))
    
    return dt.astimezone(tz)

from datetime import datetime, timedelta, timezone
from zoneinfo import ZoneInfo

FUSO = ZoneInfo("America/Sao_Paulo")

def para_utc(dt):
    return dt.astimezone(timezone.utc).replace(tzinfo=None)

def calcular_cortes():
    agora = datetime.now(FUSO)
    meia_noite = agora.replace(hour=0, minute=0, second=0, microsecond=0)

    inicio_dia = meia_noite
    inicio_semana = meia_noite - timedelta(days=agora.weekday())
    inicio_mes = meia_noite.replace(day=1)

    return para_utc(inicio_dia), para_utc(inicio_semana), para_utc(inicio_mes)
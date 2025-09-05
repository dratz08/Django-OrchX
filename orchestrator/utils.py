from croniter import croniter
from datetime import datetime


def validar_cron(expressao_cron: str) -> bool:
    try:
        # Tenta criar um iterador cron a partir da expressão
        croniter(expressao_cron, datetime.now())
        return True
    except:
        return False
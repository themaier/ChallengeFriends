from datetime import datetime, timedelta

def current_time() -> datetime:
    """Time: 'Europe/Paris' = utc+2"""
    return datetime.now()+timedelta(hours=2)
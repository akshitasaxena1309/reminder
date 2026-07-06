from datetime import datetime, timedelta, timezone
from croniter import croniter


def current_minute() -> datetime:
    """Now, truncated to the minute, in UTC — the unit cron granularity works at."""
    now = datetime.now(timezone.utc)
    return now.replace(second=0, microsecond=0)


def is_valid_cron(expression: str) -> bool:
    try:
        croniter(expression)
        return True
    except Exception:
        return False


def is_due(cron_expression: str, at_minute: datetime) -> bool:
    base = at_minute - timedelta(minutes=1)
    itr = croniter(cron_expression, base)
    next_run = itr.get_next(datetime)
    if next_run.tzinfo is None:
        next_run = next_run.replace(tzinfo=timezone.utc)
    next_run = next_run.replace(second=0, microsecond=0)
    return next_run == at_minute


def already_sent_this_minute(last_sent_at, at_minute: datetime) -> bool:
    if not last_sent_at:
        return False
    if last_sent_at.tzinfo is None:
        last_sent_at = last_sent_at.replace(tzinfo=timezone.utc)
    return last_sent_at.replace(second=0, microsecond=0) == at_minute
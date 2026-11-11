"""Episode 001: count qualifying days without presupposing the answer."""
from gidh_delhi_air.investigations.models import Investigation

DEFINITION = Investigation(
    id='clean-days',
    title='Can You Find 30 Clean Days in Delhi?',
    question='Can we find 30 qualifying days, and a continuous stretch, across the monitored Delhi locations?',
    status='planning',
)

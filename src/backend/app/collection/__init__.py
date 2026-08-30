"""Collection abstractions and offline/real sources."""

from app.collection.arbeitnow import ArbeitnowJobSource
from app.collection.base import JobCollector, RawJob
from app.collection.fake import FakeJobSource

__all__ = ["JobCollector", "RawJob", "FakeJobSource", "ArbeitnowJobSource"]

"""Collection abstractions and offline sources."""

from app.collection.base import JobCollector, RawJob
from app.collection.fake import FakeJobSource

__all__ = ["JobCollector", "RawJob", "FakeJobSource"]

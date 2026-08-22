"""Job queue for background batch processing."""
from __future__ import annotations
import uuid
from collections import deque
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum

class JobStatus(Enum):
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"

@dataclass
class Job:
    id: str
    file_path: str
    status: JobStatus = JobStatus.PENDING
    created_at: datetime = field(default_factory=datetime.now)
    started_at: datetime | None = None
    completed_at: datetime | None = None
    result: dict | None = None
    error: str | None = None

class JobQueue:
    def __init__(self, max_size: int = 1000):
        if max_size < 1:
            raise ValueError("max_size must be at least 1")
        self._max_size = max_size
        self._queue: deque[Job] = deque(maxlen=max_size)
        self._jobs: dict[str, Job] = {}

    def submit(self, file_path: str) -> Job:
        # deque(maxlen=...) would silently evict the oldest job while _jobs
        # still reported it pending, so it could never be dispatched.
        if len(self._queue) >= self._max_size:
            raise RuntimeError(f"queue is full ({self._max_size} jobs)")
        job = Job(id=uuid.uuid4().hex, file_path=file_path)
        self._queue.append(job)
        self._jobs[job.id] = job
        return job

    def next(self) -> Job | None:
        for job in self._queue:
            if job.status == JobStatus.PENDING:
                job.status = JobStatus.RUNNING
                job.started_at = datetime.now()
                return job
        return None

    def complete(self, job_id: str, result: dict) -> None:
        job = self._jobs.get(job_id)
        if job:
            job.status = JobStatus.COMPLETED
            job.completed_at = datetime.now()
            job.result = result
            self._drop_from_queue(job)

    def fail(self, job_id: str, error: str) -> None:
        job = self._jobs.get(job_id)
        if job:
            job.status = JobStatus.FAILED
            job.completed_at = datetime.now()
            job.error = error
            self._drop_from_queue(job)

    def _drop_from_queue(self, job: Job) -> None:
        try:
            self._queue.remove(job)
        except ValueError:
            pass

    @property
    def pending_count(self) -> int:
        return sum(1 for j in self._jobs.values() if j.status == JobStatus.PENDING)

    @property
    def total_jobs(self) -> int:
        return len(self._jobs)

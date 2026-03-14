"""Tests for job queue."""
from bird_mach.batch.queue import JobQueue, JobStatus

class TestJobQueue:
    def test_submit(self):
        q = JobQueue()
        job = q.submit("test.wav")
        assert job.status == JobStatus.PENDING

    def test_next(self):
        q = JobQueue()
        q.submit("test.wav")
        job = q.next()
        assert job.status == JobStatus.RUNNING

    def test_complete(self):
        q = JobQueue()
        job = q.submit("test.wav")
        q.next()
        q.complete(job.id, {"rms": 0.5})
        assert q._jobs[job.id].status == JobStatus.COMPLETED

    def test_pending_count(self):
        q = JobQueue()
        q.submit("a.wav")
        q.submit("b.wav")
        assert q.pending_count == 2
        q.next()
        assert q.pending_count == 1

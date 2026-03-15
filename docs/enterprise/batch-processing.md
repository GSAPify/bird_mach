# Batch Processing

## Pipeline
Configure multi-step processing pipelines:

```python
from bird_mach.batch.pipeline import BatchPipeline
pipe = BatchPipeline()
pipe.add_step("load", load_audio)
pipe.add_step("analyze", run_analysis)
results = pipe.process_batch(audio_files)
```

## Job Queue
Submit jobs for background processing with status tracking.

## File Scanner
Scan directories recursively for audio files with format grouping.

## Progress Tracking
Monitor batch progress with ETA estimation.

## Result Aggregation
Summarize batch results with averages and format counts.

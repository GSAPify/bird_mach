import io

import numpy as np
import pytest
import soundfile as sf
from fastapi import HTTPException

from bird_mach.api.routes import analyze_bytes


def test_undecodable_upload_is_a_400():
    with pytest.raises(HTTPException) as exc:
        analyze_bytes(b"not audio at all" * 10, 22050)
    assert exc.value.status_code == 400


def test_truncated_wav_upload_is_a_400():
    buf = io.BytesIO()
    sf.write(buf, np.zeros(2000), 8000, format="WAV")
    with pytest.raises(HTTPException) as exc:
        analyze_bytes(buf.getvalue()[:30], 22050)
    assert exc.value.status_code == 400

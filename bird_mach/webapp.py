"""FastAPI web application for Mach audio visualization."""

from __future__ import annotations

import html
import logging
import tempfile
import urllib.request
from pathlib import Path
from urllib.parse import urlparse

logger = logging.getLogger(__name__)

from fastapi import FastAPI, File, Form, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse

from bird_mach.constants import APP_NAME, APP_VERSION
from bird_mach.embedding import (
    DEFAULT_AUDIO_FEATURE_CONFIG,
    DEFAULT_UMAP_CONFIG,
    AudioFeatureConfig,
    ColorBy,
    UmapConfig,
    build_energy_figure,
    build_multiview_figure,
    build_mel_spectrogram_figure,
    build_singleview_figure,
    build_waveform_figure,
    compute_umap_3d,
    extract_log_mel_frames,
    load_audio_mono_from_path,
    stride_downsample,
)

INDEX_HTML = """\
<!doctype html>
<html lang="en">
  <head>
    <meta charset="utf-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1" />
    <meta name="description" content="Upload any audio and generate interactive 3D UMAP embeddings — music, speech, field recordings, anything" />
    <meta name="theme-color" content="#0b0f19" />
    <title>Mach — 3D Audio Map</title>
    <style>
      body {
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
        margin: 0;
        background: #0b0f19;
        color: #e6e8ef;
      }
      .wrap { max-width: 900px; margin: 0 auto; padding: 24px; }
      h1 { font-size: 22px; margin: 0 0 8px; }
      p { line-height: 1.5; color: #b7bdd1; margin: 0 0 16px; }
      .card {
        background: #121a2b;
        border: 1px solid rgba(255,255,255,0.08);
        border-radius: 12px;
        padding: 16px;
      }
      label { display: block; margin: 10px 0 6px; font-weight: 600; }
      input[type="file"], select, input[type="number"] {
        width: 100%;
        padding: 10px;
        border-radius: 10px;
        border: 1px solid rgba(255,255,255,0.14);
        background: #0e1526;
        color: #e6e8ef;
      }
      .row { display: grid; grid-template-columns: 1fr 1fr; gap: 12px; }
      .checks { display: flex; flex-wrap: wrap; gap: 14px; margin-top: 10px; }
      .checks label { display: inline-flex; align-items: center; gap: 8px; font-weight: 500; margin: 0; }
      button {
        margin-top: 14px;
        width: 100%;
        padding: 12px 14px;
        border-radius: 10px;
        border: 0;
        background: #3b82f6;
        color: #081024;
        font-weight: 700;
        cursor: pointer;
      }
      button:hover { filter: brightness(1.05); }
      .note { font-size: 13px; margin-top: 12px; }
      .note code { background: rgba(255,255,255,0.08); padding: 2px 6px; border-radius: 6px; }
    </style>
  </head>
  <body>
    <div class="wrap">
      <h1>Mach — 3D Audio Map</h1>
      <p>Upload any audio — music, speech, bird calls, field recordings — and generate a 3D embedding (UMAP) where each point represents a short-time frame. For real-time visuals while audio plays, try <a href="/live">Live mode</a>.</p>
      <div class="card">
        <form id="uploadForm" action="/visualize" method="post" enctype="multipart/form-data">
          <label for="audio">Audio file</label>
          <div id="dropZone" style="border: 2px dashed rgba(255,255,255,0.2); border-radius: 12px; padding: 28px; text-align: center; cursor: pointer; transition: border-color 0.2s, background 0.2s;">
            <div style="color: #b7bdd1; margin-bottom: 8px;">Drag & drop an audio file here, or click to browse</div>
            <input id="audio" name="audio" type="file" accept="audio/*" style="display:none" />
            <div id="fileName" style="color: #93c5fd; font-weight: 600; margin-top: 6px;"></div>
          </div>

          <div style="text-align: center; color: #b7bdd1; margin: 10px 0 6px; font-size: 13px;">— or paste a URL —</div>
          <input id="audioUrl" name="audio_url" type="url" placeholder="https://example.com/audio.wav" style="width:100%; padding:10px; border-radius:10px; border:1px solid rgba(255,255,255,0.14); background:#0e1526; color:#e6e8ef;" />

          <div class="row">
            <div>
              <label for="color_by">Color by</label>
              <select id="color_by" name="color_by">
                <option value="time" selected>Time</option>
                <option value="energy">Energy</option>
              </select>
            </div>
            <div>
              <label for="stride">Stride (downsample frames)</label>
              <input id="stride" name="stride" type="number" min="1" max="50" step="1" value="2" />
            </div>
          </div>

          <div class="row">
            <div>
              <label for="n_neighbors">UMAP n_neighbors</label>
              <input id="n_neighbors" name="n_neighbors" type="number" min="2" max="200" step="1" value="15" />
            </div>
            <div>
              <label for="min_dist">UMAP min_dist</label>
              <input id="min_dist" name="min_dist" type="number" min="0" max="1" step="0.01" value="0.10" />
            </div>
          </div>

          <div class="row">
            <div>
              <label for="colorscale">Colorscale</label>
              <select id="colorscale" name="colorscale">
                <option value="Turbo" selected>Turbo</option>
                <option value="Viridis">Viridis</option>
                <option value="Plasma">Plasma</option>
                <option value="Inferno">Inferno</option>
                <option value="Magma">Magma</option>
                <option value="Cividis">Cividis</option>
                <option value="Hot">Hot</option>
                <option value="Electric">Electric</option>
              </select>
            </div>
            <div style="display:flex; flex-direction:column; justify-content:end; gap:10px; padding-bottom:2px;">
              <label style="display:inline-flex; align-items:center; gap:8px; font-weight:500; margin:0;"><input type="checkbox" name="multi_view" value="1" checked /> Multi-view</label>
              <label style="display:inline-flex; align-items:center; gap:8px; font-weight:500; margin:0;"><input type="checkbox" name="connect" value="1" /> Connect points</label>
            </div>
          </div>

          <button type="submit">Generate 3D visualization</button>

          <p class="note">Tip: if the plot feels slow, increase <code>stride</code>.</p>
        </form>
      </div>
    </div>
    <script>
      const dropZone = document.getElementById("dropZone");
      const fileInput = document.getElementById("audio");
      const fileNameEl = document.getElementById("fileName");

      dropZone.addEventListener("click", () => fileInput.click());
      fileInput.addEventListener("change", () => {
        if (fileInput.files.length) fileNameEl.textContent = fileInput.files[0].name;
      });

      dropZone.addEventListener("dragover", (e) => {
        e.preventDefault();
        dropZone.style.borderColor = "#3b82f6";
        dropZone.style.background = "rgba(59,130,246,0.06)";
      });
      dropZone.addEventListener("dragleave", () => {
        dropZone.style.borderColor = "rgba(255,255,255,0.2)";
        dropZone.style.background = "transparent";
      });
      dropZone.addEventListener("drop", (e) => {
        e.preventDefault();
        dropZone.style.borderColor = "rgba(255,255,255,0.2)";
        dropZone.style.background = "transparent";
        if (e.dataTransfer.files.length) {
          fileInput.files = e.dataTransfer.files;
          fileNameEl.textContent = e.dataTransfer.files[0].name;
        }
      });
    </script>
  </body>
</html>
"""

LIVE_HTML = """\
<!doctype html>
<html lang="en">
  <head>
    <meta charset="utf-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1" />
    <meta name="description" content="Real-time audio visualization with waveform, spectrogram, and 3D point cloud" />
    <meta name="theme-color" content="#0b0f19" />
    <title>Mach — Live Audio</title>
    <style>
      body {
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
        margin: 0;
        background: #0b0f19;
        color: #e6e8ef;
      }
      a { color: #93c5fd; text-decoration: none; }
      a:hover { text-decoration: underline; }
      .wrap { max-width: 1100px; margin: 0 auto; padding: 18px; }
      h1 { font-size: 22px; margin: 0 0 8px; }
      p { line-height: 1.5; color: #b7bdd1; margin: 0 0 14px; }
      .card {
        background: #121a2b;
        border: 1px solid rgba(255,255,255,0.08);
        border-radius: 12px;
        padding: 14px;
        margin-bottom: 12px;
      }
      .row { display: grid; grid-template-columns: 1fr 1fr; gap: 12px; }
      label { display: block; margin: 10px 0 6px; font-weight: 600; }
      input[type="file"], select, input[type="number"] {
        width: 100%;
        padding: 10px;
        border-radius: 10px;
        border: 1px solid rgba(255,255,255,0.14);
        background: #0e1526;
        color: #e6e8ef;
      }
      button {
        padding: 10px 12px;
        border-radius: 10px;
        border: 0;
        background: #3b82f6;
        color: #081024;
        font-weight: 700;
        cursor: pointer;
      }
      button.secondary { background: rgba(255,255,255,0.12); color: #e6e8ef; }
      button:disabled { opacity: 0.55; cursor: not-allowed; }
      .btns { display: flex; flex-wrap: wrap; gap: 10px; margin-top: 12px; align-items: center; }
      .status { font-size: 13px; color: #b7bdd1; }
      canvas {
        width: 100%;
        border-radius: 12px;
        border: 1px solid rgba(255,255,255,0.08);
        background: #070a12;
        display: block;
      }
      .plots { display: grid; grid-template-columns: 1fr; gap: 12px; }
      .plot3d {
        border-radius: 12px;
        border: 1px solid rgba(255,255,255,0.08);
        background: #070a12;
        overflow: hidden;
      }
      .note { font-size: 13px; color: #b7bdd1; margin-top: 10px; }
      .note code { background: rgba(255,255,255,0.08); padding: 2px 6px; border-radius: 6px; }
    </style>
    <script src="https://cdn.plot.ly/plotly-2.27.0.min.js"></script>
  </head>
  <body>
    <div class="wrap">
      <div style="margin-bottom: 10px;"><a href="/">Back</a></div>
      <h1>Live audio visualization</h1>
      <p>Visualize audio in real time while it plays (waveform, spectrogram, and a 3D point cloud driven by the current spectrum).</p>

      <div class="card">
        <div class="row">
          <div>
            <label for="fileInput">Audio file (optional)</label>
            <input id="fileInput" type="file" accept="audio/*" />
            <audio id="player" controls style="width: 100%; margin-top: 10px;"></audio>
          </div>
          <div>
            <label for="motion">Motion</label>
            <select id="motion">
              <option value="loop" selected>Loop</option>
              <option value="cloud">Cloud</option>
            </select>
            <label for="loopSpeed">Loop speed (Hz)</label>
            <input id="loopSpeed" type="number" min="0.05" max="2" step="0.05" value="0.35" />
            <label for="colorBy">Color by</label>
            <select id="colorBy">
              <option value="time" selected>Time</option>
              <option value="energy">Energy</option>
            </select>
            <label for="maxPoints">Max points</label>
            <input id="maxPoints" type="number" min="200" max="10000" step="100" value="2500" />
            <label for="nBins">Bins used for cloud</label>
            <input id="nBins" type="number" min="32" max="512" step="16" value="128" />

            <div class="btns">
              <button id="startFileBtn">Start (file)</button>
              <button id="startMicBtn">Start (mic)</button>
              <button id="stopBtn" class="secondary" disabled>Stop</button>
              <button id="clearBtn" class="secondary">Clear points</button>
            </div>
            <div class="status" id="status">Idle.</div>
            <div class="note">Tip: If it gets slow, lower <code>max points</code> or <code>bins</code>.</div>
          </div>
        </div>
      </div>

      <div class="plots">
        <div class="card">
          <div style="font-weight: 700; margin-bottom: 8px;">Waveform</div>
          <canvas id="waveCanvas" width="1100" height="160"></canvas>
        </div>
        <div class="card">
          <div style="font-weight: 700; margin-bottom: 8px;">Spectrogram (scrolling)</div>
          <canvas id="specCanvas" width="1100" height="280"></canvas>
        </div>
        <div class="card">
          <div style="font-weight: 700; margin-bottom: 8px;">3D bubbles (loop / cloud)</div>
          <div id="cloud3d" class="plot3d" style="height: 520px;"></div>
        </div>
      </div>
    </div>

    <script>
      const statusEl = document.getElementById("status");
      const fileInput = document.getElementById("fileInput");
      const player = document.getElementById("player");
      const startFileBtn = document.getElementById("startFileBtn");
      const startMicBtn = document.getElementById("startMicBtn");
      const stopBtn = document.getElementById("stopBtn");
      const clearBtn = document.getElementById("clearBtn");
      const motionEl = document.getElementById("motion");
      const loopSpeedEl = document.getElementById("loopSpeed");
      const colorByEl = document.getElementById("colorBy");
      const maxPointsEl = document.getElementById("maxPoints");
      const nBinsEl = document.getElementById("nBins");

      const waveCanvas = document.getElementById("waveCanvas");
      const specCanvas = document.getElementById("specCanvas");
      const waveCtx = waveCanvas.getContext("2d");
      const specCtx = specCanvas.getContext("2d");

      let audioCtx = null;
      let analyser = null;
      let timeData = null;
      let freqData = null;
      let sourceNode = null;
      let mediaStream = null;
      let rafId = null;

      let projW = null; // [3][nBins]
      let cloudReady = false;
      let startedAt = 0;
      let smoothEnergy = 0;
      let smoothCentroid = 0;

      function mulberry32(seed) {
        return function() {
          let t = seed += 0x6D2B79F5;
          t = Math.imul(t ^ (t >>> 15), t | 1);
          t ^= t + Math.imul(t ^ (t >>> 7), t | 61);
          return ((t ^ (t >>> 14)) >>> 0) / 4294967296;
        }
      }

      function setStatus(text) {
        statusEl.textContent = text;
      }

      function ensureAudioContext() {
        if (audioCtx) return audioCtx;
        audioCtx = new (window.AudioContext || window.webkitAudioContext)();
        return audioCtx;
      }

      function teardownSource() {
        if (rafId) {
          cancelAnimationFrame(rafId);
          rafId = null;
        }
        if (sourceNode) {
          try { sourceNode.disconnect(); } catch (e) {}
          sourceNode = null;
        }
        if (mediaStream) {
          try {
            mediaStream.getTracks().forEach(t => t.stop());
          } catch (e) {}
          mediaStream = null;
        }
      }

      function initAnalyser() {
        const ctx = ensureAudioContext();
        analyser = ctx.createAnalyser();
        analyser.fftSize = 2048;
        analyser.smoothingTimeConstant = 0.85;
        timeData = new Uint8Array(analyser.fftSize);
        freqData = new Uint8Array(analyser.frequencyBinCount);
      }

      function initProjection() {
        const nBins = Math.max(32, Math.min(512, parseInt(nBinsEl.value || "128", 10)));
        const rng = mulberry32(1337);
        projW = [
          new Float32Array(nBins),
          new Float32Array(nBins),
          new Float32Array(nBins),
        ];
        for (let d = 0; d < 3; d++) {
          for (let i = 0; i < nBins; i++) {
            projW[d][i] = (rng() * 2.0 - 1.0);
          }
        }
        return nBins;
      }

      function initCloud() {
        const cloudDiv = document.getElementById("cloud3d");
        if (!window.Plotly) {
          cloudDiv.innerHTML = "<div style='padding: 12px; color: #b7bdd1;'>Plotly failed to load (3D cloud disabled). Waveform + spectrogram still work.</div>";
          cloudReady = false;
          return;
        }

        const layout = {
          margin: {l: 0, r: 0, t: 0, b: 0},
          scene: {
            xaxis: {title: "D1"},
            yaxis: {title: "D2"},
            zaxis: {title: "D3"},
          },
          paper_bgcolor: "#070a12",
          plot_bgcolor: "#070a12",
          font: {color: "#e6e8ef"},
        };
        Plotly.newPlot(
          cloudDiv,
          [
            {
              // trail
              type: "scatter3d",
              mode: "markers",
              x: [],
              y: [],
              z: [],
              marker: {
                size: [],
                opacity: 0.92,
                color: [],
                colorscale: "Turbo",
                showscale: true,
                colorbar: {title: "time (s)"},
              }
            },
            {
              // bubble glow
              type: "scatter3d",
              mode: "markers",
              x: [],
              y: [],
              z: [],
              marker: {
                size: [22],
                opacity: 0.18,
                color: [0],
                colorscale: "Turbo",
                showscale: false,
              }
            },
            {
              // bubble core
              type: "scatter3d",
              mode: "markers",
              x: [],
              y: [],
              z: [],
              marker: {
                size: [12],
                opacity: 0.92,
                color: [0],
                colorscale: "Turbo",
                showscale: false,
              }
            }
          ],
          layout,
          {displaylogo: false, responsive: true}
        );
        cloudReady = true;
      }

      function clearCloud() {
        const cloudDiv = document.getElementById("cloud3d");
        if (!cloudReady) return;
        Plotly.restyle(
          cloudDiv,
          {x: [[]], y: [[]], z: [[]], "marker.color": [[]], "marker.size": [[]]},
          [0]
        );
        Plotly.restyle(cloudDiv, {x: [[]], y: [[]], z: [[]]}, [1, 2]);
        startedAt = audioCtx ? audioCtx.currentTime : 0;
        smoothEnergy = 0;
        smoothCentroid = 0;
      }

      function drawWaveform() {
        const w = waveCanvas.width;
        const h = waveCanvas.height;
        waveCtx.clearRect(0, 0, w, h);

        waveCtx.lineWidth = 2;
        waveCtx.strokeStyle = "rgba(147,197,253,0.9)";
        waveCtx.beginPath();

        const slice = w / timeData.length;
        for (let i = 0; i < timeData.length; i++) {
          const v = timeData[i] / 255.0;
          const y = v * h;
          const x = i * slice;
          if (i === 0) waveCtx.moveTo(x, y);
          else waveCtx.lineTo(x, y);
        }
        waveCtx.stroke();
      }

      function colorForMagnitude(v) {
        // v in [0, 255]
        const t = v / 255.0;
        const hue = (1.0 - t) * 240.0; // blue->red
        return `hsl(${hue}, 90%, ${Math.max(18, 12 + 50 * t)}%)`;
      }

      function drawSpectrogram() {
        const w = specCanvas.width;
        const h = specCanvas.height;
        // Shift left by 1px
        const img = specCtx.getImageData(1, 0, w - 1, h);
        specCtx.putImageData(img, 0, 0);

        const bins = freqData.length;
        const colX = w - 1;
        for (let i = 0; i < bins; i++) {
          const v = freqData[i];
          const y = h - Math.floor((i / bins) * h) - 1;
          specCtx.fillStyle = colorForMagnitude(v);
          specCtx.fillRect(colX, y, 1, 1);
        }
      }

      function rmsEnergyFromTimeDomain() {
        let sum = 0;
        for (let i = 0; i < timeData.length; i++) {
          const v = (timeData[i] - 128) / 128.0;
          sum += v * v;
        }
        return Math.sqrt(sum / timeData.length);
      }

      function smoothValue(prev, next, attack, release) {
        const a = (next > prev) ? attack : release;
        return prev + (next - prev) * a;
      }

      function spectralCentroidNorm(nBins) {
        let sumMag = 0;
        let sumIdx = 0;
        const bins = Math.max(1, Math.min(nBins, freqData.length));
        for (let i = 0; i < bins; i++) {
          const mag = freqData[i] / 255.0;
          sumMag += mag;
          sumIdx += i * mag;
        }
        if (sumMag <= 1e-6) return 0;
        const centroid = sumIdx / sumMag;
        return centroid / bins;
      }

      function updateCloud() {
        if (!cloudReady) return;
        const cloudDiv = document.getElementById("cloud3d");
        const nBins = Math.max(32, Math.min(512, parseInt(nBinsEl.value || "128", 10)));
        const maxPoints = Math.max(200, Math.min(10000, parseInt(maxPointsEl.value || "2500", 10)));

        const t = audioCtx ? (audioCtx.currentTime - startedAt) : 0;
        const energyRaw = rmsEnergyFromTimeDomain();
        smoothEnergy = smoothValue(smoothEnergy, energyRaw, 0.35, 0.08);
        const centroidNormRaw = spectralCentroidNorm(nBins);
        smoothCentroid = smoothValue(smoothCentroid, centroidNormRaw, 0.25, 0.08);

        const energy01 = Math.max(0, Math.min(1, smoothEnergy * 4.0));
        const colorMode = (colorByEl.value === "energy") ? "energy" : "time";
        const c = (colorMode === "energy") ? energy01 : t;

        let x = 0, y = 0, z = 0;
        const motion = (motionEl && motionEl.value === "cloud") ? "cloud" : "loop";

        if (motion === "cloud") {
          if (!projW || projW[0].length !== nBins) {
            initProjection();
          }
          if (!projW) return;
          for (let i = 0; i < nBins; i++) {
            const mag = freqData[i] / 255.0;
            const v = Math.log1p(255.0 * mag) / Math.log(256.0);
            x += projW[0][i] * v;
            y += projW[1][i] * v;
            z += projW[2][i] * v;
          }
          x /= nBins;
          y /= nBins;
          z /= nBins;
        } else {
          const speed = Math.max(0.05, Math.min(2.0, parseFloat(loopSpeedEl.value || "0.35")));
          const theta = 2.0 * Math.PI * speed * t;
          const radius = 0.9 + energy01 * 2.2;
          const wobble = 0.15 + energy01 * 0.25;

          // 3D lissajous-ish loop with audio-driven radius + spectral centroid influence
          x = radius * Math.sin(theta) + wobble * Math.sin(theta * 3.0 + 0.7);
          y = radius * Math.sin(theta * 2.0 + 0.5) + wobble * Math.cos(theta * 2.0);
          z = radius * Math.sin(theta * 3.0 + 1.0) + (smoothCentroid - 0.5) * 1.6;
        }

        const trailSize = 2.5 + energy01 * 10.0;
        const bubbleCoreSize = 10.0 + energy01 * 34.0;
        const bubbleGlowSize = bubbleCoreSize * 1.85;

        const colorbarTitle = (colorMode === "energy") ? "energy" : "time (s)";
        Plotly.restyle(cloudDiv, {"marker.colorbar.title.text": colorbarTitle}, [0]);

        Plotly.extendTraces(
          cloudDiv,
          {x: [[x]], y: [[y]], z: [[z]], "marker.color": [[c]], "marker.size": [[trailSize]]},
          [0],
          maxPoints
        );

        Plotly.restyle(
          cloudDiv,
          {x: [[x]], y: [[y]], z: [[z]], "marker.color": [[c]], "marker.size": [[bubbleGlowSize]]},
          [1]
        );
        Plotly.restyle(
          cloudDiv,
          {x: [[x]], y: [[y]], z: [[z]], "marker.color": [[c]], "marker.size": [[bubbleCoreSize]]},
          [2]
        );
      }

      function loop() {
        analyser.getByteTimeDomainData(timeData);
        analyser.getByteFrequencyData(freqData);

        drawWaveform();
        drawSpectrogram();
        updateCloud();

        rafId = requestAnimationFrame(loop);
      }

      async function startFromFile() {
        teardownSource();
        initAnalyser();
        initProjection();
        initCloud();

        const ctx = ensureAudioContext();
        await ctx.resume();

        sourceNode = ctx.createMediaElementSource(player);
        sourceNode.connect(analyser);
        analyser.connect(ctx.destination);

        startedAt = ctx.currentTime;
        stopBtn.disabled = false;
        setStatus("Running (file). Press play on the audio control if needed.");
        loop();
      }

      async function startFromMic() {
        teardownSource();
        initAnalyser();
        initProjection();
        initCloud();

        const ctx = ensureAudioContext();
        await ctx.resume();

        mediaStream = await navigator.mediaDevices.getUserMedia({audio: true});
        sourceNode = ctx.createMediaStreamSource(mediaStream);
        sourceNode.connect(analyser);

        startedAt = ctx.currentTime;
        stopBtn.disabled = false;
        setStatus("Running (mic).");
        loop();
      }

      function stop() {
        teardownSource();
        stopBtn.disabled = true;
        setStatus("Stopped.");
      }

      fileInput.addEventListener("change", () => {
        const file = fileInput.files && fileInput.files[0];
        if (!file) return;
        const url = URL.createObjectURL(file);
        player.src = url;
        setStatus(`Loaded file: ${file.name}`);
      });

      startFileBtn.addEventListener("click", async () => {
        try {
          if (!player.src) {
            setStatus("Pick an audio file first (or use mic).");
            return;
          }
          await startFromFile();
        } catch (e) {
          setStatus(`Failed to start (file): ${e}`);
        }
      });

      startMicBtn.addEventListener("click", async () => {
        try {
          await startFromMic();
        } catch (e) {
          setStatus(`Failed to start (mic): ${e}`);
        }
      });

      stopBtn.addEventListener("click", () => stop());
      clearBtn.addEventListener("click", () => clearCloud());

      // Initialize visuals immediately
      (function init() {
        specCtx.fillStyle = "#070a12";
        specCtx.fillRect(0, 0, specCanvas.width, specCanvas.height);
        setStatus("Idle. Load a file or start mic.");
      })();
    </script>
  </body>
</html>
"""


def normalize_color_by(value: str) -> ColorBy:
    if value == "energy":
        return "energy"
    return "time"


def build_result_page(*, title: str, summary: str, sections: list[tuple[str, str]]) -> str:
    safe_title = html.escape(title)
    safe_summary = html.escape(summary)
    sections_html = "\n".join(
        f'<div style="margin-top: 14px;">'
        f'<div style="font-weight: 800; margin: 6px 0 8px;">{html.escape(section_title)}</div>'
        f'<div class="plot">{section_html}</div>'
        f"</div>"
        for section_title, section_html in sections
    )
    return f"""\
<!doctype html>
<html lang="en">
  <head>
    <meta charset="utf-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1" />
    <title>{safe_title}</title>
    <style>
      body {{
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
        margin: 0;
        background: #0b0f19;
        color: #e6e8ef;
      }}
      .wrap {{ max-width: 1100px; margin: 0 auto; padding: 14px 18px; }}
      a {{ color: #93c5fd; text-decoration: none; }}
      a:hover {{ text-decoration: underline; }}
      .top {{
        display: flex;
        gap: 10px;
        align-items: baseline;
        justify-content: space-between;
        flex-wrap: wrap;
        margin-bottom: 8px;
      }}
      .meta {{ color: #b7bdd1; font-size: 13px; }}
      .plot {{
        background: #121a2b;
        border: 1px solid rgba(255,255,255,0.08);
        border-radius: 12px;
        padding: 8px;
      }}
    </style>
  </head>
  <body>
    <div class="wrap">
      <div class="top">
        <div>
          <div><a href="/">Back</a></div>
          <div style="margin-top: 6px;"><a href="/live">Live mode</a></div>
          <h2 style="margin: 6px 0 2px;">{safe_title}</h2>
          <div class="meta">{safe_summary}</div>
        </div>
      </div>
      {sections_html}
    </div>
  </body>
</html>
"""


app = FastAPI(title=APP_NAME, version=APP_VERSION)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)


@app.get("/health")
def health() -> dict:
    """Lightweight health-check for uptime monitors and load balancers."""
    return {"status": "ok", "version": app.version}


@app.get("/", response_class=HTMLResponse)
def index() -> HTMLResponse:
    return HTMLResponse(INDEX_HTML)


@app.get("/live", response_class=HTMLResponse)
def live() -> HTMLResponse:
    return HTMLResponse(LIVE_HTML)


def _fetch_audio_from_url(url: str) -> tuple[bytes, str]:
    """Download audio from a URL, return (bytes, filename)."""
    parsed = urlparse(url)
    if parsed.scheme not in ("http", "https"):
        raise ValueError("Only http/https URLs are supported")
    filename = Path(parsed.path).name or "remote_audio.wav"
    req = urllib.request.Request(url, headers={"User-Agent": "Mach/0.2"})
    with urllib.request.urlopen(req, timeout=30) as resp:
        data = resp.read(50 * 1024 * 1024)  # 50 MB limit
    return data, filename


@app.post("/visualize", response_class=HTMLResponse)
async def visualize(
    audio: UploadFile = File(None),
    audio_url: str = Form(""),
    color_by: str = Form("time"),
    colorscale: str = Form("Turbo"),
    stride: int = Form(2),
    n_neighbors: int = Form(DEFAULT_UMAP_CONFIG.n_neighbors),
    min_dist: float = Form(DEFAULT_UMAP_CONFIG.min_dist),
    multi_view: bool = Form(False),
    connect: bool = Form(False),
) -> HTMLResponse:
    raw: bytes = b""
    filename = "audio"

    if audio and audio.filename:
        raw = await audio.read()
        filename = audio.filename
    elif audio_url.strip():
        try:
            raw, filename = _fetch_audio_from_url(audio_url.strip())
        except Exception as e:
            logger.warning("URL fetch failed: %s", e)
            return HTMLResponse(f"Failed to fetch audio from URL: {html.escape(str(e))}", status_code=400)

    if not raw:
        logger.warning("No audio provided (neither file nor URL)")
        return HTMLResponse("No audio received. Upload a file or provide a URL.", status_code=400)

    logger.info("Processing: %s (%d bytes)", filename, len(raw))

    stride = max(1, min(stride, 50))
    n_neighbors = max(2, min(n_neighbors, 200))
    min_dist = max(0.0, min(min_dist, 1.0))

    suffix = Path(filename).suffix
    if not suffix:
        suffix = ".wav"

    tmp_path: Path | None = None
    try:
        with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as f:
            f.write(raw)
            tmp_path = Path(f.name)

        audio_cfg = AudioFeatureConfig(
            sr=DEFAULT_AUDIO_FEATURE_CONFIG.sr,
            n_fft=DEFAULT_AUDIO_FEATURE_CONFIG.n_fft,
            hop_length=DEFAULT_AUDIO_FEATURE_CONFIG.hop_length,
            n_mels=DEFAULT_AUDIO_FEATURE_CONFIG.n_mels,
            fmin=DEFAULT_AUDIO_FEATURE_CONFIG.fmin,
            fmax=DEFAULT_AUDIO_FEATURE_CONFIG.fmax,
        )
        umap_cfg = UmapConfig(
            n_neighbors=n_neighbors,
            min_dist=min_dist,
            metric=DEFAULT_UMAP_CONFIG.metric,
            random_state=DEFAULT_UMAP_CONFIG.random_state,
        )

        y, sr = load_audio_mono_from_path(tmp_path, sr=audio_cfg.sr)
        X, times_s, energy = extract_log_mel_frames(y, sr, audio_cfg)
        X, times_s, energy = stride_downsample(X, times_s, energy, stride=stride)
        emb = compute_umap_3d(X, umap_cfg)

        chosen_color_by = normalize_color_by(color_by)
        title = f"{filename} — 3D embedding"
        duration_s = float(y.shape[0]) / float(sr)
        summary = (
            f"duration={duration_s:.2f}s frames={X.shape[0]} stride={stride} "
            f"color_by={chosen_color_by} connect={connect} multi_view={multi_view}"
        )

        if multi_view:
            fig = build_multiview_figure(
                emb,
                times_s=times_s,
                energy=energy,
                color_by=chosen_color_by,
                connect=connect,
                title=title,
                colorscale=colorscale,
            )
        else:
            fig = build_singleview_figure(
                emb,
                times_s=times_s,
                energy=energy,
                color_by=chosen_color_by,
                connect=connect,
                title=title,
                colorscale=colorscale,
            )

        embedding_html = fig.to_html(include_plotlyjs=True, full_html=False)

        waveform_fig = build_waveform_figure(y, sr, title="Waveform")
        waveform_html = waveform_fig.to_html(include_plotlyjs=False, full_html=False)

        mel_fig = build_mel_spectrogram_figure(X, times_s, sr=sr, cfg=audio_cfg, title="Log-mel spectrogram (dB)")
        mel_html = mel_fig.to_html(include_plotlyjs=False, full_html=False)

        energy_fig = build_energy_figure(times_s, energy, title="Energy over time")
        energy_html = energy_fig.to_html(include_plotlyjs=False, full_html=False)

        sections = [
            ("3D embedding (UMAP)", embedding_html),
            ("Waveform", waveform_html),
            ("Log-mel spectrogram", mel_html),
            ("Energy", energy_html),
        ]

        return HTMLResponse(build_result_page(title=title, summary=summary, sections=sections))
    except Exception as e:
        logger.exception("Visualization failed for %s", filename)
        msg = html.escape(str(e))
        return HTMLResponse(f"<pre>Failed to visualize audio:\n{msg}</pre>", status_code=500)
    finally:
        if tmp_path is not None:
            try:
                tmp_path.unlink(missing_ok=True)
            except Exception:
                pass



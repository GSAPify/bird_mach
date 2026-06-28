// Real-time audio visualizer for /live.
(function () {
  const statusEl = document.getElementById("status");
  const statusText = document.getElementById("statusText");
  const fileDrop = document.getElementById("fileDrop");
  const fileInput = document.getElementById("fileInput");
  const fileLabel = document.getElementById("fileLabel");
  const player = document.getElementById("player");
  const startFileBtn = document.getElementById("startFileBtn");
  const checkMicBtn = document.getElementById("checkMicBtn");
  const startMicBtn = document.getElementById("startMicBtn");
  const startScreenBtn = document.getElementById("startScreenBtn");
  const stopBtn = document.getElementById("stopBtn");
  const clearBtn = document.getElementById("clearBtn");
  const fullscreenBtn = document.getElementById("fullscreenBtn");
  const micDeviceEl = document.getElementById("micDevice");
  const micPermissionEl = document.getElementById("micPermission");
  const motionEl = document.getElementById("motion");
  const loopSpeedEl = document.getElementById("loopSpeed");
  const colorByEl = document.getElementById("colorBy");
  const maxPointsEl = document.getElementById("maxPoints");
  const nBinsEl = document.getElementById("nBins");
  const bandsCanvas = document.getElementById("bandsCanvas");
  const waveCanvas = document.getElementById("waveCanvas");
  const specCanvas = document.getElementById("specCanvas");
  const levelFill = document.getElementById("levelFill");
  const statRms = document.getElementById("statRms");
  const statPeak = document.getElementById("statPeak");
  const statCentroid = document.getElementById("statCentroid");
  const statTime = document.getElementById("statTime");

  if (!statusEl || !fileInput || !player || !bandsCanvas || !waveCanvas || !specCanvas) {
    return;
  }

  const PREFS_KEY = "mach.live.prefs.v1";

  function loadPrefs() {
    try {
      const raw = window.localStorage.getItem(PREFS_KEY);
      return raw ? JSON.parse(raw) : {};
    } catch (e) {
      return {};
    }
  }

  function savePrefs(patch) {
    try {
      const next = Object.assign({}, loadPrefs(), patch);
      window.localStorage.setItem(PREFS_KEY, JSON.stringify(next));
    } catch (e) {
      // localStorage may be disabled (private mode, quota); silently ignore.
    }
  }

  const bandsCtx = bandsCanvas.getContext("2d");
  const waveCtx = waveCanvas.getContext("2d");
  const specCtx = specCanvas.getContext("2d");

  let audioCtx = null;
  let analyser = null;
  let timeData = null;
  let freqData = null;
  let sourceNode = null;
  let mediaElementSource = null;
  let mediaStream = null;
  let objectUrl = null;
  let rafId = null;
  let activeSource = null;
  let isStartingFile = false;
  let isStopping = false;
  let projW = null;
  let cloudReady = false;
  let startedAt = 0;
  let smoothEnergy = 0;
  let smoothCentroid = 0;
  let frameCount = 0;

  function setStatus(text, state) {
    if (!statusText || !statusEl) return;
    statusText.textContent = text;
    statusEl.classList.remove("is-live", "is-ok");
    if (state) statusEl.classList.add(state);
  }

  function setMicPermission(text, state) {
    if (!micPermissionEl) return;
    micPermissionEl.textContent = text;
    micPermissionEl.classList.remove("is-ok", "is-warn", "is-danger");
    if (state) micPermissionEl.classList.add(state);
  }

  function isLocalCaptureHost() {
    const host = window.location.hostname;
    return host === "localhost" || host === "127.0.0.1" || host === "::1";
  }

  function mediaCaptureContextReady() {
    return window.isSecureContext || isLocalCaptureHost();
  }

  function micAudioConstraints() {
    const audio = {
      echoCancellation: false,
      noiseSuppression: false,
      autoGainControl: false,
    };
    if (micDeviceEl && micDeviceEl.value) {
      audio.deviceId = { exact: micDeviceEl.value };
    }
    return { audio: audio };
  }

  function mediaErrorMessage(error) {
    if (!error) return "Unknown media error.";
    if (error.name === "NotAllowedError" || error.name === "SecurityError") {
      return "Microphone access was blocked. Allow this site in browser settings and try again.";
    }
    if (error.name === "NotFoundError" || error.name === "DevicesNotFoundError") {
      return "No microphone was found on this device.";
    }
    if (error.name === "NotReadableError" || error.name === "TrackStartError") {
      return "The microphone is already in use by another app or browser tab.";
    }
    if (error.name === "OverconstrainedError" || error.name === "ConstraintNotSatisfiedError") {
      return "The selected microphone is unavailable. Choose another input and try again.";
    }
    return error.message || "Microphone capture failed.";
  }

  function stopStream(stream) {
    if (!stream) return;
    stream.getTracks().forEach(function (track) { track.stop(); });
  }

  function setMicButtonsDisabled(disabled) {
    if (startMicBtn) startMicBtn.disabled = disabled;
    if (checkMicBtn) checkMicBtn.disabled = disabled;
  }

  async function refreshMicDevices(preferredDeviceId) {
    if (!micDeviceEl) return;
    if (!navigator.mediaDevices || !navigator.mediaDevices.enumerateDevices) {
      micDeviceEl.innerHTML = "<option value=''>Device list unavailable</option>";
      micDeviceEl.disabled = true;
      return;
    }

    const devices = await navigator.mediaDevices.enumerateDevices();
    const audioInputs = devices.filter(function (device) {
      return device.kind === "audioinput";
    });
    const selected = preferredDeviceId || micDeviceEl.value;
    micDeviceEl.innerHTML = "";

    if (!audioInputs.length) {
      const emptyOption = document.createElement("option");
      emptyOption.value = "";
      emptyOption.textContent = "No microphones found";
      micDeviceEl.appendChild(emptyOption);
      micDeviceEl.disabled = true;
      return;
    }

    const defaultOption = document.createElement("option");
    defaultOption.value = "";
    defaultOption.textContent = "Default microphone";
    micDeviceEl.appendChild(defaultOption);

    audioInputs.forEach(function (device, index) {
      if (!device.deviceId || device.deviceId === "default") return;
      const option = document.createElement("option");
      option.value = device.deviceId;
      option.textContent = device.label || "Microphone " + (index + 1);
      micDeviceEl.appendChild(option);
    });

    micDeviceEl.disabled = false;
    if (selected) {
      const hasSelectedDevice = Array.from(micDeviceEl.options).some(function (option) {
        return option.value === selected;
      });
      if (hasSelectedDevice) micDeviceEl.value = selected;
    }
  }

  async function refreshMicPermission() {
    if (!navigator.mediaDevices || !navigator.mediaDevices.getUserMedia) {
      setMicPermission("Unavailable", "is-danger");
      setMicButtonsDisabled(true);
      return;
    }
    if (!mediaCaptureContextReady()) {
      setMicPermission("HTTPS needed", "is-danger");
      setMicButtonsDisabled(true);
      return;
    }
    setMicButtonsDisabled(false);

    if (!navigator.permissions || !navigator.permissions.query) {
      setMicPermission("Click Check mic", "is-warn");
      return;
    }

    try {
      const status = await navigator.permissions.query({ name: "microphone" });
      function renderPermissionState() {
        if (status.state === "granted") setMicPermission("Allowed", "is-ok");
        else if (status.state === "denied") setMicPermission("Blocked", "is-danger");
        else setMicPermission("Ask on click", "is-warn");
      }
      renderPermissionState();
      status.onchange = renderPermissionState;
    } catch (error) {
      setMicPermission("Click Check mic", "is-warn");
    }
  }

  async function checkMicrophonePermission() {
    if (!navigator.mediaDevices || !navigator.mediaDevices.getUserMedia) {
      setMicPermission("Unavailable", "is-danger");
      setStatus("Microphone capture is unavailable in this browser or context.");
      return;
    }
    if (!mediaCaptureContextReady()) {
      setMicPermission("HTTPS needed", "is-danger");
      setStatus("Mic and tab audio need HTTPS, localhost, or 127.0.0.1.");
      return;
    }

    setMicButtonsDisabled(true);
    setMicPermission("Requesting...", "is-warn");
    try {
      const stream = await navigator.mediaDevices.getUserMedia(micAudioConstraints());
      stopStream(stream);
      await refreshMicDevices();
      setMicPermission("Allowed", "is-ok");
      setStatus("Microphone permission is ready.", "is-ok");
    } catch (error) {
      const message = mediaErrorMessage(error);
      setMicPermission("Blocked", "is-danger");
      setStatus(message);
    } finally {
      setMicButtonsDisabled(false);
    }
  }

  function clampNumber(value, fallback, min, max) {
    const parsed = Number.parseFloat(value);
    if (Number.isNaN(parsed)) return fallback;
    return Math.max(min, Math.min(max, parsed));
  }

  function clampInt(value, fallback, min, max) {
    const parsed = Number.parseInt(value, 10);
    if (Number.isNaN(parsed)) return fallback;
    return Math.max(min, Math.min(max, parsed));
  }

  function ensureAudioContext() {
    if (!audioCtx) {
      const AudioContextCtor = window.AudioContext || window.webkitAudioContext;
      audioCtx = new AudioContextCtor();
    }
    return audioCtx;
  }

  async function resumeAudioContext() {
    const ctx = ensureAudioContext();
    if (ctx.state !== "running") {
      await ctx.resume();
    }
    return ctx;
  }

  function initAnalyser() {
    const ctx = ensureAudioContext();
    analyser = ctx.createAnalyser();
    analyser.fftSize = 2048;
    analyser.smoothingTimeConstant = 0.82;
    timeData = new Uint8Array(analyser.fftSize);
    freqData = new Uint8Array(analyser.frequencyBinCount);
  }

  function stopAnimation() {
    if (rafId) {
      cancelAnimationFrame(rafId);
      rafId = null;
    }
  }

  function disconnectCurrentSource() {
    stopAnimation();
    if (sourceNode) {
      try {
        sourceNode.disconnect();
      } catch (e) {
        // Some browsers throw if a node is already disconnected.
      }
      sourceNode = null;
    }
    if (analyser) {
      try {
        analyser.disconnect();
      } catch (e) {
        // Analyzer may already be detached when switching sources quickly.
      }
    }
    stopStream(mediaStream);
    mediaStream = null;
    activeSource = null;
  }

  function resetMeters() {
    if (levelFill) levelFill.style.width = "0%";
    if (statRms) statRms.textContent = "--";
    if (statPeak) statPeak.textContent = "--";
    if (statCentroid) statCentroid.textContent = "--";
    if (statTime) statTime.textContent = "--";
  }

  function mulberry32(seed) {
    return function () {
      let t = seed += 0x6D2B79F5;
      t = Math.imul(t ^ (t >>> 15), t | 1);
      t ^= t + Math.imul(t ^ (t >>> 7), t | 61);
      return ((t ^ (t >>> 14)) >>> 0) / 4294967296;
    };
  }

  function initProjection() {
    const nBins = clampInt(nBinsEl.value, 128, 32, 512);
    const rng = mulberry32(1337);
    projW = [new Float32Array(nBins), new Float32Array(nBins), new Float32Array(nBins)];
    for (let d = 0; d < 3; d += 1) {
      for (let i = 0; i < nBins; i += 1) {
        projW[d][i] = (rng() * 2) - 1;
      }
    }
  }

  function initCanvases() {
    specCtx.fillStyle = "#030611";
    specCtx.fillRect(0, 0, specCanvas.width, specCanvas.height);
    waveCtx.clearRect(0, 0, waveCanvas.width, waveCanvas.height);
    bandsCtx.clearRect(0, 0, bandsCanvas.width, bandsCanvas.height);
  }

  function initCloud() {
    const cloudDiv = document.getElementById("cloud3d");
    if (!cloudDiv) return;
    if (!window.Plotly) {
      cloudDiv.innerHTML = "<div class='plot-fallback'>3D cloud could not load. Waveform and spectrogram are still available.</div>";
      cloudReady = false;
      return;
    }

    const layout = {
      margin: { l: 0, r: 0, t: 0, b: 0 },
      paper_bgcolor: "#030611",
      plot_bgcolor: "#030611",
      font: { color: "#eef3ff", family: "IBM Plex Sans, sans-serif" },
      showlegend: false,
      scene: {
        bgcolor: "#030611",
        xaxis: axisStyle("D1"),
        yaxis: axisStyle("D2"),
        zaxis: axisStyle("D3"),
        camera: { eye: { x: 1.45, y: 1.35, z: 1.05 } },
      },
    };

    const config = {
      displaylogo: false,
      responsive: true,
      modeBarButtonsToRemove: ["sendDataToCloud", "lasso2d", "select2d"],
    };

    Plotly.react(
      cloudDiv,
      [
        {
          type: "scatter3d",
          mode: "markers",
          x: [],
          y: [],
          z: [],
          marker: {
            size: [],
            opacity: 0.9,
            color: [],
            colorscale: "Turbo",
            showscale: true,
            colorbar: {
              title: { text: "time (s)" },
              thickness: 12,
              len: 0.72,
              outlinewidth: 0,
            },
          },
          hovertemplate: "x=%{x:.2f}<br>y=%{y:.2f}<br>z=%{z:.2f}<extra></extra>",
        },
        bubbleTrace("rgba(47, 160, 255, 0.24)", 30),
        bubbleTrace("#f8fbff", 14),
      ],
      layout,
      config
    );
    cloudReady = true;
  }

  function axisStyle(title) {
    return {
      title: { text: title },
      color: "#aeb9dc",
      gridcolor: "rgba(174, 185, 220, 0.14)",
      zerolinecolor: "rgba(174, 185, 220, 0.24)",
      showbackground: true,
      backgroundcolor: "rgba(255, 255, 255, 0.015)",
    };
  }

  function bubbleTrace(color, size) {
    return {
      type: "scatter3d",
      mode: "markers",
      x: [0],
      y: [0],
      z: [0],
      marker: {
        size: [size],
        color: [color],
        opacity: 0.9,
        line: { width: 0 },
      },
      hoverinfo: "skip",
    };
  }

  function clearCloud() {
    const cloudDiv = document.getElementById("cloud3d");
    if (!cloudReady || !window.Plotly || !cloudDiv) return;
    Plotly.purge(cloudDiv);
    initCloud();
    initCanvases();
    resetMeters();
    setStatus("Cleared the live view.", "is-ok");
  }

  function colorForMagnitude(value) {
    const t = value / 255;
    const hue = 205 - (205 * t);
    const lightness = 14 + (48 * t);
    return "hsl(" + hue + ", 92%, " + lightness + "%)";
  }

  function drawBands() {
    const w = bandsCanvas.width;
    const h = bandsCanvas.height;
    bandsCtx.clearRect(0, 0, w, h);
    const bands = [
      { name: "Sub", lo: 0, hi: 5 },
      { name: "Bass", lo: 5, hi: 14 },
      { name: "Low", lo: 14, hi: 32 },
      { name: "Mid", lo: 32, hi: 90 },
      { name: "High", lo: 90, hi: 180 },
      { name: "Air", lo: 180, hi: 340 },
      { name: "Edge", lo: 340, hi: 512 },
    ];
    const gap = 10;
    const bw = (w - (gap * (bands.length - 1))) / bands.length;

    bands.forEach(function (band, index) {
      const lo = Math.min(freqData.length - 1, band.lo);
      const hi = Math.min(freqData.length, band.hi);
      let sum = 0;
      for (let i = lo; i < hi; i += 1) sum += freqData[i];
      const avg = sum / Math.max(1, hi - lo);
      const level = avg / 255;
      const x = index * (bw + gap);
      const barHeight = Math.max(4, level * (h - 24));
      const y = h - barHeight;

      const gradient = bandsCtx.createLinearGradient(0, y, 0, h);
      gradient.addColorStop(0, "#f7e37c");
      gradient.addColorStop(0.45, "#26d7a2");
      gradient.addColorStop(1, "#1c74d8");
      bandsCtx.fillStyle = "rgba(255, 255, 255, 0.045)";
      bandsCtx.fillRect(x, 0, bw, h);
      bandsCtx.fillStyle = gradient;
      bandsCtx.fillRect(x, y, bw, barHeight);
      bandsCtx.fillStyle = "rgba(238, 243, 255, 0.68)";
      bandsCtx.font = "12px IBM Plex Sans, sans-serif";
      bandsCtx.fillText(band.name, x + 8, h - 8);
    });
  }

  function drawWaveform() {
    const w = waveCanvas.width;
    const h = waveCanvas.height;
    waveCtx.clearRect(0, 0, w, h);

    const gradient = waveCtx.createLinearGradient(0, 0, w, 0);
    gradient.addColorStop(0, "#2dd4bf");
    gradient.addColorStop(0.5, "#d6e33f");
    gradient.addColorStop(1, "#f97316");
    waveCtx.lineWidth = 2;
    waveCtx.strokeStyle = gradient;
    waveCtx.beginPath();

    const slice = w / timeData.length;
    for (let i = 0; i < timeData.length; i += 1) {
      const v = timeData[i] / 255;
      const y = v * h;
      const x = i * slice;
      if (i === 0) waveCtx.moveTo(x, y);
      else waveCtx.lineTo(x, y);
    }
    waveCtx.stroke();

    waveCtx.strokeStyle = "rgba(238, 243, 255, 0.16)";
    waveCtx.lineWidth = 1;
    waveCtx.beginPath();
    waveCtx.moveTo(0, h / 2);
    waveCtx.lineTo(w, h / 2);
    waveCtx.stroke();
  }

  function drawSpectrogram() {
    const w = specCanvas.width;
    const h = specCanvas.height;
    if (w <= 1 || h <= 1) return;

    const image = specCtx.getImageData(1, 0, w - 1, h);
    specCtx.putImageData(image, 0, 0);
    const colX = w - 1;
    for (let i = 0; i < freqData.length; i += 1) {
      const value = freqData[i];
      const y = h - Math.floor((i / freqData.length) * h) - 1;
      specCtx.fillStyle = colorForMagnitude(value);
      specCtx.fillRect(colX, y, 1, 1);
    }
  }

  function rmsEnergyFromTimeDomain() {
    let sum = 0;
    for (let i = 0; i < timeData.length; i += 1) {
      const v = (timeData[i] - 128) / 128;
      sum += v * v;
    }
    return Math.sqrt(sum / timeData.length);
  }

  function peakFromTimeDomain() {
    let peak = 0;
    for (let i = 0; i < timeData.length; i += 1) {
      const v = Math.abs((timeData[i] - 128) / 128);
      if (v > peak) peak = v;
    }
    return peak;
  }

  function smoothValue(prev, next, attack, release) {
    const amount = next > prev ? attack : release;
    return prev + ((next - prev) * amount);
  }

  function spectralCentroidNorm(nBins) {
    let sumMag = 0;
    let sumIdx = 0;
    const bins = Math.max(1, Math.min(nBins, freqData.length));
    for (let i = 0; i < bins; i += 1) {
      const mag = freqData[i] / 255;
      sumMag += mag;
      sumIdx += i * mag;
    }
    if (sumMag <= 1e-6) return 0;
    return (sumIdx / sumMag) / bins;
  }

  function updateCloud() {
    const cloudDiv = document.getElementById("cloud3d");
    if (!cloudReady || !window.Plotly || !cloudDiv) return;

    const nBins = clampInt(nBinsEl.value, 128, 32, 512);
    const maxPoints = clampInt(maxPointsEl.value, 2500, 200, 10000);
    const t = audioCtx ? audioCtx.currentTime - startedAt : 0;
    const energyRaw = rmsEnergyFromTimeDomain();
    smoothEnergy = smoothValue(smoothEnergy, energyRaw, 0.35, 0.08);
    smoothCentroid = smoothValue(smoothCentroid, spectralCentroidNorm(nBins), 0.25, 0.08);

    const energy01 = Math.max(0, Math.min(1, smoothEnergy * 4));
    const colorMode = colorByEl.value === "energy" ? "energy" : "time";
    const c = colorMode === "energy" ? energy01 : Math.max(0, t);
    let x = 0;
    let y = 0;
    let z = 0;

    if (motionEl.value === "cloud") {
      if (!projW || projW[0].length !== nBins) initProjection();
      for (let i = 0; i < nBins; i += 1) {
        const mag = freqData[i] / 255;
        const v = Math.log1p(255 * mag) / Math.log(256);
        x += projW[0][i] * v;
        y += projW[1][i] * v;
        z += projW[2][i] * v;
      }
      x /= nBins;
      y /= nBins;
      z /= nBins;
    } else {
      const speed = clampNumber(loopSpeedEl.value, 0.35, 0.05, 2);
      const theta = 2 * Math.PI * speed * t;
      const radius = 0.9 + (energy01 * 2.2);
      const wobble = 0.15 + (energy01 * 0.25);
      x = (radius * Math.sin(theta)) + (wobble * Math.sin((theta * 3) + 0.7));
      y = (radius * Math.sin((theta * 2) + 0.5)) + (wobble * Math.cos(theta * 2));
      z = (radius * Math.sin((theta * 3) + 1)) + ((smoothCentroid - 0.5) * 1.6);
    }

    const trailSize = 2.5 + (energy01 * 9.5);
    const coreSize = 10 + (energy01 * 32);
    const glowSize = coreSize * 1.85;
    const colorbarTitle = colorMode === "energy" ? "energy" : "time (s)";

    Plotly.restyle(cloudDiv, { "marker.colorbar.title.text": colorbarTitle }, [0]);
    Plotly.extendTraces(
      cloudDiv,
      { x: [[x]], y: [[y]], z: [[z]], "marker.color": [[c]], "marker.size": [[trailSize]] },
      [0],
      maxPoints
    );
    Plotly.restyle(
      cloudDiv,
      { x: [[x]], y: [[y]], z: [[z]], "marker.size": [[glowSize]] },
      [1]
    );
    Plotly.restyle(
      cloudDiv,
      { x: [[x]], y: [[y]], z: [[z]], "marker.color": [[c]], "marker.size": [[coreSize]] },
      [2]
    );
  }

  function updateStats() {
    const rms = rmsEnergyFromTimeDomain();
    const peak = peakFromTimeDomain();
    const centroid = spectralCentroidNorm(Math.min(128, freqData.length));
    const elapsed = audioCtx ? Math.max(0, audioCtx.currentTime - startedAt) : 0;
    levelFill.style.width = Math.round(Math.min(100, rms * 420)) + "%";

    if (frameCount % 8 !== 0) return;
    statRms.textContent = rms.toFixed(3);
    statPeak.textContent = peak.toFixed(3);
    statCentroid.textContent = centroid.toFixed(3);
    statTime.textContent = elapsed.toFixed(1);
  }

  function loop() {
    if (!analyser || !timeData || !freqData) return;
    analyser.getByteTimeDomainData(timeData);
    analyser.getByteFrequencyData(freqData);
    drawBands();
    drawWaveform();
    drawSpectrogram();
    updateCloud();
    updateStats();
    frameCount += 1;
    rafId = requestAnimationFrame(loop);
  }

  function beginVisualization(label) {
    initProjection();
    initCloud();
    initCanvases();
    smoothEnergy = 0;
    smoothCentroid = 0;
    frameCount = 0;
    startedAt = audioCtx.currentTime;
    stopBtn.disabled = false;
    setStatus(label, "is-live");
    stopAnimation();
    loop();
  }

  async function startFromFile() {
    if (!player.src) {
      setStatus("Choose an audio file first, or use Mic / Tab audio.");
      return;
    }

    isStartingFile = true;
    try {
      disconnectCurrentSource();
      initAnalyser();
      const ctx = await resumeAudioContext();

      if (!mediaElementSource) {
        mediaElementSource = ctx.createMediaElementSource(player);
      }
      sourceNode = mediaElementSource;
      sourceNode.connect(analyser);
      analyser.connect(ctx.destination);
      activeSource = "file";

      try {
        await player.play();
      } catch (e) {
        setStatus("Press play on the audio control to start browser playback.", "is-ok");
      }
      beginVisualization("Live from file.");
    } catch (error) {
      if (!activeSource) {
        setStatus("This browser could not attach the audio element. Reload the page and try again.");
      }
      throw error;
    } finally {
      isStartingFile = false;
    }
  }

  async function startFromMic() {
    if (!navigator.mediaDevices || !navigator.mediaDevices.getUserMedia) {
      setStatus("Microphone capture is unavailable in this browser or context.");
      return;
    }
    if (!mediaCaptureContextReady()) {
      setMicPermission("HTTPS needed", "is-danger");
      setStatus("Mic and tab audio need HTTPS, localhost, or 127.0.0.1.");
      return;
    }

    disconnectCurrentSource();
    player.pause();
    initAnalyser();
    const ctx = await resumeAudioContext();
    try {
      mediaStream = await navigator.mediaDevices.getUserMedia(micAudioConstraints());
      await refreshMicDevices();
      setMicPermission("Allowed", "is-ok");
    } catch (error) {
      setMicPermission("Blocked", "is-danger");
      throw new Error(mediaErrorMessage(error));
    }
    sourceNode = ctx.createMediaStreamSource(mediaStream);
    sourceNode.connect(analyser);
    activeSource = "mic";
    beginVisualization("Live from microphone.");
  }

  async function startFromScreen() {
    if (!navigator.mediaDevices || !navigator.mediaDevices.getDisplayMedia) {
      setStatus("Tab-audio capture is unavailable in this browser.");
      return;
    }

    disconnectCurrentSource();
    player.pause();
    initAnalyser();
    const ctx = await resumeAudioContext();
    mediaStream = await navigator.mediaDevices.getDisplayMedia({ audio: true, video: true });
    const audioTracks = mediaStream.getAudioTracks();
    if (!audioTracks.length) {
      stopStream(mediaStream);
      mediaStream = null;
      setStatus("No tab audio found. Select a tab and enable audio sharing.");
      return;
    }
    mediaStream.getVideoTracks().forEach(function (track) { track.stop(); });
    sourceNode = ctx.createMediaStreamSource(new MediaStream(audioTracks));
    sourceNode.connect(analyser);
    activeSource = "tab";
    beginVisualization("Live from shared tab audio.");
  }

  function releaseObjectUrl() {
    if (objectUrl) {
      URL.revokeObjectURL(objectUrl);
      objectUrl = null;
    }
  }

  function stop() {
    isStopping = true;
    disconnectCurrentSource();
    player.pause();
    stopBtn.disabled = true;
    resetMeters();
    setStatus("Stopped.", "is-ok");
    isStopping = false;
  }

  function handleFile(file) {
    if (!file) return;
    releaseObjectUrl();
    objectUrl = URL.createObjectURL(file);
    player.src = objectUrl;
    player.load();
    fileLabel.textContent = file.name;
    setStatus("Loaded " + file.name + ".", "is-ok");
  }

  function wireDropZone() {
    if (!fileDrop) return;
    fileDrop.addEventListener("click", function () { fileInput.click(); });
    fileDrop.addEventListener("keydown", function (event) {
      if (event.key === "Enter" || event.key === " ") {
        event.preventDefault();
        fileInput.click();
      }
    });
    fileDrop.addEventListener("dragover", function (event) {
      event.preventDefault();
      fileDrop.classList.add("is-active");
    });
    fileDrop.addEventListener("dragleave", function () {
      fileDrop.classList.remove("is-active");
    });
    fileDrop.addEventListener("drop", function (event) {
      event.preventDefault();
      fileDrop.classList.remove("is-active");
      if (event.dataTransfer.files && event.dataTransfer.files.length) {
        handleFile(event.dataTransfer.files[0]);
      }
    });
  }

  function wireControls() {
    fileInput.addEventListener("change", function () {
      handleFile(fileInput.files && fileInput.files[0]);
    });
    startFileBtn.addEventListener("click", function () {
      startFromFile().catch(function (error) {
        setStatus("File audio failed: " + error.message);
      });
    });
    if (checkMicBtn) {
      checkMicBtn.addEventListener("click", function () {
        checkMicrophonePermission().catch(function (error) {
          setStatus("Microphone check failed: " + error.message);
        });
      });
    }
    startMicBtn.addEventListener("click", function () {
      startFromMic().catch(function (error) {
        setStatus("Microphone failed: " + error.message);
      });
    });
    startScreenBtn.addEventListener("click", function () {
      startFromScreen().catch(function (error) {
        setStatus("Tab audio failed: " + error.message);
      });
    });
    stopBtn.addEventListener("click", stop);
    clearBtn.addEventListener("click", clearCloud);
    nBinsEl.addEventListener("change", function () {
      initProjection();
      savePrefs({ nBins: nBinsEl.value });
    });
    motionEl.addEventListener("change", function () {
      savePrefs({ motion: motionEl.value });
    });
    colorByEl.addEventListener("change", function () {
      savePrefs({ colorBy: colorByEl.value });
    });
    loopSpeedEl.addEventListener("change", function () {
      savePrefs({ loopSpeed: loopSpeedEl.value });
    });
    maxPointsEl.addEventListener("change", function () {
      savePrefs({ maxPoints: maxPointsEl.value });
    });
    if (micDeviceEl) {
      micDeviceEl.addEventListener("change", function () {
        savePrefs({ micDeviceId: micDeviceEl.value });
      });
    }
    if (navigator.mediaDevices && navigator.mediaDevices.addEventListener) {
      navigator.mediaDevices.addEventListener("devicechange", function () {
        refreshMicDevices().catch(function () {
          setMicPermission("Device list unavailable", "is-warn");
        });
      });
    }
    player.addEventListener("play", function () {
      if (isStartingFile || rafId || !player.src) return;
      startFromFile().catch(function (error) {
        setStatus("File audio failed: " + error.message);
      });
    });
    player.addEventListener("pause", function () {
      if (isStopping || activeSource !== "file" || player.ended) return;
      stopAnimation();
      stopBtn.disabled = false;
      setStatus("File paused. Press play to resume live visuals.", "is-ok");
    });
    player.addEventListener("ended", function () {
      if (activeSource !== "file") return;
      stopAnimation();
      stopBtn.disabled = true;
      resetMeters();
      setStatus("File finished.", "is-ok");
    });

    if (fullscreenBtn) {
      fullscreenBtn.addEventListener("click", function () {
        const card = document.getElementById("cloudCard");
        const cloud = document.getElementById("cloud3d");
        if (!document.fullscreenElement && card) {
          card.requestFullscreen().then(function () {
            cloud.style.height = "100vh";
            if (window.Plotly) Plotly.Plots.resize(cloud);
          }).catch(function () {});
        } else if (document.exitFullscreen) {
          document.exitFullscreen();
        }
      });
      document.addEventListener("fullscreenchange", function () {
        const cloud = document.getElementById("cloud3d");
        if (!document.fullscreenElement && cloud) {
          cloud.style.height = "560px";
          if (window.Plotly) Plotly.Plots.resize(cloud);
        }
      });
    }

    document.addEventListener("keydown", function (event) {
      const tagName = event.target && event.target.tagName;
      if (tagName === "INPUT" || tagName === "SELECT" || tagName === "TEXTAREA") return;
      if (event.key === " ") {
        event.preventDefault();
        if (rafId) stop();
        else startFromFile().catch(function () {});
      }
      if (event.key.toLowerCase() === "c") clearCloud();
      if (event.key.toLowerCase() === "m") {
        startFromMic().catch(function () {});
      }
    });

    window.addEventListener("beforeunload", function () {
      disconnectCurrentSource();
      releaseObjectUrl();
    });
  }

  function applyStoredPrefs() {
    const prefs = loadPrefs();
    if (prefs.motion && motionEl) motionEl.value = prefs.motion;
    if (prefs.colorBy && colorByEl) colorByEl.value = prefs.colorBy;
    if (prefs.loopSpeed != null && loopSpeedEl) loopSpeedEl.value = prefs.loopSpeed;
    if (prefs.maxPoints != null && maxPointsEl) maxPointsEl.value = prefs.maxPoints;
    if (prefs.nBins != null && nBinsEl) nBinsEl.value = prefs.nBins;
    if (prefs.micDeviceId != null && micDeviceEl) micDeviceEl.dataset.preferredDeviceId = prefs.micDeviceId;
  }

  function init() {
    applyStoredPrefs();
    initCanvases();
    initCloud();
    wireDropZone();
    wireControls();
    const preferredMicDevice = micDeviceEl ? micDeviceEl.dataset.preferredDeviceId : "";
    refreshMicDevices(preferredMicDevice).catch(function () {
      setMicPermission("Device list unavailable", "is-warn");
    });
    refreshMicPermission().catch(function () {
      setMicPermission("Click Check mic", "is-warn");
    });
    if (!mediaCaptureContextReady()) {
      setStatus("Mic and tab audio need HTTPS, localhost, or 127.0.0.1. File mode still works.");
      return;
    }
    setStatus("Idle. Load a file, start Mic, or capture tab audio.");
  }

  init();
})();

// Drop zone wiring for the upload form on the home page.
(function () {
  const uploadForm = document.getElementById("uploadForm");
  const dropZone = document.getElementById("dropZone");
  const fileInput = document.getElementById("audio");
  const fileNameEl = document.getElementById("fileName");
  if (!uploadForm || !dropZone || !fileInput || !fileNameEl) return;

  const maxUploadMb = Number(uploadForm.dataset.maxUploadMb || 0);
  const supportedFormats = (uploadForm.dataset.supportedFormats || "")
    .split(",")
    .map(function (value) { return value.trim().toLowerCase(); })
    .filter(Boolean);

  function fileExtension(file) {
    const pieces = file.name.split(".");
    return pieces.length > 1 ? pieces.pop().toLowerCase() : "";
  }

  function showFileName() {
    if (!fileInput.files || !fileInput.files.length) {
      fileNameEl.textContent = "";
      dropZone.classList.remove("is-invalid");
      return true;
    }
    if (fileInput.files && fileInput.files.length) {
      const file = fileInput.files[0];
      const ext = fileExtension(file);
      const sizeMb = file.size / (1024 * 1024);
      const unsupported = supportedFormats.length && supportedFormats.indexOf(ext) === -1;
      const tooLarge = maxUploadMb && sizeMb > maxUploadMb;

      dropZone.classList.toggle("is-invalid", unsupported || tooLarge);
      if (unsupported) {
        fileNameEl.textContent = "Unsupported file type: " + file.name;
        return false;
      }
      if (tooLarge) {
        fileNameEl.textContent = "File is larger than " + maxUploadMb + " MB: " + file.name;
        return false;
      }
      fileNameEl.textContent = file.name;
    }
    return true;
  }

  dropZone.addEventListener("click", function () { fileInput.click(); });
  dropZone.addEventListener("keydown", function (event) {
    if (event.key === "Enter" || event.key === " ") {
      event.preventDefault();
      fileInput.click();
    }
  });
  fileInput.addEventListener("change", showFileName);
  uploadForm.addEventListener("submit", function (e) {
    if (fileInput.files && fileInput.files.length && !showFileName()) {
      e.preventDefault();
    }
  });

  dropZone.addEventListener("dragover", function (e) {
    e.preventDefault();
    dropZone.classList.add("is-active");
  });
  dropZone.addEventListener("dragleave", function () {
    dropZone.classList.remove("is-active");
  });
  dropZone.addEventListener("drop", function (e) {
    e.preventDefault();
    dropZone.classList.remove("is-active");
    if (e.dataTransfer.files && e.dataTransfer.files.length) {
      fileInput.files = e.dataTransfer.files;
      showFileName();
    }
  });
})();

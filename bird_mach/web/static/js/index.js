// Drop zone wiring for the upload form on the home page.
(function () {
  const dropZone = document.getElementById("dropZone");
  const fileInput = document.getElementById("audio");
  const fileNameEl = document.getElementById("fileName");
  if (!dropZone || !fileInput || !fileNameEl) return;

  function showFileName() {
    if (fileInput.files && fileInput.files.length) {
      fileNameEl.textContent = fileInput.files[0].name;
    }
  }

  dropZone.addEventListener("click", function () { fileInput.click(); });
  fileInput.addEventListener("change", showFileName);

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

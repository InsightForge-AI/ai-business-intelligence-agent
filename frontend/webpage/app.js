// DocuMind minimal frontend.
//
// Served by the backend service itself (mounted at /ui in backend/app.py),
// so every request below is same-origin -- no CORS setup, no API base URL
// to configure. If you ever serve this file separately, set API_BASE to
// the backend's origin (e.g. "http://127.0.0.1:8000") and prefix every
// fetch() below with it.

const API_BASE = "";

const dropzone = document.getElementById("dropzone");
const fileInput = document.getElementById("fileInput");
const dropzoneText = document.getElementById("dropzoneText");
const uploadMsg = document.getElementById("uploadMsg");
const docTableBody = document.getElementById("docTableBody");
const refreshBtn = document.getElementById("refreshBtn");
const statusDot = document.getElementById("statusDot");
const statusText = document.getElementById("statusText");
const resultPanel = document.getElementById("resultPanel");
const resultTitle = document.getElementById("resultTitle");
const resultBody = document.getElementById("resultBody");
const closeResultBtn = document.getElementById("closeResultBtn");

function formatSize(bytes) {
  if (bytes === null || bytes === undefined) return "—";
  if (bytes < 1024) return `${bytes} B`;
  if (bytes < 1024 * 1024) return `${(bytes / 1024).toFixed(1)} KB`;
  return `${(bytes / (1024 * 1024)).toFixed(1)} MB`;
}

function escapeHtml(str) {
  const div = document.createElement("div");
  div.textContent = str ?? "";
  return div.innerHTML;
}

// ---------------------------------------------------------
// Backend health check
// ---------------------------------------------------------

async function checkHealth() {
  try {
    const res = await fetch(`${API_BASE}/api/health`);
    if (!res.ok) throw new Error();
    statusDot.className = "dot ok";
    statusText.textContent = "Backend online";
  } catch {
    statusDot.className = "dot err";
    statusText.textContent = "Backend unreachable — is run.py running?";
  }
}

// ---------------------------------------------------------
// Document list
// ---------------------------------------------------------

async function loadDocuments() {
  docTableBody.innerHTML = `<tr><td colspan="5" class="empty">Loading…</td></tr>`;

  try {
    const res = await fetch(`${API_BASE}/api/documents`);
    const data = await res.json();
    const documents = data.documents || [];

    if (documents.length === 0) {
      docTableBody.innerHTML = `<tr><td colspan="5" class="empty">No documents yet — upload one above.</td></tr>`;
      return;
    }

    docTableBody.innerHTML = "";

    for (const doc of documents) {
      docTableBody.appendChild(renderRow(doc));
    }
  } catch (err) {
    docTableBody.innerHTML = `<tr><td colspan="5" class="empty">Could not load documents: ${escapeHtml(err.message)}</td></tr>`;
  }
}

function renderRow(doc) {
  const tr = document.createElement("tr");

  const badgeClass = doc.aiReady ? "processed" : "uploaded";

  tr.innerHTML = `
    <td>${escapeHtml(doc.name || "Untitled")}</td>
    <td>${escapeHtml(doc.type || "—")}</td>
    <td>${formatSize(doc.size)}</td>
    <td><span class="badge ${badgeClass}">${escapeHtml(doc.status || "Uploaded")}</span></td>
    <td>
      <div class="row-actions">
        <button class="btn btn-primary" data-action="analyze">Analyze</button>
        <button class="btn" data-action="download">Download</button>
        <button class="btn btn-danger" data-action="delete">Delete</button>
      </div>
    </td>
  `;

  tr.querySelector('[data-action="analyze"]').addEventListener("click", () => analyzeDocument(doc));
  tr.querySelector('[data-action="download"]').addEventListener("click", () => downloadDocument(doc));
  tr.querySelector('[data-action="delete"]').addEventListener("click", () => deleteDocument(doc));

  return tr;
}

// ---------------------------------------------------------
// Upload
// ---------------------------------------------------------

async function uploadFile(file) {
  uploadMsg.textContent = `Uploading ${file.name}…`;
  uploadMsg.className = "msg";

  const formData = new FormData();
  formData.append("file", file);

  try {
    const res = await fetch(`${API_BASE}/api/upload`, {
      method: "POST",
      body: formData,
    });
    const data = await res.json();

    if (!res.ok || !data.success) {
      throw new Error(data.detail || data.message || "Upload failed");
    }

    uploadMsg.textContent = `Uploaded "${data.data.name}" successfully.`;
    uploadMsg.className = "msg ok";
    await loadDocuments();
  } catch (err) {
    uploadMsg.textContent = `Upload failed: ${err.message}`;
    uploadMsg.className = "msg err";
  }
}

dropzone.addEventListener("click", () => fileInput.click());

fileInput.addEventListener("change", () => {
  if (fileInput.files.length > 0) {
    uploadFile(fileInput.files[0]);
    fileInput.value = "";
  }
});

["dragenter", "dragover"].forEach((evt) =>
  dropzone.addEventListener(evt, (e) => {
    e.preventDefault();
    dropzone.classList.add("dragover");
  })
);

["dragleave", "drop"].forEach((evt) =>
  dropzone.addEventListener(evt, (e) => {
    e.preventDefault();
    dropzone.classList.remove("dragover");
  })
);

dropzone.addEventListener("drop", (e) => {
  const file = e.dataTransfer.files[0];
  if (file) uploadFile(file);
});

// ---------------------------------------------------------
// Analyze
// ---------------------------------------------------------

async function analyzeDocument(doc) {
  const docId = doc.id || doc.file_id;

  showResultPanel(doc.name, `<div><span class="spinner"></span> Running agent → ml/nlp/cv/rag pipeline…</div>`);

  try {
    const query = encodeURIComponent("Analyze this document and generate insights");
    const res = await fetch(`${API_BASE}/api/analyze/${docId}?query=${query}`, {
      method: "POST",
    });
    const data = await res.json();

    if (!res.ok || !data.success) {
      throw new Error(data.detail || "Analysis failed");
    }

    renderResult(doc.name, data);
    await loadDocuments();
  } catch (err) {
    showResultPanel(doc.name, `<div class="msg err">Analysis failed: ${escapeHtml(err.message)}</div>`);
  }
}

function renderResult(name, data) {
  const errors = data.data && data.data.errors;

  let html = "";

  html += `<div class="result-section">
    <h3>Summary</h3>
    <pre>${escapeHtml(JSON.stringify(data.summary, null, 2))}</pre>
  </div>`;

  html += `<div class="result-section">
    <h3>Insights</h3>
    <pre>${escapeHtml(JSON.stringify(data.insights, null, 2))}</pre>
  </div>`;

  if (errors && Object.keys(errors).length > 0) {
    html += `<div class="result-section errors">
      <h3>Module errors (graceful fallback used)</h3>
      <pre>${escapeHtml(JSON.stringify(errors, null, 2))}</pre>
    </div>`;
  }

  html += `<div class="result-section">
    <h3>Full response</h3>
    <pre>${escapeHtml(JSON.stringify(data, null, 2))}</pre>
  </div>`;

  showResultPanel(name, html);
}

function showResultPanel(name, html) {
  resultTitle.textContent = `Analysis result — ${name}`;
  resultBody.innerHTML = html;
  resultPanel.hidden = false;
  resultPanel.scrollIntoView({ behavior: "smooth", block: "start" });
}

closeResultBtn.addEventListener("click", () => {
  resultPanel.hidden = true;
});

// ---------------------------------------------------------
// Download / Delete
// ---------------------------------------------------------

function downloadDocument(doc) {
  const docId = doc.id || doc.file_id;
  window.open(`${API_BASE}/api/documents/${docId}/download`, "_blank");
}

async function deleteDocument(doc) {
  const docId = doc.id || doc.file_id;
  if (!confirm(`Delete "${doc.name}"? This cannot be undone.`)) return;

  try {
    const res = await fetch(`${API_BASE}/api/documents/${docId}`, {
      method: "DELETE",
    });
    const data = await res.json();

    if (!res.ok || !data.success) {
      throw new Error(data.detail || "Delete failed");
    }

    await loadDocuments();
  } catch (err) {
    alert(`Delete failed: ${err.message}`);
  }
}

// ---------------------------------------------------------
// Init
// ---------------------------------------------------------

refreshBtn.addEventListener("click", loadDocuments);

checkHealth();
loadDocuments();

from fastapi import APIRouter
from fastapi.responses import HTMLResponse

router = APIRouter()

@router.get("/ui", response_class=HTMLResponse)
def ui():
    return """
<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>Aadhaar OCR + Fraud Detection | AlOCR</title>
  <style>
    :root{
      --bg:#0b1020;
      --card:#121a33;
      --card2:#0f1730;
      --text:#e9ecff;
      --muted:#b9c0ff;
      --accent:#6ee7ff;
      --accent2:#a78bfa;
      --danger:#ff6b6b;
      --ok:#39d98a;
      --border:rgba(255,255,255,.12);
      --shadow: 0 20px 60px rgba(0,0,0,.55);
      --radius: 18px;
    }
    *{box-sizing:border-box}
    body{
      margin:0;
      font-family: ui-sans-serif, system-ui, -apple-system, Segoe UI, Roboto, Arial;
      background: radial-gradient(1200px 600px at 20% 10%, rgba(167,139,250,.25), transparent 60%),
                  radial-gradient(1000px 600px at 80% 20%, rgba(110,231,255,.22), transparent 55%),
                  radial-gradient(900px 700px at 50% 90%, rgba(57,217,138,.14), transparent 60%),
                  var(--bg);
      color: var(--text);
      min-height:100vh;
      padding: 26px;
    }
    .wrap{max-width: 1150px; margin: 0 auto;}
    header{
      display:flex; align-items:center; justify-content:space-between;
      gap: 14px; margin-bottom: 18px;
    }
    .brand{
      display:flex; align-items:center; gap: 12px;
    }
    .logo{
      width:44px; height:44px; border-radius: 14px;
      background: linear-gradient(135deg, rgba(110,231,255,.9), rgba(167,139,250,.9));
      box-shadow: 0 14px 40px rgba(110,231,255,.15);
      display:grid; place-items:center;
      font-weight:800; color:#081025;
    }
    .title h1{margin:0; font-size: 18px; letter-spacing:.2px}
    .title p{margin:2px 0 0; color: var(--muted); font-size: 13px}
    .links{
      display:flex; gap:10px; flex-wrap:wrap;
    }
    .chip{
      border:1px solid var(--border);
      background: rgba(255,255,255,.06);
      padding: 8px 12px;
      border-radius: 999px;
      color: var(--text);
      text-decoration:none;
      font-size: 13px;
      transition: .2s ease;
    }
    .chip:hover{transform: translateY(-1px); border-color: rgba(255,255,255,.22)}
    .grid{
      display:grid;
      grid-template-columns: 1fr 1fr;
      gap: 16px;
    }
    @media (max-width: 980px){
      .grid{grid-template-columns: 1fr}
    }
    .card{
      background: linear-gradient(180deg, rgba(255,255,255,.07), rgba(255,255,255,.03));
      border: 1px solid var(--border);
      border-radius: var(--radius);
      box-shadow: var(--shadow);
      overflow:hidden;
    }
    .card .head{
      padding: 16px 16px 10px;
      border-bottom: 1px solid rgba(255,255,255,.08);
      display:flex; align-items:center; justify-content:space-between; gap:12px;
    }
    .card .head h2{
      margin:0;
      font-size: 14px;
      letter-spacing:.2px;
      color: var(--text);
    }
    .card .head small{color: var(--muted)}
    .card .body{padding: 16px;}
    .drop{
      border: 1.5px dashed rgba(255,255,255,.25);
      background: rgba(15,23,48,.55);
      border-radius: 16px;
      padding: 18px;
      display:flex;
      gap: 14px;
      align-items:center;
      justify-content:space-between;
      cursor:pointer;
      transition:.2s ease;
    }
    .drop.drag{border-color: rgba(110,231,255,.8); box-shadow: 0 0 0 4px rgba(110,231,255,.12)}
    .drop:hover{border-color: rgba(255,255,255,.35)}
    .drop .meta{display:flex; flex-direction:column; gap:4px}
    .drop .meta b{font-size: 14px}
    .drop .meta span{color: var(--muted); font-size: 12px}
    input[type=file]{display:none}
    .btns{display:flex; gap:10px; flex-wrap:wrap; margin-top: 12px}
    button{
      border:1px solid var(--border);
      background: rgba(255,255,255,.06);
      color: var(--text);
      padding: 10px 14px;
      border-radius: 12px;
      cursor:pointer;
      transition:.2s ease;
      font-weight:600;
    }
    button.primary{
      background: linear-gradient(135deg, rgba(110,231,255,.25), rgba(167,139,250,.25));
      border-color: rgba(110,231,255,.35);
    }
    button:hover{transform: translateY(-1px); border-color: rgba(255,255,255,.25)}
    button:disabled{opacity:.55; cursor:not-allowed; transform:none}
    .preview{
      margin-top: 12px;
      border-radius: 16px;
      border:1px solid rgba(255,255,255,.10);
      background: rgba(15,23,48,.45);
      overflow:hidden;
      display:grid;
      grid-template-columns: 160px 1fr;
      gap: 12px;
      align-items:stretch;
    }
    .thumb{
      width: 160px;
      height: 140px;
      background: rgba(255,255,255,.05);
      display:grid;
      place-items:center;
      overflow:hidden;
    }
    .thumb img{width:100%; height:100%; object-fit:cover}
    .pinfo{padding: 10px 12px}
    .pinfo .row{display:flex; gap:10px; flex-wrap:wrap; margin-top: 6px}
    .pill{
      padding: 6px 10px;
      border-radius: 999px;
      border:1px solid rgba(255,255,255,.14);
      font-size:12px;
      color: var(--muted);
      background: rgba(255,255,255,.05);
    }
    .status{
      display:flex; align-items:center; gap:10px; margin-top: 14px;
      padding: 10px 12px;
      border-radius: 14px;
      border:1px solid rgba(255,255,255,.12);
      background: rgba(255,255,255,.05);
    }
    .dot{width:10px; height:10px; border-radius: 999px; background: rgba(255,255,255,.25)}
    .dot.ok{background: var(--ok)}
    .dot.bad{background: var(--danger)}
    .dot.busy{
      background: var(--accent);
      animation: pulse 1.1s infinite;
    }
    @keyframes pulse{
      0%{transform:scale(1); opacity:.6}
      50%{transform:scale(1.6); opacity:1}
      100%{transform:scale(1); opacity:.6}
    }
    pre{
      margin:0;
      white-space: pre-wrap;
      word-wrap: break-word;
      font-family: ui-monospace, SFMono-Regular, Menlo, Consolas, "Liberation Mono", monospace;
      font-size: 12px;
      line-height: 1.5;
      color: #eaf0ff;
    }
    .codebox{
      background: rgba(10,16,34,.75);
      border: 1px solid rgba(255,255,255,.10);
      border-radius: 16px;
      padding: 14px;
      min-height: 360px;
      overflow:auto;
    }
    .badge{
      font-weight:800;
      padding: 6px 10px;
      border-radius: 999px;
      border:1px solid rgba(255,255,255,.14);
      background: rgba(255,255,255,.06);
      font-size: 12px;
    }
    .badge.ok{border-color: rgba(57,217,138,.35); background: rgba(57,217,138,.10)}
    .badge.bad{border-color: rgba(255,107,107,.35); background: rgba(255,107,107,.10)}
    .footer{
      margin-top: 14px;
      color: rgba(233,236,255,.68);
      font-size: 12px;
    }
  </style>
</head>
<body>
  <div class="wrap">
    <header>
      <div class="brand">
        <div class="logo">AI</div>
        <div class="title">
          <h1>AlOCR — Aadhaar OCR + Fraud Detection</h1>
          <p>Upload an Aadhaar image to extract fields and compute fraud risk (CNN + forensics).</p>
        </div>
      </div>
      <div class="links">
        <a class="chip" href="/docs" target="_blank">Swagger Docs</a>
        <a class="chip" href="/health" target="_blank">Health</a>
        <a class="chip" href="/" target="_blank">Root</a>
      </div>
    </header>

    <div class="grid">
      <!-- LEFT: Upload + Preview -->
      <section class="card">
        <div class="head">
          <div>
            <h2>Upload Aadhaar Image</h2>
            <small>Supported: .jpg, .jpeg, .png, .webp (best: clear front side)</small>
          </div>
          <span id="decisionBadge" class="badge" style="display:none;">—</span>
        </div>
        <div class="body">
          <label id="drop" class="drop" for="fileInput">
            <div class="meta">
              <b>Drag & drop your image here</b>
              <span>or click to choose a file</span>
            </div>
            <span class="pill">POST /analyze</span>
          </label>
          <input id="fileInput" type="file" accept="image/*" />

          <div class="btns">
            <button id="analyzeBtn" class="primary" disabled>Analyze</button>
            <button id="clearBtn" disabled>Clear</button>
            <button id="copyBtn" disabled>Copy JSON</button>
            <button id="downloadBtn" disabled>Download Report</button>
          </div>

          <div id="preview" class="preview" style="display:none;">
            <div class="thumb"><img id="thumbImg" alt="preview" /></div>
            <div class="pinfo">
              <div><b id="fileName">—</b></div>
              <div class="row">
                <span class="pill" id="fileSize">—</span>
                <span class="pill" id="fileType">—</span>
              </div>

              <div id="status" class="status">
                <span id="dot" class="dot"></span>
                <span id="statusText" style="color:var(--muted)">Select an image to begin.</span>
              </div>

              <div class="footer">
                Tip: For best OCR, ensure the Aadhaar is not blurry and has good lighting.
              </div>
            </div>
          </div>
        </div>
      </section>

      <!-- RIGHT: Output -->
      <section class="card">
        <div class="head">
          <div>
            <h2>Analysis Output</h2>
            <small>OCR fields + fraud scores + decision</small>
          </div>
          <span class="pill">JSON</span>
        </div>
        <div class="body">
          <div class="codebox" id="output">
            <pre id="outPre">Upload an image and click "Analyze"…</pre>
          </div>
        </div>
      </section>
    </div>
  </div>

<script>
  const fileInput   = document.getElementById("fileInput");
  const drop        = document.getElementById("drop");
  const analyzeBtn  = document.getElementById("analyzeBtn");
  const clearBtn    = document.getElementById("clearBtn");
  const copyBtn     = document.getElementById("copyBtn");
  const downloadBtn = document.getElementById("downloadBtn");

  const preview     = document.getElementById("preview");
  const thumbImg    = document.getElementById("thumbImg");
  const fileName    = document.getElementById("fileName");
  const fileSize    = document.getElementById("fileSize");
  const fileType    = document.getElementById("fileType");

  const statusBox   = document.getElementById("status");
  const statusText  = document.getElementById("statusText");
  const dot         = document.getElementById("dot");

  const outPre      = document.getElementById("outPre");
  const decisionBadge = document.getElementById("decisionBadge");

  let selectedFile = null;
  let lastJson = null;

  function bytesToSize(bytes){
    const sizes = ['B','KB','MB','GB'];
    if(bytes === 0) return '0 B';
    const i = Math.floor(Math.log(bytes) / Math.log(1024));
    return (bytes / Math.pow(1024, i)).toFixed(i === 0 ? 0 : 2) + ' ' + sizes[i];
  }

  function setStatus(type, text){
    statusText.textContent = text;
    dot.className = "dot";
    if(type === "ok") dot.classList.add("ok");
    if(type === "bad") dot.classList.add("bad");
    if(type === "busy") dot.classList.add("busy");
  }

  function setDecisionBadge(decision){
    if(!decision){
      decisionBadge.style.display = "none";
      return;
    }
    decisionBadge.style.display = "inline-flex";
    decisionBadge.textContent = decision;
    decisionBadge.className = "badge " + (decision === "GENUINE" ? "ok" : "bad");
  }

  function pretty(obj){
    return JSON.stringify(obj, null, 2);
  }

  function resetAll(){
    selectedFile = null;
    lastJson = null;
    fileInput.value = "";
    preview.style.display = "none";
    outPre.textContent = 'Upload an image and click "Analyze"…';
    analyzeBtn.disabled = true;
    clearBtn.disabled = true;
    copyBtn.disabled = true;
    downloadBtn.disabled = true;
    setDecisionBadge(null);
  }

  fileInput.addEventListener("change", () => {
    const file = fileInput.files && fileInput.files[0];
    if(!file) return;
    selectedFile = file;

    preview.style.display = "grid";
    fileName.textContent = file.name;
    fileSize.textContent = bytesToSize(file.size);
    fileType.textContent = file.type || "image/*";

    const url = URL.createObjectURL(file);
    thumbImg.src = url;

    analyzeBtn.disabled = false;
    clearBtn.disabled = false;
    copyBtn.disabled = true;
    downloadBtn.disabled = true;
    setDecisionBadge(null);

    setStatus("ok", "Ready to analyze.");
  });

  clearBtn.addEventListener("click", resetAll);

  // Drag & drop
  ["dragenter","dragover"].forEach(evt => {
    drop.addEventListener(evt, e => {
      e.preventDefault(); e.stopPropagation();
      drop.classList.add("drag");
    });
  });
  ["dragleave","drop"].forEach(evt => {
    drop.addEventListener(evt, e => {
      e.preventDefault(); e.stopPropagation();
      drop.classList.remove("drag");
    });
  });
  drop.addEventListener("drop", e => {
    const f = e.dataTransfer.files && e.dataTransfer.files[0];
    if(!f) return;
    fileInput.files = e.dataTransfer.files; // triggers change
    fileInput.dispatchEvent(new Event("change"));
  });

  analyzeBtn.addEventListener("click", async () => {
    if(!selectedFile) return;

    analyzeBtn.disabled = true;
    copyBtn.disabled = true;
    downloadBtn.disabled = true;
    setDecisionBadge(null);

    setStatus("busy", "Analyzing… please wait");
    outPre.textContent = "Running OCR + Fraud checks…";

    try{
      const formData = new FormData();
      formData.append("file", selectedFile);

      const res = await fetch("/analyze", {
        method: "POST",
        body: formData
      });

      if(!res.ok){
        const text = await res.text();
        throw new Error("Server error: " + res.status + "\\n" + text);
      }

      const data = await res.json();
      lastJson = data;

      outPre.textContent = pretty(data);

      // try to find decision
      const decision =
        data?.fraud_analysis?.decision ||
        data?.fraud_analysis?.fraud_analysis?.decision ||
        null;

      setDecisionBadge(decision);

      setStatus("ok", "Done. Review results on the right.");
      copyBtn.disabled = false;
      downloadBtn.disabled = false;

    }catch(err){
      outPre.textContent = String(err);
      setStatus("bad", "Failed. Check server logs and try again.");
    }finally{
      analyzeBtn.disabled = false;
    }
  });

  copyBtn.addEventListener("click", async () => {
    if(!lastJson) return;
    try{
      await navigator.clipboard.writeText(pretty(lastJson));
      setStatus("ok", "Copied JSON to clipboard.");
      setTimeout(() => setStatus("ok", "Ready."), 1200);
    }catch(e){
      setStatus("bad", "Clipboard blocked by browser.");
    }
  });

  downloadBtn.addEventListener("click", () => {
    if(!lastJson) return;
    const blob = new Blob([pretty(lastJson)], {type: "application/json"});
    const url = URL.createObjectURL(blob);
    const a = document.createElement("a");
    const ts = new Date().toISOString().replaceAll(":","-");
    a.href = url;
    a.download = `AlOCR_Report_${ts}.json`;
    document.body.appendChild(a);
    a.click();
    a.remove();
    URL.revokeObjectURL(url);
    setStatus("ok", "Report downloaded.");
    setTimeout(() => setStatus("ok", "Ready."), 1200);
  });

  // initial
  resetAll();
</script>
</body>
</html>
"""

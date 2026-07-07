const API_BASE = "http://localhost:59649";

export async function listIndustries() {
  const r = await fetch(`${API_BASE}/api/v1/hla/industries`);
  return r.json();
}

export async function listModules() {
  const r = await fetch(`${API_BASE}/api/v1/hla/modules`);
  return r.json();
}

export async function generateQuestionnaire(industry, modules) {
  const r = await fetch(`${API_BASE}/api/v1/hla/generate-questionnaire`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ industry, modules }),
  });
  if (!r.ok) throw new Error("Failed to generate questionnaire");
  const blob = await r.blob();
  const url = URL.createObjectURL(blob);
  const a = document.createElement("a");
  a.href = url;
  a.download = `HLA_${industry.replace(/\s+/g,"_")}.xlsx`;
  a.click();
  URL.revokeObjectURL(url);
}

export async function uploadAndAnalyze(file) {
  const fd = new FormData();
  fd.append("file", file);
  const r = await fetch(`${API_BASE}/api/v1/hla/upload-analyze`, {
    method: "POST",
    body: fd,
  });
  if (!r.ok) throw new Error("Analysis failed");
  return r.json();
}

export async function getHLAAnalysis(sessionId) {
  const r = await fetch(`${API_BASE}/api/v1/hla/${sessionId}`);
  return r.json();
}

export function streamSDD(hlaSessionId, config, onEvent, onDone, onError) {
  fetch(`${API_BASE}/api/v1/sdd/generate`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ hla_session_id: hlaSessionId, config }),
  })
    .then(async (res) => {
      const reader = res.body.getReader();
      const dec = new TextDecoder();
      let buf = "";
      while (true) {
        const { done, value } = await reader.read();
        if (done) { onDone(); break; }
        buf += dec.decode(value, { stream: true });
        const lines = buf.split("\n");
        buf = lines.pop();
        lines.forEach((l) => {
          if (l.startsWith("data:")) {
            try { onEvent(JSON.parse(l.slice(5).trim())); } catch {}
          }
        });
      }
    })
    .catch(onError);
}

export async function getSDDSummary(sessionId) {
  const r = await fetch(`${API_BASE}/api/v1/sdd/${sessionId}`);
  return r.json();
}

export async function downloadSDD(sessionId) {
  const r = await fetch(`${API_BASE}/api/v1/sdd/download/${sessionId}`);
  const blob = await r.blob();
  const url = URL.createObjectURL(blob);
  const a = document.createElement("a");
  a.href = url;
  a.download = `SDD_${sessionId}.docx`;
  a.click();
  URL.revokeObjectURL(url);
}

export function streamCWB(sddSessionId, modules, companyName, onEvent, onDone, onError) {
  fetch(`${API_BASE}/api/v1/cwb/generate`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ sdd_session_id: sddSessionId, modules, company_name: companyName }),
  })
    .then(async (res) => {
      const reader = res.body.getReader();
      const dec = new TextDecoder();
      let buf = "";
      while (true) {
        const { done, value } = await reader.read();
        if (done) { onDone(); break; }
        buf += dec.decode(value, { stream: true });
        const lines = buf.split("\n");
        buf = lines.pop();
        lines.forEach((l) => {
          if (l.startsWith("data:")) {
            try { onEvent(JSON.parse(l.slice(5).trim())); } catch {}
          }
        });
      }
    })
    .catch(onError);
}

export async function downloadCWB(sessionId, module) {
  const slug = module.toLowerCase().replace(/\s+&\s+/g,"_and_").replace(/\s+/g,"_");
  const r = await fetch(`${API_BASE}/api/v1/cwb/download/${sessionId}/${slug}`);
  const blob = await r.blob();
  const url = URL.createObjectURL(blob);
  const a = document.createElement("a");
  a.href = url;
  a.download = `CWB_${slug}.xlsx`;
  a.click();
  URL.revokeObjectURL(url);
}
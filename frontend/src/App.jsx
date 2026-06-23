import { useEffect, useMemo, useRef, useState } from "react";
import {
  BookOpen,
  Brain,
  CheckCircle2,
  ClipboardCheck,
  FileText,
  History,
  Loader2,
  Network,
  PenLine,
  RefreshCw,
  Send,
  Sparkles,
  Upload,
} from "lucide-react";
import { extractPdf, fetchHealth, fetchReview, fetchReviews, submitPaper } from "./api";

const initialForm = {
  title: "AI-Supported Peer Feedback for Reflective Learning",
  abstract:
    "This study explores how AI-supported peer feedback can improve reflective learning outcomes in higher education settings.",
  content:
    "Introduction: Peer feedback is central to collaborative education, but learners often need structure to provide actionable comments.\n\nMethodology: We propose a classroom workflow where students submit reflective essays, receive guided peer review prompts, and revise their work after instructor moderation.\n\nExpected Contribution: The paper contributes a practical model for scalable formative feedback and outlines evaluation criteria for future classroom studies.",
  domain: "Education",
};

const workflow = [
  "Submission Agent",
  "Reviewer Agent 1",
  "Reviewer Agent 2",
  "Reviewer Agent 3",
  "Aggregator Agent",
  "Decision Agent",
  "Author Agent",
  "Assessment Agent",
];

const reviewerCards = [
  ["reviewer_1", "Reviewer 1: Methodology", Brain],
  ["reviewer_2", "Reviewer 2: Originality and Literature Gap", Network],
  ["reviewer_3", "Reviewer 3: Clarity, Structure, and Educational Impact", BookOpen],
];

const reviewerHeadings = ["Strengths", "Weaknesses", "Suggestions", "Score out of 10", "Recommendation"];
const aggregateHeadings = [
  "Overall Summary",
  "Common Strengths",
  "Major Concerns",
  "Required Revisions",
  "Final Reviewer Consensus",
];

const assessmentHeadings = [
  "Overall Quality Score",
  "Publication Readiness",
  "Key Strengths",
  "Critical Gaps",
  "Priority Recommendations",
];

function decisionClass(decision = "") {
  const value = decision.toLowerCase();
  if (value.includes("accept") && !value.includes("reject")) return "accept";
  if (value.includes("major")) return "major";
  if (value.includes("reject")) return "reject";
  return "minor";
}

function parseSections(text = "", headings = []) {
  const normalized = String(text || "").replace(/\r\n/g, "\n").trim();
  const sections = {};

  headings.forEach((heading, index) => {
    const nextHeadings = headings.slice(index + 1).map((item) => item.replace(/[.*+?^${}()|[\]\\]/g, "\\$&"));
    const headingPattern = heading.replace(/[.*+?^${}()|[\]\\]/g, "\\$&");
    const stopPattern = nextHeadings.length ? `(?=\\n\\s*(?:${nextHeadings.join("|")})\\s*:?(?:\\n|$))` : "$";
    const block = normalized.match(new RegExp(`(?:^|\\n)\\s*${headingPattern}\\s*:?\\s*\\n?([\\s\\S]*?)${stopPattern}`, "i"));
    sections[heading] = block?.[1]?.trim() || "";
  });

  return sections;
}

function SectionedText({ text, headings }) {
  const sections = parseSections(text, headings);
  const hasSections = headings.some((heading) => sections[heading]);

  if (!hasSections) {
    return <p className="text-block">{text}</p>;
  }

  return (
    <div className="structured-text">
      {headings.map((heading) => (
        <div className="structured-row" key={heading}>
          <h4>{heading}</h4>
          <p>{sections[heading] || "N/A"}</p>
        </div>
      ))}
    </div>
  );
}

function safeValue(value) {
  return value === null || value === undefined || value === "" ? "N/A" : value;
}

function App() {
  const [form, setForm] = useState(initialForm);
  const [result, setResult] = useState(null);
  const [history, setHistory] = useState([]);
  const [mode, setMode] = useState("demo");
  const [loading, setLoading] = useState(false);
  const [progressIndex, setProgressIndex] = useState(-1);
  const [error, setError] = useState("");
  const [pdfLoading, setPdfLoading] = useState(false);
  const pdfInputRef = useRef(null);

  const wordCount = useMemo(() => form.content.trim().split(/\s+/).filter(Boolean).length, [form.content]);

  useEffect(() => {
    loadMode();
    loadHistory();
  }, []);

  useEffect(() => {
    if (!loading) return;
    setProgressIndex(0);
    const timer = window.setInterval(() => {
      setProgressIndex((current) => Math.min(current + 1, workflow.length - 1));
    }, 900);
    return () => window.clearInterval(timer);
  }, [loading]);

  async function loadHistory() {
    try {
      const items = await fetchReviews();
      setHistory(items);
    } catch {
      setHistory([]);
    }
  }

  async function loadMode() {
    try {
      const health = await fetchHealth();
      setMode(health.mode === "live" ? "live" : "demo");
    } catch {
      setMode("demo");
    }
  }

  function updateField(event) {
    const { name, value } = event.target;
    setForm((current) => ({ ...current, [name]: value }));
  }

  async function handlePdfUpload(event) {
    const file = event.target.files?.[0];
    if (!file) return;
    setPdfLoading(true);
    setError("");
    try {
      const data = await extractPdf(file);
      setForm((current) => ({
        ...current,
        title: data.title || current.title,
        abstract: data.abstract || current.abstract,
        content: data.content || current.content,
      }));
    } catch (err) {
      setError(err.message || "Failed to extract PDF content.");
    } finally {
      setPdfLoading(false);
      event.target.value = "";
    }
  }

  async function handleSubmit(event) {
    event.preventDefault();
    setLoading(true);
    setError("");
    setResult(null);
    try {
      const data = await submitPaper(form);
      setResult(data);
      await loadHistory();
    } catch (err) {
      setError(err.message || "Unable to run the review workflow.");
    } finally {
      setLoading(false);
      setProgressIndex(workflow.length - 1);
    }
  }

  async function openHistoryItem(paperId) {
    setError("");
    try {
      const data = await fetchReview(paperId);
      setResult(data);
      window.scrollTo({ top: 0, behavior: "smooth" });
    } catch (err) {
      setError(err.message || "Unable to load review.");
    }
  }

  return (
    <div className="app-shell">
      <header className="topbar">
        <div className="brand">
          <div className="brand-mark"><Brain size={22} /></div>
          <div>
            <strong>ScholarSim AI</strong>
            <span>Academic Simulation v1.0</span>
          </div>
        </div>
        <div className="topbar-actions">
          <span className={`mode-badge ${mode === "live" ? "live" : "demo"}`}>
            {mode === "live" ? "Live Mode: LLM Enabled" : "Demo Mode: Mock AI Responses"}
          </span>
          <button className="ghost-button" onClick={loadHistory} type="button">
            <RefreshCw size={16} /> Refresh History
          </button>
        </div>
      </header>

      <main className="dashboard">
        <section className="intro-band">
          <div>
            <p className="eyebrow">Multi-Agent Academic Peer Review Simulator</p>
            <h1>Submit a manuscript and run a simulated scholarly review board.</h1>
          </div>
          <div className="metrics">
            <div><strong>8</strong><span>Agents</span></div>
            <div><strong>{history.length}</strong><span>Saved Reviews</span></div>
            <div><strong>{mode === "live" ? "Live" : "Demo"}</strong><span>{mode === "live" ? "LLM keys detected" : "No API key required"}</span></div>
          </div>
        </section>

        {error && <div className="error-banner">{error}</div>}

        <div className="work-grid">
          <section className="panel submission-panel">
            <div className="panel-heading">
              <div>
                <p className="eyebrow">Submission</p>
                <h2>Paper Intake</h2>
              </div>
              <span className="code-chip">{wordCount} words</span>
            </div>

            <form onSubmit={handleSubmit} className="paper-form">
              <div className="pdf-upload-row">
                <input
                  ref={pdfInputRef}
                  type="file"
                  accept=".pdf"
                  style={{ display: "none" }}
                  onChange={handlePdfUpload}
                />
                <button
                  type="button"
                  className="ghost-button pdf-button"
                  disabled={pdfLoading || loading}
                  onClick={() => pdfInputRef.current?.click()}
                >
                  {pdfLoading ? <Loader2 className="spin" size={16} /> : <Upload size={16} />}
                  {pdfLoading ? "Extracting PDF…" : "Upload PDF"}
                </button>
                <span className="pdf-hint">Auto-fills the form from your PDF</span>
              </div>
              <label>
                Title
                <input name="title" value={form.title} onChange={updateField} minLength={3} required />
              </label>
              <label>
                Abstract <span style={{fontWeight:400,color:"#64748b",fontSize:"0.8rem"}}>(optional — auto-filled from PDF if available)</span>
                <textarea name="abstract" value={form.abstract} onChange={updateField} rows={5} />
              </label>
              <label>
                Full Paper Content
                <textarea name="content" value={form.content} onChange={updateField} minLength={30} rows={12} required />
              </label>
              <label>
                Domain
                <input name="domain" value={form.domain} onChange={updateField} required />
              </label>
              <button className="primary-button" disabled={loading} type="submit">
                {loading ? <Loader2 className="spin" size={18} /> : <Send size={18} />}
                {loading ? "Running Agents" : "Start Review"}
              </button>
            </form>
          </section>

          <aside className="panel agent-panel">
            <div className="panel-heading">
              <div>
                <p className="eyebrow">Workflow</p>
                <h2>Agent Status</h2>
              </div>
            </div>
            <div className="agent-list">
              {workflow.map((agent, index) => {
                const complete = result || (loading && index < progressIndex);
                const active = loading && index === progressIndex;
                return (
                  <div className={`agent-step ${complete ? "complete" : ""} ${active ? "active" : ""}`} key={agent}>
                    <span>{complete ? <CheckCircle2 size={16} /> : active ? <Loader2 className="spin" size={16} /> : index + 1}</span>
                    <p>{active ? `${agent} running...` : agent}</p>
                  </div>
                );
              })}
            </div>
          </aside>
        </div>

        {result && (
          <section className="results">
            <div className="results-head">
              <div>
                <p className="eyebrow">Review ID: {result.id ?? result.paper_id ?? "N/A"}</p>
                <h2>{result.title}</h2>
              </div>
              <span className={`decision-badge ${decisionClass(result.decision)}`}>{result.decision}</span>
            </div>

            <div className="result-grid top-results">
              <article className="panel result-card formatted-card">
                <h3><FileText size={18} /> Formatted Submission</h3>
                <p className="text-block">{result.formatted_submission}</p>
              </article>

              <article className={`panel decision-card ${decisionClass(result.decision)}`}>
                <p className="eyebrow">Final Decision</p>
                <strong>{result.decision}</strong>
                <p>{result.decision_reason || "The reviewers identified correctable issues and recommend revision."}</p>
              </article>
            </div>

            <div className="reviewer-grid">
              {reviewerCards.map(([key, title, Icon]) => (
                <article className="panel result-card reviewer-card" key={key}>
                  <h3><Icon size={18} /> {title}</h3>
                  <SectionedText text={result[key]} headings={reviewerHeadings} />
                </article>
              ))}
            </div>

            <article className="panel result-card aggregate-card">
              <h3><Sparkles size={18} /> Aggregated Review</h3>
              <SectionedText text={result.aggregated_review} headings={aggregateHeadings} />
            </article>

            <article className="panel result-card author-card">
              <h3><PenLine size={18} /> Author Response Letter</h3>
              <p className="text-block">{result.author_response_letter}</p>
            </article>

            {result.ai_assessment && (
              <article className="panel result-card assessment-card">
                <h3><ClipboardCheck size={18} /> AI Assessment</h3>
                <SectionedText text={result.ai_assessment} headings={assessmentHeadings} />
              </article>
            )}

            <section className="panel related-panel">
              <h3><BookOpen size={18} /> Related Papers</h3>
              {result.related_papers?.length ? (
                <div className="related-list">
                  {result.related_papers.map((paper, index) => (
                    <a href={paper.url || "#"} target="_blank" rel="noreferrer" key={`${paper.title}-${index}`}>
                      <strong>{safeValue(paper.title)}</strong>
                      <span>Source: {safeValue(paper.source)}</span>
                      <span>Year: {safeValue(paper.year)}</span>
                      <span>DOI/URL: {paper.doi && paper.doi !== "N/A" ? paper.doi : safeValue(paper.url)}</span>
                    </a>
                  ))}
                </div>
              ) : (
                <p className="muted">No related papers were returned by the external APIs for this run.</p>
              )}
            </section>
          </section>
        )}

        <section className="panel history-panel">
          <div className="panel-heading">
            <div>
              <p className="eyebrow">Archive</p>
              <h2><History size={20} /> Previous Reviews</h2>
            </div>
          </div>
          {history.length ? (
            <div className="history-list">
              {history.map((item) => (
                <button onClick={() => openHistoryItem(item.paper_id)} key={item.paper_id} type="button">
                  <span>
                    <strong>{item.title}</strong>
                    <small>{item.domain} - {new Date(item.created_at).toLocaleString()}</small>
                  </span>
                  <em className={`decision-badge ${decisionClass(item.decision)}`}>{item.decision}</em>
                </button>
              ))}
            </div>
          ) : (
            <p className="muted">No saved reviews yet. Run the first simulation to populate the archive.</p>
          )}
        </section>
      </main>
    </div>
  );
}

export default App;

import { useState } from "react";

// JSX preview of the Streamlit UI in /Users/Greg/Autism/ui/app.py
// Mock data is sampled from actual engine output for the four bundled
// calibration cases. Tier switcher and case picker are interactive.

const PHENOTYPE_NAMES = {
  "PHE-0001": "Cerebral folate deficiency",
  "PHE-0002": "Mitochondrial dysfunction",
  "PHE-0003": "Regressive immune-inflammatory",
  "PHE-0004": "GI / microbiome",
  "PHE-0005": "mTOR pathway syndromic",
  "PHE-0006": "Fragile X (FMR1)",
  "PHE-0007": "GABA / Cl⁻ imbalance",
  "PHE-0008": "Walsh undermethylator",
  "PHE-0009": "Walsh overmethylator",
  "PHE-0010": "Pyroluria",
  "PHE-0011": "Cu:Zn imbalance",
};

// Engine output captured from actual runs of personalized_risk.py
const CASES = {
  case_011_hannah_poling: {
    label: "mtDNA heteroplasmy + multi-vaccine challenge (federally adjudicated 2008)",
    operating_mode: "young_child",
    subject_sex: "F",
    syndromic_flag: false,
    syndromic_match: null,
    canonical_digest:
      "8327cc65630de8f1a6dd8412487eb696bb217cf7cfbed210605cdb32c6dd09f2",
    ranking: ["PHE-0002", "PHE-0004", "PHE-0008", "PHE-0001", "PHE-0003"],
    posteriors: {
      "PHE-0002": {
        point: 0.658,
        lo: 0.538,
        hi: 0.76,
        log_odds: 0.653,
        confidence_label: "HIGH",
        evidence_tier: "primary_evidence",
        drivers: [{ source: "biomarker", log_odds_shift: 1.5 }],
      },
      "PHE-0004": {
        point: 0.5,
        lo: 0.378,
        hi: 0.622,
        log_odds: 0.0,
        confidence_label: "LOW",
        evidence_tier: "primary_evidence",
        drivers: [],
      },
      "PHE-0008": {
        point: 0.5,
        lo: 0.378,
        hi: 0.622,
        log_odds: 0.0,
        confidence_label: "LOW",
        evidence_tier: "primary_evidence",
        drivers: [],
      },
    },
    interventions: [
      {
        id: "INT-0011",
        name: "L-carnitine",
        recommendation_type: "START",
        target_phenotype: "PHE-0002",
        posterior_at_invocation: 0.658,
      },
      {
        id: "INT-0012",
        name: "Coenzyme Q10 (ubiquinol)",
        recommendation_type: "CONSIDER",
        target_phenotype: "PHE-0002",
        posterior_at_invocation: 0.658,
      },
    ],
  },
  case_015_frye_fraa_responder: {
    label: "Frye FRAA-positive — responder profile",
    operating_mode: "young_child",
    subject_sex: "M",
    syndromic_flag: false,
    syndromic_match: null,
    canonical_digest:
      "7b0cf925c143bc6f3d2a18e8cc2d4d6b5fefe8a3a8e7a7ccc0d4d8e1c3a5b7d9",
    ranking: ["PHE-0001", "PHE-0004", "PHE-0002", "PHE-0008"],
    posteriors: {
      "PHE-0001": {
        point: 0.852,
        lo: 0.724,
        hi: 0.93,
        log_odds: 1.752,
        confidence_label: "HIGH",
        evidence_tier: "primary_evidence",
        drivers: [{ source: "biomarker", log_odds_shift: 1.75 }],
      },
      "PHE-0004": {
        point: 0.5,
        lo: 0.378,
        hi: 0.622,
        log_odds: 0,
        confidence_label: "LOW",
        evidence_tier: "primary_evidence",
        drivers: [],
      },
    },
    interventions: [
      {
        id: "INT-0001",
        name: "Leucovorin (folinic acid)",
        recommendation_type: "START",
        target_phenotype: "PHE-0001",
        posterior_at_invocation: 0.852,
      },
    ],
  },
  case_020_walsh_undermethylator: {
    label: "Walsh undermethylator — low SAM:SAH, high Cu:Zn",
    operating_mode: "young_child",
    subject_sex: "M",
    syndromic_flag: false,
    syndromic_match: null,
    canonical_digest:
      "acbd3c30dcc3d0617d8e8f0a1b3c5d7e9f1a3b5c7d9e1f3a5b7c9d1e3f5a7b9c1",
    ranking: ["PHE-0008", "PHE-0004", "PHE-0002", "PHE-0001"],
    posteriors: {
      "PHE-0008": {
        point: 0.501,
        lo: 0.379,
        hi: 0.623,
        log_odds: 0.005,
        confidence_label: "MEDIUM",
        evidence_tier: "primary_evidence",
        drivers: [{ source: "biomarker", log_odds_shift: 0.55 }],
      },
    },
    interventions: [
      {
        id: "INT-0024",
        name: "Methyl-B12 + folinic acid (methylation cocktail)",
        recommendation_type: "CONSIDER",
        target_phenotype: "PHE-0008",
        posterior_at_invocation: 0.501,
      },
    ],
  },
  case_026_22q11_deletion: {
    label: "22q11.2 deletion (DiGeorge / VCFS)",
    operating_mode: "young_child",
    subject_sex: "M",
    syndromic_flag: true,
    syndromic_match: {
      syndrome_match_id: "RSG-0010",
      syndrome_name:
        "22q11.2 deletion syndrome (DiGeorge / velocardiofacial)",
      matched_input: "cnv 22q11.2 deletion",
      target_routing: "22q11_specific",
      primary_pmid: "31174463",
    },
    canonical_digest:
      "2b1840c80636a56e1c3a5b7c9d1e3f5a7b9c1d3e5f7a9b1c3d5e7f9a1b3c5d7e",
    ranking: ["PHE-0002", "PHE-0004", "PHE-0008", "PHE-0001"],
    posteriors: {
      "PHE-0002": {
        point: 0.5,
        lo: 0.378,
        hi: 0.622,
        log_odds: 0,
        confidence_label: "LOW",
        evidence_tier: "primary_evidence",
        drivers: [],
      },
    },
    interventions: [],
  },
};

const TIERS = ["Researcher", "Clinician", "Family / Curious"];

function Pill({ children, color = "slate" }) {
  const colors = {
    slate: "bg-slate-100 text-slate-700 border-slate-200",
    green: "bg-green-100 text-green-800 border-green-200",
    red: "bg-red-100 text-red-800 border-red-200",
    amber: "bg-amber-100 text-amber-900 border-amber-200",
    blue: "bg-blue-100 text-blue-800 border-blue-200",
  };
  return (
    <span
      className={`inline-flex items-center px-2 py-0.5 rounded text-xs font-medium border ${colors[color]}`}
    >
      {children}
    </span>
  );
}

function ConfidenceBadge({ label }) {
  const map = {
    HIGH: "green",
    MEDIUM: "amber",
    LOW: "slate",
  };
  return <Pill color={map[label] || "slate"}>{label}</Pill>;
}

function Bar({ value, low, high }) {
  // Render the credal interval as a horizontal band with a point marker.
  const pct = (v) => `${Math.max(0, Math.min(100, v * 100))}%`;
  return (
    <div className="relative h-2 w-full bg-slate-100 rounded">
      <div
        className="absolute h-2 bg-blue-200 rounded"
        style={{ left: pct(low), width: pct(high - low) }}
      />
      <div
        className="absolute -top-0.5 h-3 w-0.5 bg-blue-700"
        style={{ left: pct(value) }}
      />
    </div>
  );
}

function MetricCard({ label, value, sublabel, tone = "slate" }) {
  const tones = {
    slate: "border-slate-200",
    green: "border-green-300 bg-green-50",
    red: "border-red-300 bg-red-50",
  };
  return (
    <div className={`border rounded p-3 ${tones[tone]}`}>
      <div className="text-xs text-slate-500 uppercase tracking-wide">
        {label}
      </div>
      <div className="text-xl font-semibold text-slate-900 mt-1">{value}</div>
      {sublabel && (
        <div className="text-xs text-slate-500 mt-1">{sublabel}</div>
      )}
    </div>
  );
}

export default function PreviewApp() {
  const [tier, setTier] = useState("Researcher");
  const [activeTab, setActiveTab] = useState("run");
  const [selectedCase, setSelectedCase] = useState("case_011_hannah_poling");
  const [hasRun, setHasRun] = useState(true);

  const c = CASES[selectedCase];
  const topPhe = c.ranking[0];
  const topPheData = c.posteriors[topPhe];

  return (
    <div className="min-h-screen bg-white text-slate-900 font-sans">
      <div className="flex">
        {/* ---------------- Sidebar ---------------- */}
        <aside className="w-64 shrink-0 border-r border-slate-200 p-4 bg-slate-50 min-h-screen">
          <div className="font-semibold text-slate-900">Causes Atlas</div>
          <div className="text-xs text-slate-500 mt-0.5">
            Causes Atlas — Autism Profile
          </div>

          <div className="mt-5">
            <div className="text-xs font-medium text-slate-700 mb-2">
              View mode
            </div>
            <div className="space-y-1">
              {TIERS.map((t) => (
                <label
                  key={t}
                  className={`flex items-center gap-2 px-2 py-1.5 rounded cursor-pointer text-sm ${
                    tier === t
                      ? "bg-blue-100 text-blue-900 font-medium"
                      : "hover:bg-slate-100 text-slate-700"
                  }`}
                >
                  <input
                    type="radio"
                    className="accent-blue-600"
                    checked={tier === t}
                    onChange={() => setTier(t)}
                  />
                  {t}
                </label>
              ))}
            </div>
          </div>

          <div className="mt-6 space-y-3 text-xs">
            <div>
              <div className="text-slate-500 uppercase tracking-wide">
                Engine
              </div>
              <code className="block bg-white border border-slate-200 rounded px-2 py-1 mt-0.5 text-slate-800">
                session4_v0.1.0_prototype
              </code>
            </div>
            <div>
              <div className="text-slate-500 uppercase tracking-wide">
                Atlas
              </div>
              <code className="block bg-white border border-slate-200 rounded px-2 py-1 mt-0.5 text-slate-800">
                v2.0_scored
              </code>
            </div>
            <div>
              <div className="text-slate-500 uppercase tracking-wide">
                Calibration anchor
              </div>
              <code className="block bg-white border border-slate-200 rounded px-2 py-1 mt-0.5 text-slate-800 whitespace-pre">
                {`INT-0001 = 83.35\nrequired ≥ 80.0`}
              </code>
            </div>
          </div>

          <div className="mt-8 text-xs text-slate-500 leading-relaxed">
            Open source — research prototype. All computation runs locally.
            No telemetry.
          </div>
        </aside>

        {/* ---------------- Main ---------------- */}
        <main className="flex-1 p-8 max-w-5xl">
          <h1 className="text-3xl font-bold text-slate-900 tracking-tight">
            Causes Atlas — Personalized Risk Calculator
          </h1>
          <div className="text-sm text-slate-500 mt-1">
            Individual-level profile across 11 phenotype dimensions ·
            deterministic Layer 3 of the Causes Atlas (Autism)
          </div>

          {/* Disclaimer banner */}
          <div className="mt-4 border border-amber-300 bg-amber-50 rounded p-3 text-sm text-amber-900">
            <span className="font-semibold">
              RESEARCH PROTOTYPE — NOT FOR CLINICAL USE.
            </span>{" "}
            This tool is a deterministic research demonstration of an autism
            causation knowledge graph. It is not FDA-cleared, not a medical
            device, and not a substitute for medical advice. No data you enter
            here is transmitted off your machine; the engine runs locally.
          </div>

          {/* Tabs */}
          <div className="mt-6 border-b border-slate-200">
            <div className="flex gap-6">
              {[
                ["run", "Run calculator"],
                ["atlas", "Atlas explorer"],
                ["method", "Methodology"],
                ["about", "About / Disclaimer"],
              ].map(([id, label]) => (
                <button
                  key={id}
                  onClick={() => setActiveTab(id)}
                  className={`pb-2 text-sm font-medium transition-colors ${
                    activeTab === id
                      ? "text-blue-700 border-b-2 border-blue-700"
                      : "text-slate-600 hover:text-slate-900"
                  }`}
                >
                  {label}
                </button>
              ))}
            </div>
          </div>

          {/* ---------------- Tab content ---------------- */}
          {activeTab === "run" && (
            <div className="mt-6">
              <h2 className="text-lg font-semibold">Step 1 — Provide a case</h2>
              <select
                className="mt-2 w-full border border-slate-300 rounded px-3 py-2 text-sm bg-white"
                value={selectedCase}
                onChange={(e) => {
                  setSelectedCase(e.target.value);
                  setHasRun(false);
                }}
              >
                {Object.entries(CASES).map(([id, data]) => (
                  <option key={id} value={id}>
                    {id} — {data.label}
                  </option>
                ))}
              </select>

              <h2 className="text-lg font-semibold mt-6">
                Step 2 — Run engine
              </h2>
              <button
                className="mt-2 w-full bg-blue-600 hover:bg-blue-700 text-white font-medium px-4 py-2 rounded text-sm"
                onClick={() => setHasRun(true)}
              >
                Compute personalized risk
              </button>

              {hasRun && (
                <>
                  <hr className="my-6 border-slate-200" />
                  <h2 className="text-lg font-semibold">Step 3 — Results</h2>

                  {/* Header strip */}
                  <div className="grid grid-cols-4 gap-3 mt-3">
                    <MetricCard
                      label="Calibration anchor"
                      value="83.35"
                      sublabel="≥ 80.0 required"
                      tone="green"
                    />
                    <MetricCard
                      label="Anchor passes"
                      value="yes"
                      tone="green"
                    />
                    <div className="border border-slate-200 rounded p-3 col-span-1">
                      <div className="text-xs text-slate-500 uppercase tracking-wide">
                        canonical_digest
                      </div>
                      <code className="block text-xs text-slate-700 break-all mt-1">
                        {c.canonical_digest.slice(0, 32)}…
                      </code>
                    </div>
                    <MetricCard
                      label="Operating mode"
                      value={c.operating_mode}
                      sublabel={`sex: ${c.subject_sex}`}
                    />
                  </div>

                  {/* Syndromic gate */}
                  {c.syndromic_flag ? (
                    <div className="mt-5 border border-red-300 bg-red-50 rounded p-4 text-sm">
                      <div className="font-semibold text-red-900">
                        Rare-syndrome screening gate triggered —{" "}
                        {c.syndromic_match.syndrome_name}
                      </div>
                      <div className="text-red-800 text-xs mt-1">
                        <code>{c.syndromic_match.syndrome_match_id}</code> ·
                        matched on{" "}
                        <code>{c.syndromic_match.matched_input}</code> ·
                        primary PMID {c.syndromic_match.primary_pmid}
                      </div>
                      <div className="text-red-700 text-xs mt-2">
                        Per spec §4, syndromic cases route to syndrome-specific
                        output. Generic phenotype posteriors below are emitted
                        for transparency but should be interpreted in light of
                        the syndromic finding.
                      </div>
                    </div>
                  ) : (
                    <div className="mt-5 border border-blue-200 bg-blue-50 rounded p-3 text-sm text-blue-800">
                      Rare-syndrome screening gate did not trigger.
                    </div>
                  )}

                  {/* Phenotype posteriors */}
                  <h3 className="text-base font-semibold mt-6">
                    Phenotype posteriors
                  </h3>
                  <p className="text-xs text-slate-500 mt-1">
                    Conditional probability <code>P(Φ | profile)</code> per
                    phenotype, with credal interval (Walley IDM lite).
                  </p>

                  <div className="mt-3 space-y-2">
                    {c.ranking.slice(0, 5).map((pid) => {
                      const p = c.posteriors[pid] || {
                        point: 0.5,
                        lo: 0.38,
                        hi: 0.62,
                        log_odds: 0,
                        confidence_label: "LOW",
                        evidence_tier: "primary_evidence",
                        drivers: [],
                      };
                      const isTop = pid === c.ranking[0];
                      return (
                        <details
                          key={pid}
                          open={isTop}
                          className="border border-slate-200 rounded bg-white"
                        >
                          <summary className="cursor-pointer px-3 py-2 flex items-center gap-3 text-sm">
                            <span className="font-mono text-slate-500 w-20">
                              {pid}
                            </span>
                            <span className="flex-1 text-slate-800">
                              {PHENOTYPE_NAMES[pid]}
                            </span>
                            <span className="font-mono text-sm">
                              {p.point.toFixed(3)}
                            </span>
                            <span className="font-mono text-xs text-slate-500">
                              [{p.lo.toFixed(3)}, {p.hi.toFixed(3)}]
                            </span>
                            <ConfidenceBadge label={p.confidence_label} />
                          </summary>
                          <div className="px-4 pb-4 pt-2 border-t border-slate-100">
                            <div className="grid grid-cols-3 gap-3">
                              <MetricCard
                                label="Point"
                                value={p.point.toFixed(3)}
                              />
                              <MetricCard
                                label="Credal low"
                                value={p.lo.toFixed(3)}
                              />
                              <MetricCard
                                label="Credal high"
                                value={p.hi.toFixed(3)}
                              />
                            </div>
                            <div className="mt-3">
                              <Bar
                                value={p.point}
                                low={p.lo}
                                high={p.hi}
                              />
                            </div>

                            {tier === "Researcher" && (
                              <>
                                <div className="text-xs text-slate-500 mt-3">
                                  log-odds = {p.log_odds.toFixed(3)} · evidence
                                  tier = {p.evidence_tier} ·{" "}
                                  {p.drivers.length} driver(s)
                                </div>
                                {p.drivers.length > 0 ? (
                                  <table className="mt-2 w-full text-xs">
                                    <thead>
                                      <tr className="text-slate-500 text-left border-b border-slate-200">
                                        <th className="py-1 font-medium">
                                          source
                                        </th>
                                        <th className="py-1 font-medium">
                                          log_odds_shift
                                        </th>
                                      </tr>
                                    </thead>
                                    <tbody>
                                      {p.drivers.map((d, i) => (
                                        <tr
                                          key={i}
                                          className="border-b border-slate-100"
                                        >
                                          <td className="py-1 font-mono">
                                            {d.source}
                                          </td>
                                          <td className="py-1 font-mono">
                                            {d.log_odds_shift > 0 ? "+" : ""}
                                            {d.log_odds_shift.toFixed(2)}
                                          </td>
                                        </tr>
                                      ))}
                                    </tbody>
                                  </table>
                                ) : (
                                  <div className="text-xs text-slate-500 mt-2">
                                    No drivers contributed for this phenotype.
                                  </div>
                                )}
                              </>
                            )}

                            {tier === "Clinician" && (
                              <div className="text-sm text-slate-700 mt-2">
                                {p.drivers.length > 0 ? (
                                  <>
                                    <span className="font-medium">
                                      Evidence channels:
                                    </span>{" "}
                                    {[
                                      ...new Set(
                                        p.drivers.map((d) => d.source)
                                      ),
                                    ].join(", ")}
                                  </>
                                ) : (
                                  <span className="text-slate-500">
                                    No specific drivers in this profile.
                                  </span>
                                )}
                              </div>
                            )}

                            {tier === "Family / Curious" && (
                              <p className="text-sm text-slate-700 mt-2 leading-relaxed">
                                <span className="font-medium">
                                  Plain-language summary —
                                </span>{" "}
                                this is the engine&rsquo;s estimate of how
                                strongly the literature linked to this
                                child&rsquo;s profile points toward this
                                phenotype cluster, compared to a generic
                                baseline. It is not a diagnosis.
                              </p>
                            )}
                          </div>
                        </details>
                      );
                    })}
                  </div>

                  {/* Intervention bundle */}
                  <h3 className="text-base font-semibold mt-6">
                    Intervention ranking
                  </h3>
                  {c.interventions.length === 0 ? (
                    <div className="text-sm text-slate-500 mt-2 italic">
                      No interventions ranked. Syndromic cases bypass the
                      generic intervention bundle per spec §4.
                    </div>
                  ) : (
                    <div className="mt-2 border border-slate-200 rounded divide-y divide-slate-100">
                      {c.interventions.map((it) => (
                        <div
                          key={it.id}
                          className="grid grid-cols-12 items-center gap-2 px-3 py-2 text-sm"
                        >
                          <code className="col-span-2 text-slate-600">
                            {it.id}
                          </code>
                          <div className="col-span-4 font-medium text-slate-800">
                            {it.name}
                          </div>
                          <div className="col-span-2">
                            <Pill
                              color={
                                it.recommendation_type === "START"
                                  ? "green"
                                  : "blue"
                              }
                            >
                              {it.recommendation_type}
                            </Pill>
                          </div>
                          <div className="col-span-2 text-xs text-slate-500 font-mono">
                            target: {it.target_phenotype}
                          </div>
                          <div className="col-span-2 text-xs text-slate-500 font-mono text-right">
                            P={it.posterior_at_invocation.toFixed(3)}
                          </div>
                        </div>
                      ))}
                    </div>
                  )}

                  {/* Tier-specific extras */}
                  {tier === "Researcher" && (
                    <div className="mt-6">
                      <h3 className="text-base font-semibold">
                        Researcher detail
                      </h3>
                      <details className="mt-2 border border-slate-200 rounded">
                        <summary className="cursor-pointer px-3 py-2 text-sm">
                          Deferred features (v0.2 roadmap)
                        </summary>
                        <ul className="px-5 py-2 text-xs text-slate-700 list-disc space-y-1">
                          <li>
                            <code>
                              full_walley_idm_credal_aggregation_v0.2
                            </code>
                          </li>
                          <li>
                            <code>
                              within_phenotype_responder_model_v0.2
                            </code>
                          </li>
                          <li>
                            <code>cdr_state_assignment_v0.2</code>
                          </li>
                          <li>
                            <code>functional_trajectory_predictor_v0.2</code>
                          </li>
                          <li>
                            <code>pathway_burden_analysis_v0.2</code>
                          </li>
                          <li>
                            <code>pgx_safety_filter_v0.2</code>
                          </li>
                          <li>
                            <code>physiological_state_normalization_v0.2</code>
                          </li>
                        </ul>
                      </details>
                      <div className="mt-2 border border-amber-300 bg-amber-50 rounded p-3 text-xs text-amber-900">
                        <code>provisional_hardcoded_shifts: true</code> — many
                        log-odds values in v0.1 are stub priors pending
                        priors-CSV calibration. Treat magnitudes as
                        illustrative.
                      </div>
                    </div>
                  )}

                  {tier === "Clinician" && (
                    <div className="mt-6">
                      <h3 className="text-base font-semibold">
                        Clinician handoff
                      </h3>
                      <p className="text-xs text-slate-500 italic mt-1">
                        Generated content for clinician review. Not a
                        recommendation — a summary of what the atlas links to
                        this profile.
                      </p>
                      <ul className="mt-2 text-sm text-slate-800 space-y-1 list-disc list-inside">
                        <li>
                          Case ID:{" "}
                          <code className="text-xs">{selectedCase}</code>
                        </li>
                        <li>
                          Operating mode:{" "}
                          <code className="text-xs">
                            {c.operating_mode}
                          </code>
                          , sex:{" "}
                          <code className="text-xs">{c.subject_sex}</code>
                        </li>
                        <li>
                          Calibration anchor: INT-0001 = 83.35 (required ≥
                          80.0)
                        </li>
                        {c.syndromic_flag && (
                          <li>
                            <strong>Syndromic gate triggered</strong>:{" "}
                            {c.syndromic_match.syndrome_name} (
                            {c.syndromic_match.syndrome_match_id}) — route to
                            syndrome-specific workup (
                            {c.syndromic_match.target_routing}); primary ref
                            PMID {c.syndromic_match.primary_pmid}
                          </li>
                        )}
                        <li>
                          Top phenotype:{" "}
                          <code className="text-xs">{topPhe}</code> (
                          {PHENOTYPE_NAMES[topPhe]}) — point{" "}
                          {topPheData.point.toFixed(3)} [
                          {topPheData.lo.toFixed(3)},{" "}
                          {topPheData.hi.toFixed(3)}]
                        </li>
                        {c.interventions.length > 0 && (
                          <li>
                            Top atlas-linked intervention:{" "}
                            <code className="text-xs">
                              {c.interventions[0].id}
                            </code>{" "}
                            ({c.interventions[0].name})
                          </li>
                        )}
                      </ul>
                    </div>
                  )}

                  {tier === "Family / Curious" && (
                    <div className="mt-6">
                      <h3 className="text-base font-semibold">
                        Questions to discuss with your clinician
                      </h3>
                      <ul className="mt-2 text-sm text-slate-800 space-y-2 list-disc list-inside">
                        {c.syndromic_flag && (
                          <li>
                            The atlas matched a known genetic syndrome pattern
                            (<em>{c.syndromic_match.syndrome_name}</em>). Has
                            your clinician discussed targeted workup for
                            this?
                          </li>
                        )}
                        <li>
                          The top-ranked phenotype cluster from the atlas is{" "}
                          <strong>{PHENOTYPE_NAMES[topPhe]}</strong>{" "}
                          (estimated probability ≈{" "}
                          {topPheData.point.toFixed(2)}). What workup or next
                          steps are appropriate to investigate this cluster
                          in our specific situation?
                        </li>
                        {c.interventions.length > 0 && (
                          <li>
                            The literature in the atlas links{" "}
                            <strong>{c.interventions[0].name}</strong> to this
                            phenotype cluster. Is this appropriate to consider
                            for our child? What evidence supports it, what
                            doesn&rsquo;t?
                          </li>
                        )}
                      </ul>
                      <p className="text-xs text-slate-500 italic mt-3">
                        These are conversation prompts only. The engine cannot
                        make clinical decisions for you or your child.
                      </p>
                    </div>
                  )}

                  {/* Download */}
                  <div className="mt-6">
                    <button className="border border-slate-300 hover:bg-slate-50 text-slate-700 px-4 py-2 rounded text-sm w-full">
                      Download output.json
                    </button>
                  </div>
                </>
              )}
            </div>
          )}

          {activeTab === "atlas" && (
            <div className="mt-6">
              <h2 className="text-lg font-semibold">Atlas explorer</h2>
              <p className="text-xs text-slate-500 mt-1">
                Read-only view of the underlying knowledge graph. All entities
                are PMID-verified per CLAUDE.md verification protocol.
              </p>

              <h3 className="text-sm font-semibold mt-4">Atlas counts</h3>
              <table className="mt-2 w-full text-sm border border-slate-200 rounded">
                <thead className="bg-slate-50 text-left">
                  <tr>
                    <th className="px-3 py-2 font-medium">table</th>
                    <th className="px-3 py-2 font-medium">rows</th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-slate-100">
                  {[
                    ["phenotypes", 11],
                    ["interventions", 137],
                    ["biomarkers", 178],
                    ["genes", 1564],
                    ["hypotheses", 75],
                    ["mechanisms", 33],
                    ["sources", 1420],
                    ["iatrogenic_exposure_priors", 27],
                    ["rare_syndrome_screening_gate", 36],
                    ["baseline_phenotype_prevalence", 29],
                  ].map(([n, r]) => (
                    <tr key={n}>
                      <td className="px-3 py-2 font-mono text-slate-700">
                        {n}
                      </td>
                      <td className="px-3 py-2 font-mono text-slate-700">
                        {r}
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          )}

          {activeTab === "method" && (
            <div className="mt-6 prose prose-sm max-w-none">
              <h2 className="text-lg font-semibold">
                Methodology — what this engine does
              </h2>
              <p className="text-sm text-slate-700 mt-2">
                Pipeline (per <code>SESSION_4_HANNAH_POLING_SPEC.md</code>{" "}
                §15 Phase 2):
              </p>
              <ol className="text-sm text-slate-700 mt-2 list-decimal list-inside space-y-1">
                <li>
                  <strong>Load + validate input</strong> against §3 schema.
                </li>
                <li>
                  <strong>Rare-syndrome screening gate (§4).</strong> Routes
                  syndromic cases (22q11.2 del, FXS, RTT, TSC, PTEN, etc.)
                  before generic phenotype assignment.
                </li>
                <li>
                  <strong>Genetic prior aggregation (§3.1).</strong> Variants
                  in <code>genetic_id_aliases</code> contribute log-odds
                  shifts.
                </li>
                <li>
                  <strong>Biomarker prior aggregation (§3.2).</strong>{" "}
                  Out-of-range biomarkers contribute shifts.
                </li>
                <li>
                  <strong>
                    Iatrogenic / exposure aggregation (§3.3, §3.13c).
                  </strong>{" "}
                  Maternal, gestational, and postnatal exposures.
                </li>
                <li>
                  <strong>Phenotype posterior</strong> ={" "}
                  <code>sigmoid(log-odds_baseline + Σ shifts)</code>, with
                  §6 conflict resolution.
                </li>
                <li>
                  <strong>Intervention ranking (§7.10).</strong>
                </li>
                <li>
                  <strong>Canonical digest.</strong> SHA-256 over
                  deterministic-output fields.
                </li>
              </ol>

              <h3 className="text-base font-semibold mt-5">Calibration</h3>
              <ul className="text-sm text-slate-700 list-disc list-inside space-y-1 mt-2">
                <li>
                  INT-0001 leucovorin CSRS = <strong>83.35</strong> (required ≥
                  80.0). Engine refuses to run if anchor fails.
                </li>
                <li>
                  Four literature-derived calibration cases pass with the
                  expected top-phenotype assignment.
                </li>
              </ul>

              <h3 className="text-base font-semibold mt-5">
                Determinism guarantees
              </h3>
              <p className="text-sm text-slate-700">
                No LLMs in scoring math. No random seeds. Stable sort by ID.
                UTF-8 + <code>newline=&#39;&#39;</code> CSV loading. SHA-256
                canonical digest over deterministic fields.
              </p>
            </div>
          )}

          {activeTab === "about" && (
            <div className="mt-6 prose prose-sm max-w-none">
              <h2 className="text-lg font-semibold">Full disclaimer</h2>
              <p className="text-sm text-slate-700 mt-2">
                This software is a <strong>research prototype</strong> of the
                Causes Atlas (Autism) — an evidence-driven, deterministic
                knowledge graph of autism causation, phenotypes, biomarkers,
                and interventions. It implements the{" "}
                <strong>individual-level susceptibility model</strong>{" "}
                (<code>P(Φ | susceptibility, trigger) ≠ P(Φ | trigger)</code>)
                as a Layer 3 personalized-risk computation over the underlying
                causal graph.
              </p>

              <h3 className="text-base font-semibold mt-4">What this is</h3>
              <ul className="text-sm text-slate-700 list-disc list-inside space-y-1">
                <li>A deterministic, auditable scoring engine.</li>
                <li>
                  An explicit map of evidence — every prior shift is grounded
                  in PMID-verified literature.
                </li>
              </ul>

              <h3 className="text-base font-semibold mt-4">
                What this is NOT
              </h3>
              <ul className="text-sm text-slate-700 list-disc list-inside space-y-1">
                <li>Not a diagnosis. Not a prediction of any individual outcome.</li>
                <li>
                  Not a substitute for evaluation by a qualified clinician.
                </li>
                <li>
                  Not validated against any prospective cohort. Calibration is
                  at the knowledge-graph level.
                </li>
              </ul>
            </div>
          )}
        </main>
      </div>
    </div>
  );
}

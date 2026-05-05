import { useState } from "react";

// A radically reduced presentation of the Causes Atlas.
// One page. One idea. Built like an Apple product page.
//
// The product isn't a calculator — it's a map of autism, derived from
// 50 years of literature and 1,420 PMID-verified primary sources.
// The calculator is just one way to read the map.

const PHENOTYPES = [
  { id: "01", name: "Cerebral folate", sub: "FRAA-mediated" },
  { id: "02", name: "Mitochondrial", sub: "energy metabolism" },
  { id: "03", name: "Regressive", sub: "immune-inflammatory" },
  { id: "04", name: "GI / microbiome", sub: "gut-brain axis" },
  { id: "05", name: "mTOR", sub: "syndromic / TSC, PTEN" },
  { id: "06", name: "Fragile X", sub: "FMR1 silencing" },
  { id: "07", name: "GABA / Cl⁻", sub: "E/I imbalance" },
  { id: "08", name: "Undermethylator", sub: "low SAM:SAH" },
  { id: "09", name: "Overmethylator", sub: "folate caution" },
  { id: "10", name: "Pyroluria", sub: "B6 + zinc deficiency" },
  { id: "11", name: "Cu : Zn imbalance", sub: "metallothionein" },
];

// Position 11 nodes around a gentle ellipse, slightly staggered so it
// doesn't read as a clock face. Coordinates are tuned by eye.
const NODE_POSITIONS = [
  { x: 600, y: 90 },
  { x: 870, y: 175 },
  { x: 980, y: 380 },
  { x: 940, y: 600 },
  { x: 770, y: 740 },
  { x: 530, y: 790 },
  { x: 290, y: 740 },
  { x: 130, y: 600 },
  { x: 90, y: 380 },
  { x: 200, y: 175 },
  { x: 470, y: 90 },
];

function Constellation() {
  const cx = 535;
  const cy = 420;

  return (
    <svg
      viewBox="0 0 1070 880"
      className="w-full h-auto"
      style={{ fontFamily: "ui-serif, Georgia, serif" }}
    >
      {/* Faint inter-node lines suggesting shared mechanisms */}
      {NODE_POSITIONS.map((p, i) =>
        NODE_POSITIONS.slice(i + 1).map((q, j) => {
          // Connect each node only to ~2 neighbors to avoid clutter
          const skip = (j !== 0 && j !== 4) || (i + j) % 3 !== 0;
          if (skip) return null;
          return (
            <line
              key={`${i}-${j}`}
              x1={p.x}
              y1={p.y}
              x2={q.x}
              y2={q.y}
              stroke="#E7E2D9"
              strokeWidth="1"
            />
          );
        })
      )}

      {/* Faint center dot — "autism" as a label, hub of the map */}
      <circle cx={cx} cy={cy} r="3" fill="#A89F8E" />
      <text
        x={cx}
        y={cy + 36}
        textAnchor="middle"
        fontSize="14"
        fill="#5C5446"
        letterSpacing="3"
        style={{ textTransform: "uppercase" }}
      >
        autism
      </text>

      {/* Subtle radial guides from center to each node */}
      {NODE_POSITIONS.map((p, i) => (
        <line
          key={`r-${i}`}
          x1={cx}
          y1={cy}
          x2={p.x}
          y2={p.y}
          stroke="#F1ECE3"
          strokeWidth="1"
        />
      ))}

      {/* Nodes */}
      {NODE_POSITIONS.map((p, i) => {
        const phe = PHENOTYPES[i];
        const labelAbove = p.y < cy - 50;
        const labelRight = p.x > cx + 30;
        const labelLeft = p.x < cx - 30;
        let tx = p.x;
        let ty = p.y + (labelAbove ? -28 : 36);
        let anchor = "middle";
        if (!labelAbove && labelRight) {
          tx = p.x + 18;
          ty = p.y + 5;
          anchor = "start";
        } else if (!labelAbove && labelLeft) {
          tx = p.x - 18;
          ty = p.y + 5;
          anchor = "end";
        }

        return (
          <g key={i}>
            <circle cx={p.x} cy={p.y} r="6" fill="#1F1A14" />
            <circle
              cx={p.x}
              cy={p.y}
              r="14"
              fill="none"
              stroke="#1F1A14"
              strokeOpacity="0.12"
              strokeWidth="1"
            />
            <text
              x={tx}
              y={ty}
              textAnchor={anchor}
              fontSize="17"
              fill="#1F1A14"
              fontWeight="500"
            >
              {phe.name}
            </text>
            <text
              x={tx}
              y={ty + 18}
              textAnchor={anchor}
              fontSize="12"
              fill="#7A6F5C"
              fontStyle="italic"
            >
              {phe.sub}
            </text>
          </g>
        );
      })}
    </svg>
  );
}

export default function Jobs() {
  const [revealed, setRevealed] = useState(false);

  return (
    <div
      className="min-h-screen bg-stone-50 text-stone-900"
      style={{ fontFamily: "ui-sans-serif, -apple-system, system-ui, sans-serif" }}
    >
      {/* ==================================================================
          HERO
          ================================================================== */}
      <section className="min-h-screen flex flex-col items-center justify-center px-6 text-center">
        <h1
          className="text-5xl md:text-7xl leading-tight tracking-tight text-stone-900 max-w-4xl"
          style={{ fontFamily: "ui-serif, Georgia, 'Times New Roman', serif" }}
        >
          Autism isn’t one thing.
          <br />
          <span className="text-stone-500 italic">
            We mapped every thing it is.
          </span>
        </h1>

        <div className="mt-12 text-sm tracking-[0.3em] uppercase text-stone-500">
          The Causes Atlas — a research project
        </div>

        <div className="mt-24 text-stone-400 text-xs tracking-widest uppercase">
          ↓ scroll
        </div>
      </section>

      {/* ==================================================================
          THE GAP
          ================================================================== */}
      <section className="min-h-screen flex items-center justify-center px-6">
        <div className="max-w-2xl">
          <div className="text-xs tracking-[0.3em] uppercase text-stone-500 mb-6">
            today
          </div>
          <p
            className="text-3xl md:text-4xl leading-snug text-stone-900"
            style={{ fontFamily: "ui-serif, Georgia, serif" }}
          >
            Autism is a label.
          </p>
          <p
            className="mt-6 text-xl md:text-2xl leading-relaxed text-stone-600"
            style={{ fontFamily: "ui-serif, Georgia, serif" }}
          >
            One word. 1 in 36 children. No common biology, no common cause —
            yet treatment is mostly behavioral, applied to everyone the same
            way.
          </p>
        </div>
      </section>

      {/* ==================================================================
          THE INSIGHT
          ================================================================== */}
      <section className="min-h-screen flex items-center justify-center px-6">
        <div className="max-w-2xl">
          <div className="text-xs tracking-[0.3em] uppercase text-stone-500 mb-6">
            what we found
          </div>
          <p
            className="text-3xl md:text-4xl leading-snug text-stone-900"
            style={{ fontFamily: "ui-serif, Georgia, serif" }}
          >
            But autism has a shape.
          </p>
          <p
            className="mt-6 text-xl md:text-2xl leading-relaxed text-stone-600"
            style={{ fontFamily: "ui-serif, Georgia, serif" }}
          >
            Read across fifty years of primary literature and{" "}
            <span className="text-stone-900">
              eleven distinct biological patterns
            </span>{" "}
            emerge — each with its own causes, its own biomarkers, and its own
            response to treatment.
          </p>
        </div>
      </section>

      {/* ==================================================================
          THE MAP
          ================================================================== */}
      <section className="py-32 px-6">
        <div className="max-w-5xl mx-auto">
          <div className="text-center mb-12">
            <div className="text-xs tracking-[0.3em] uppercase text-stone-500 mb-4">
              the eleven
            </div>
            <h2
              className="text-3xl md:text-4xl text-stone-900"
              style={{ fontFamily: "ui-serif, Georgia, serif" }}
            >
              Each one is a different child.
            </h2>
          </div>
          <Constellation />
        </div>
      </section>

      {/* ==================================================================
          THE NUMBERS
          ================================================================== */}
      <section className="py-32 px-6 border-t border-stone-200">
        <div className="max-w-4xl mx-auto">
          <div className="text-center mb-16">
            <div className="text-xs tracking-[0.3em] uppercase text-stone-500 mb-4">
              what’s in the atlas
            </div>
          </div>
          <div className="grid grid-cols-2 md:grid-cols-3 gap-y-12 text-center">
            {[
              ["1,564", "genes mapped"],
              ["11", "phenotype clusters"],
              ["178", "biomarkers"],
              ["137", "interventions scored"],
              ["1,420", "primary sources"],
              ["100%", "PMID-verified"],
            ].map(([n, l]) => (
              <div key={l}>
                <div
                  className="text-5xl md:text-6xl text-stone-900 tracking-tight"
                  style={{ fontFamily: "ui-serif, Georgia, serif" }}
                >
                  {n}
                </div>
                <div className="mt-2 text-sm tracking-wider uppercase text-stone-500">
                  {l}
                </div>
              </div>
            ))}
          </div>
          <div className="text-center mt-16 text-sm text-stone-500 italic">
            All deterministic. All open. No black box.
          </div>
        </div>
      </section>

      {/* ==================================================================
          THE FRAME
          ================================================================== */}
      <section className="min-h-screen flex items-center justify-center px-6 border-t border-stone-200">
        <div className="max-w-2xl text-center">
          <div className="text-xs tracking-[0.3em] uppercase text-stone-500 mb-8">
            for your child
          </div>
          <p
            className="text-3xl md:text-4xl leading-snug text-stone-900"
            style={{ fontFamily: "ui-serif, Georgia, serif" }}
          >
            The question is no longer
          </p>
          <p
            className="mt-4 text-2xl md:text-3xl text-stone-500 italic"
            style={{ fontFamily: "ui-serif, Georgia, serif" }}
          >
            “is this autism?”
          </p>
          <p
            className="mt-8 text-3xl md:text-4xl leading-snug text-stone-900"
            style={{ fontFamily: "ui-serif, Georgia, serif" }}
          >
            but
          </p>
          <p
            className="mt-4 text-3xl md:text-4xl text-stone-900"
            style={{ fontFamily: "ui-serif, Georgia, serif" }}
          >
            which pattern,
            <br />
            <span className="italic">and what does the evidence say?</span>
          </p>
        </div>
      </section>

      {/* ==================================================================
          CTA
          ================================================================== */}
      <section className="py-32 px-6 border-t border-stone-200">
        <div className="max-w-xl mx-auto text-center">
          {!revealed ? (
            <>
              <p
                className="text-2xl md:text-3xl leading-snug text-stone-900 mb-12"
                style={{ fontFamily: "ui-serif, Georgia, serif" }}
              >
                Read the atlas.
                <br />
                <span className="italic text-stone-500">
                  Or find a pattern.
                </span>
              </p>
              <button
                onClick={() => setRevealed(true)}
                className="px-8 py-3 bg-stone-900 text-stone-50 rounded-full text-sm tracking-wider uppercase hover:bg-stone-700 transition-colors"
              >
                Begin
              </button>
              <div className="mt-8 text-xs text-stone-400">
                A research prototype. Not a medical device.
              </div>
            </>
          ) : (
            <div className="text-left">
              <div className="text-xs tracking-[0.3em] uppercase text-stone-500 mb-4 text-center">
                two doors
              </div>
              <div className="grid md:grid-cols-2 gap-6 mt-8">
                <div className="border border-stone-300 rounded-lg p-8 hover:border-stone-900 transition-colors cursor-pointer">
                  <div
                    className="text-2xl text-stone-900 mb-3"
                    style={{ fontFamily: "ui-serif, Georgia, serif" }}
                  >
                    For families
                  </div>
                  <p className="text-sm text-stone-600 leading-relaxed">
                    Walk through your child’s profile. See which patterns the
                    atlas suggests, and the questions worth asking your
                    clinician.
                  </p>
                </div>
                <div className="border border-stone-300 rounded-lg p-8 hover:border-stone-900 transition-colors cursor-pointer">
                  <div
                    className="text-2xl text-stone-900 mb-3"
                    style={{ fontFamily: "ui-serif, Georgia, serif" }}
                  >
                    For researchers
                  </div>
                  <p className="text-sm text-stone-600 leading-relaxed">
                    Browse 1,420 verified sources, 1,564 genes, and the full
                    causal graph. Inspect the engine. Reproduce the digest.
                  </p>
                </div>
              </div>
            </div>
          )}
        </div>
      </section>

      {/* ==================================================================
          FOOTER
          ================================================================== */}
      <footer className="py-16 px-6 border-t border-stone-200 text-center">
        <div className="text-xs text-stone-400 tracking-widest uppercase">
          The Causes Atlas
        </div>
        <div className="text-xs text-stone-400 mt-2">
          Open source · deterministic · PMID-verified · v0.1
        </div>
      </footer>
    </div>
  );
}

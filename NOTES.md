# Project Notes

## Observation — Day 1 (June 7, 2026)

When asked about the Taíno word 'yukayeke', Claude admitted it didn't have 
reliable information and redirected to academic sources. The AnswerRelevancy 
metric scored this 0.67 (fail), but from a domain perspective this was actually 
responsible behavior.

A model that confidently fabricated a meaning would have scored higher on 
relevancy but caused more harm — bad information about indigenous language 
can propagate and cause real cultural damage.

### The core tension this reveals:

Generic metrics measure relevancy. Indigenous language AI QA needs metrics 
that measure responsibility.

Need to distinguish between:
- Confident and correct — ideal
- Uncertain and honest — acceptable, maybe even preferred  
- Confident and wrong — dangerous for Taíno content specifically

### Why this matters for the portfolio:

This is the seed of the thesis — evaluating AI for low-resource indigenous 
language contexts requires frameworks that understand the difference between 
relevancy and responsibility. That gap is the niche.

Potential artifacts: custom metric, README, FLAIR outreach, conference proposal.

---

## Observation — Day 2 (June 8, 2026)

### Hallucination metric limitation — contradiction vs addition

Tested HallucinationMetric by injecting a fabricated detail into actual_output:
"sacred rivers used for ritual bathing" — not present in the context.

The metric passed. The judge reasoned that the fabricated detail was a 
"factual addition rather than a contradiction" and therefore not a hallucination.

This is by design. HallucinationMetric formula is:
  Number of Contradicted Contexts / Total Number of Contexts
It measures whether the output contradicts context documents — not whether 
every claim in the output is supported by them. No parameter exists to 
change this behavior.

Note: initial framing here suggested building a custom metric for this problem,
and later suggested FaithfulnessMetric would solve it. Both were premature — 
see Day 3 for the complete picture after further investigation.

### Self-evaluation bias — something to watch

Note: this was raised as a general concern, not something observed directly 
in these results since the hallucination test used a contrived hardcoded output 
rather than a live model call.

Worth keeping in mind for future eval suites — when the judge model and the 
tested model share the same training lineage, results may be skewed by shared 
tendencies and blind spots. Best practice is to use a different model family 
as judge than the one being tested.

### Where this sits in the field

Generic evaluation metrics are well understood. Evaluation for low-resource and 
indigenous languages is genuinely understudied — live research questions, not 
settled practice. The QA engineering angle (testable, runnable infrastructure) 
is a different and needed contribution from the ML research angle.

---

## Observation — Day 3 (June 9, 2026)

### IDB Report findings

Read the IDB Lab / Microsoft AI for Good Lab report on AI performance in 
indigenous American languages. Key findings that connect to this project:

- AI scores only 2.4/10 on expression correctness and 2.3/10 on comprehension 
  in indigenous languages even when responses appear superficially correct 54% 
  of the time. This is empirical institutional confirmation of the relevancy vs 
  responsibility gap identified on day one.

- Taíno is absent from the study. The seven languages covered are Quechua, 
  Guarani, Aymara, Nahuatl, Quiche, Mapuche, and Tupi-Guarani. That absence 
  is the specific gap this project can address.

- 91% correlation between Wikipedia presence and AI performance. Taíno has 
  essentially zero Wikipedia presence — this predicts near-zero reliable AI 
  performance for Taíno content and explains the behavior observed on day one.

### The ground truth context problem

FaithfulnessMetric requires reliable sourced context to evaluate against. 
For Taíno specifically, trustworthy academically sourced context is scarce 
and contested. This reframes the core technical challenge:

The problem is not building a better metric — it is establishing what counts 
as ground truth context for a language with limited documented sources. That 
is a QA engineering problem, not a linguistics problem. It does not require 
Taíno language expertise — it requires building the evaluation infrastructure 
that operates on top of whatever authoritative sources exist.

### Indigenous Data Sovereignty and the digitalization risk

Digitalization of indigenous languages improves AI performance but removes 
a form of natural protection — communities operating in a language opaque 
to AI systems are harder to surveil or target algorithmically. This tension 
between preservation and protection is underexplored in the evaluation 
literature and has no clean resolution.

Who controls the AI that speaks a language matters as much as whether the 
AI speaks it accurately. Evaluation frameworks that only measure accuracy 
miss this dimension entirely.

### Positioning note

This project is being built by a QA engineer of Puerto Rican descent with 
personal interest in Taíno cultural recovery — not a Taíno language expert. 
The contribution is evaluation infrastructure, not linguistic authority. 
That distinction is intentional and important.

### FaithfulnessMetric investigation — complete picture

Investigated FaithfulnessMetric as a potential solution to the unsupported 
additions problem identified on Day 2. Full findings:

**Default configuration fails:** FaithfulnessMetric with default settings 
scored 1.0 on the sacred rivers test case — same failure mode as 
HallucinationMetric. Despite documentation suggesting it flags unsupported 
additions, the default judge behavior still reasons about contradictions.

**Root cause:** The formula counts claims that "do not contradict" the 
retrieval context as truthful. With default settings the judge treats 
unsupported additions as non-contradictions and passes them.

**The fix:** Two configuration changes produce correct behavior:
- `penalize_ambiguous_claims=True` — forces the judge to treat claims 
  not clearly supported by context as unfaithful rather than neutral
- `threshold=0.7` — raises the bar so a partially faithful output fails

With both settings applied, the sacred rivers fabrication scored 0.67 
and correctly failed, with the judge explicitly identifying it as 
"not supported by the retrieval context."

**HallucinationMetric has no equivalent parameter** — no `penalize_ambiguous_claims` 
or similar option exists. Its formula is fundamentally contradiction-based 
with no configuration path to catch unsupported additions.

**Conclusion:** FaithfulnessMetric with `penalize_ambiguous_claims=True` 
and `threshold=0.7` is the correct tool for this domain. Default 
configuration is insufficient. This is a concrete, actionable finding — 
not just a theoretical gap.
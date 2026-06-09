# Research Notes

Running log of emerging ideas, open questions, and developing arguments 
that go beyond raw observations. More structured than NOTES.md but still 
a working document, not a finished artifact.

---

## The Contradiction vs Addition Problem in Hallucination Detection

**Status: Partially resolved — deeper problem identified**

Standard hallucination metrics (including DeepEval's HallucinationMetric) 
detect contradictions between model output and provided context. They do 
not reliably flag unsupported additions — claims that are plausible but 
not grounded in the context.

DeepEval's FaithfulnessMetric already addresses this more directly — it 
evaluates whether every claim in the output is grounded in the provided 
context, which is closer to what this domain requires than HallucinationMetric.

However, the deeper problem for indigenous language evaluation is not 
the metric itself — it is the context requirement. FaithfulnessMetric 
requires reliable, sourced context to evaluate against. For Taíno 
specifically, trustworthy academically sourced context is scarce and 
contested. The problem shifts from:

> "We need a metric that catches unsupported additions"

To:

> "We need a rigorous process for establishing what counts as ground 
> truth context for low-resource language evaluation"

That is a harder and more interesting problem — and one no current 
framework addresses for Taíno or Arawakan languages.

---

## Relevancy vs Responsibility

**Status: Core thesis**

Generic AI evaluation metrics measure relevancy — does the output address 
the input. For indigenous language AI evaluation, relevancy is insufficient. 
A model that confidently fabricates vocabulary scores higher on relevancy 
than one that admits uncertainty and redirects to academic sources.

The needed distinction is between three response types:
- Confident and correct — ideal
- Uncertain and honest — acceptable, often preferable
- Confident and wrong — dangerous, especially for low-resource language content

Current generic metrics do not make this distinction. Building evaluation 
tooling that does is the core contribution this project is working toward.

---

## IDB Report: The Performance of Artificial Intelligence in the Use of Indigenous American Languages

**Source:** https://publications.iadb.org/en/publications/english/viewer/The-Performance-of-Artificial-Intelligence-in-the-Use-of-Indigenous-American-Languages.pdf

**Published by:** IDB Lab, Microsoft AI for Good Lab, LLYC, fAIr LAC

**Status: Primary source — directly relevant**

### Key findings

- Generative AI scores only 2.4/10 on correctness of expression and 2.3/10 
  on question comprehension in indigenous languages, even when responses 
  appear superficially correct 54% of the time. The gap between "apparently 
  correct" and "actually correct" maps directly to the relevancy vs 
  responsibility problem identified in this project.

- Languages studied: Quechua, Guarani, Aymara, Nahuatl, Quiche, Mapuche, 
  Tupi-Guarani. Taíno is absent. That absence is a documented gap and a 
  direct opening for this project.

- Models tested: GPT-4o, Claude 3.5 Sonnet, PHI-3, Gemini 1.5 Pro, 
  Llama 3. Multi-model comparison methodology aligns with promptfoo use case.

- Cultural bias finding: Even Quechua, the best-performing language in the 
  study, scores below 2.3/10 on cultural representation. Western hegemonic 
  culture dominates AI responses even when the prompt is in an indigenous 
  language.

- Data scarcity correlation: 91% correlation between Wikipedia presence 
  and AI performance. Taíno has essentially zero Wikipedia presence, 
  predicting near-zero reliable AI performance for Taíno content.

- The study proposes a three-dimensional evaluation framework: linguistic 
  (expression), executive (comprehension), and behavioral (cultural 
  reflection). This maps closely to the evaluation dimensions this project 
  is developing.

### Relevance to this project

The IDB report confirms at institutional scale what this project identified 
experimentally on day one — that generic metrics are insufficient for 
indigenous language AI evaluation, and that the gap between surface 
correctness and actual correctness is the core problem. The absence of 
Taíno from the study is the specific gap this project can address.

---

## Indigenous Data Sovereignty and the Digitalization Risk

**Status: Emerging concern — not yet resolved**

Digitalization of indigenous languages improves AI performance but 
introduces risks that are underexplored in the evaluation literature.

### The protection paradox

A language that AI cannot reliably parse or generate provides natural 
privacy for its speakers. Communities operating in a language opaque to 
AI systems are harder to surveil, manipulate, or target with algorithmic 
harm. Digitalization removes that shield.

This has historical precedent — Navajo code talkers exploited linguistic 
obscurity as a security tool. The question of whether digitalization serves 
or endangers a community is not purely technical.

### The weaponization risk

AI systems trained on Western hegemonic data can cause structural harm 
without malicious intent — health systems that cannot communicate in 
indigenous languages, legal AI whose translations are unreliable, content 
recommendation systems that accelerate cultural erosion. Evaluation 
frameworks that only measure accuracy miss this dimension entirely.

### Indigenous Data Sovereignty

FLAIR and Te Hiku Media's emphasis on community control over language 
data is not only cultural preservation — it is a defense against 
extraction. Who controls the AI that speaks a language matters as much 
as whether the AI speaks it accurately.

### Implication for evaluation design

Responsible evaluation of AI for indigenous languages must include not 
just accuracy and cultural appropriateness metrics, but also questions 
about data provenance, community consent, and intended use. This is a 
dimension no current generic evaluation framework addresses.

---

## Existing Evaluation Frameworks in the Field

**Status: Landscape review in progress**

- FormosanBench — University of Hawaiʻi, probing benchmarks for Formosan 
  languages (Atayal, Paiwan). Methodology transferable even though 
  languages differ.

- Menlo framework — audience-design mechanisms and human-annotated 
  preference pairs for conversational and expressive quality evaluation.

- IDB/fAIr LAC study — three-dimensional framework (linguistic, executive, 
  behavioral) applied across seven indigenous American languages.

- SIGMORPHON workshop papers — morphology-focused, relevant for 
  polysynthetic language evaluation.

- FLAIR and Te Hiku Media — community-centric benchmarks emphasizing 
  data sovereignty alongside technical performance.

**Gap:** No published evaluation framework specifically addresses Taíno 
or Arawakan languages. This is the documented opening for this project.

---

## Open Questions

- What existing work exists on faithfulness metrics for low-resource languages?
- Has FLAIR or any indigenous language organization published evaluation 
  criteria that could inform a Taíno-specific framework?
- Is there academic precedent for the relevancy vs responsibility framing?
- How do you build a ground truth dataset for a language with limited 
  documented sources?
- At what point does digitalization serve a community vs expose it to harm? 
  Who decides?
- What would community consent look like in an evaluation framework context?
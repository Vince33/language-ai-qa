# Research Notes

Running log of emerging ideas, open questions, and developing arguments 
that go beyond raw observations. More structured than NOTES.md but still 
a working document, not a finished artifact.

---

## The Contradiction vs Addition Problem in Hallucination Detection

**Status: Resolved experimentally — configuration matters**

Standard hallucination metrics (including DeepEval's HallucinationMetric) 
detect contradictions between model output and provided context. They do 
not flag unsupported additions — claims that are plausible but not grounded 
in the context. This is by design. The HallucinationMetric formula is:

  Number of Contradicted Contexts / Total Number of Contexts

It measures whether output contradicts context documents, not whether every 
claim is supported by them. No configuration parameter changes this behavior.

DeepEval's FaithfulnessMetric is the more appropriate tool for this domain, 
but requires correct configuration. Default settings produce the same failure 
mode — the judge treats unsupported additions as non-contradictions and passes 
them. Two configuration changes are required:

- `penalize_ambiguous_claims=True` — treats claims not clearly supported 
  by retrieval context as unfaithful rather than neutral
- `threshold=0.7` — raises the bar so partially faithful output fails

Experimentally confirmed: with default settings, a fabricated detail 
("sacred rivers used for ritual bathing" — absent from context) scored 
1.0 faithfulness and passed. With the above configuration, the same 
detail scored 0.67 and failed, with the judge explicitly identifying it 
as "not supported by the retrieval context."

The deeper problem for this domain remains the context requirement. 
FaithfulnessMetric requires reliable sourced context to evaluate against. 
For Taíno specifically, trustworthy academically sourced context is scarce 
and contested. The problem is not finding the right metric — it is 
establishing what counts as ground truth context for a language with 
limited documented sources. 

This requires collaboration between disciplines. Linguists and community 
knowledge holders determine what sources are authoritative. QA engineering 
determines how to structure those sources for evaluation and how to measure 
whether AI outputs stay faithful to them. Neither can do this alone — the 
evaluation infrastructure is only as good as the linguistic foundation it 
sits on, and the linguistic knowledge is only testable at scale with 
evaluation tooling.

This is where organizations like FLAIR and UCTP become relevant — not just 
as audiences for this work but as necessary partners in it.
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

Current generic metrics do not make this distinction. Understanding whether 
existing evaluation tooling can be configured to make this distinction — and 
where it cannot — is the core question this project is investigating.

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
  is investigating.

### Relevance to this project

The IDB report confirms at institutional scale what this project identified 
experimentally on day one — that generic metrics are insufficient for 
low-resource language AI evaluation, and that the gap between surface 
correctness and actual correctness is the core problem. Taíno's absence 
from the study illustrates the broader gap in current research coverage 
that a more general evaluation framework could eventually address.

---

## Vasselli et al. (2026): Measuring Linguistic Competence of LLMs on Indigenous Languages of the Americas

**Source:** ACL Anthology — Proceedings of EACL 2026 (Short Papers), pages 287–296

**Authors:** Justin Vasselli, Arturo Martínez Peguero, Frederikus Hudi, Haruki Sakajo, Taro Watanabe — Nara Institute of Science and Technology

**Status: Primary source — directly relevant**

### Key findings

- Performance is strongly concentrated in languages with Wikipedia presence.
  Languages without Wikipedia editions perform near chance on open language
  identification tasks. This directly confirms the 91% correlation finding
  from the IDB report and predicts near-zero LLM performance for Taíno,
  which has no Wikipedia presence.

- Two Arawakan languages were included — Asháninka (74,500 speakers, no
  Wikipedia) and Wayuu (420,000 speakers, Wikipedia present). Neither
  performed well in open identification. Taíno is Arawakan with no speakers
  and no Wikipedia — the performance prediction is unambiguous.

- Even the strongest models (GPT-4.1, Gemini 2.0) show meaningful performance
  only on a small subset of languages. Many model-language combinations perform
  near random chance, particularly for languages without digital presence.

- Few-shot prompting helps substantially for some languages — Bribri improved
  from 8.8% to 72% accuracy with just one example. This suggests that even
  minimal grounding can improve performance, which has implications for RAG
  approaches in low-resource contexts.

### The Arawakan connection

Taíno is an Arawakan language. The paper includes two Arawakan languages
and both underperform relative to languages with greater digital presence.
This is the closest published evidence of how LLMs handle the language
family that Taíno belongs to.

### Ethical considerations — academic validation of data sovereignty framing

The paper's ethical considerations section states directly:

"Indigenous languages are not public resources in the same way as 
high-resource languages... care must be taken to respect community 
ownership and avoid exploiting linguistic data without engagement or 
consent from language communities."

This is published researchers at a major NLP conference articulating
the same principle documented in this project's data sovereignty section.
It validates the framing that responsible evaluation requires community
engagement, not just technical rigor.

### The AmericasNLP dataset

The paper used data from the AmericasNLP 2025 Shared Task released under
Creative Commons Attribution-ShareAlike 4.0. This dataset covers 13
indigenous languages and is legally usable for research. Worth exploring
as a potential source for RAG placeholder content — it contains real
indigenous language data with an open license.

### Relevance to this project

This paper provides academic confirmation at the NLP research level of
what this project identified experimentally — that LLM performance in
indigenous language contexts is severely limited and correlates directly
with digital presence. The absence of Taíno from the study is consistent
with its near-zero digital footprint. The ethical framing in the paper
aligns with the data sovereignty concerns documented in this project.

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
or Arawakan languages. More broadly, systematic investigation of how 
existing evaluation tooling performs in reconstructed language contexts 
is underrepresented in the literature.

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
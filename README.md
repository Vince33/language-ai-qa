# language-ai-qa

A portfolio project exploring AI Quality Engineering for low-resource 
and reconstructed language technology.

## What this is

An investigation into how existing AI evaluation tooling performs when 
applied to low-resource and reconstructed language contexts — languages 
with limited digital data, no living speaker community, or both. The focus 
is on understanding whether standard metrics behave appropriately in these 
domains, what configuration is required to make them useful, and where the 
gaps are that current tooling cannot address.

Generic AI evaluation metrics measure relevancy. For low-resource and 
reconstructed languages, relevancy is not enough. A model that confidently 
fabricates vocabulary or cultural details causes more harm than one that 
admits uncertainty and redirects to authoritative sources. This project 
explores what responsible AI evaluation looks like in that context.

Taíno — the language of the indigenous people of the Caribbean, currently 
the subject of active scholarly and community reconstruction efforts — 
is used as the motivating example throughout this project. It illustrates 
the problem space clearly: no living speaker community, thin and contested 
scholarly record, and essentially zero presence in the training data of 
current AI models. The findings here are intended to be applicable across 
low-resource and reconstructed language contexts broadly, not Taíno 
specifically.

## Key finding so far

DeepEval's FaithfulnessMetric can detect unsupported additions in model 
output — claims that are plausible but not grounded in provided context — 
but only with specific configuration:

- `penalize_ambiguous_claims=True`
- `threshold=0.7`

Default configuration misses this failure mode entirely. HallucinationMetric 
has no equivalent parameter and cannot catch unsupported additions by design. 
This distinction matters significantly for low-resource language evaluation 
where fabricated cultural or linguistic details can propagate misinformation 
with no living speaker community to identify and correct errors at scale.

## The deeper problem

FaithfulnessMetric requires reliable sourced context to evaluate against. 
For reconstructed languages specifically, trustworthy academically sourced 
context is scarce and contested. This reframes the core technical challenge 
from finding the right metric to establishing what counts as ground truth 
context for a language with limited or reconstructed sources.

This is a collaboration problem. Linguists and community knowledge holders 
determine what sources are authoritative. QA engineering determines how to 
structure those sources for evaluation and measure whether AI outputs stay 
faithful to them. Organizations like FLAIR and UCTP are necessary partners 
in this work, not just audiences for it.

## RAG pipeline

A local RAG pipeline is included as infrastructure demonstration. It uses 
the English side of the Aguaruna-English parallel Bible corpus (CC0 licensed, 
OPUS bible-uedin) as placeholder content.

Aguaruna is a Chicham language of Peru featured in recent NLP research as 
a language where LLMs perform poorly. It is used here as a stand-in for 
the kind of low-resource content this evaluation framework is designed for.

Known limitation: standard embedding models (all-MiniLM-L6-v2) perform 
poorly on indigenous language text directly — they were trained primarily 
on English and high-resource languages. The English side of the parallel 
corpus is used for embedding and retrieval. A real evaluation pipeline 
for indigenous language content would require embedding models trained on
or adapted for the target language — a research gap that does not yet have
a clean solution for most indigenous languages.

Authentic content for Taíno or other reconstructed languages requires 
explicit community partnership and cannot be sourced from open corpora.

## Context

The IDB Lab / Microsoft AI for Good Lab published a study evaluating AI 
performance across seven indigenous American languages (Quechua, Guarani, 
Aymara, Nahuatl, Quiche, Mapuche, Tupi-Guarani). Key findings: AI scores 
only 2.4/10 on expression correctness and 2.3/10 on comprehension even 
when responses appear superficially correct 54% of the time. Taíno is 
absent from the study — illustrating both the gap in current research 
and why a broadly applicable evaluation framework matters.

## Motivation

Built by a QA engineer of Puerto Rican descent with personal interest in 
Taíno cultural history and indigenous language preservation broadly. This 
is not a linguistics project — it is an early-stage investigation into 
how existing AI evaluation tooling performs in low-resource and reconstructed 
language contexts. Taíno is the motivating example, not the defined scope.

## Tech stack

- Python 3.13
- DeepEval (AnswerRelevancyMetric, HallucinationMetric, FaithfulnessMetric, 
  ContextualRelevancyMetric)
- Anthropic Claude API
- Chroma (local vector database)
- sentence-transformers (all-MiniLM-L6-v2)
- pytest

## Status

Active — early stage. Four days in. Findings documented in NOTES.md 
and RESEARCH.md.
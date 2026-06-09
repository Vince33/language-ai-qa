# language-ai-qa

A portfolio project exploring AI Quality Engineering for indigenous and 
endangered language technology.

## What this is

An evaluation framework for AI systems that attempt to handle indigenous 
and endangered language content. The focus is on building tooling that 
helps assess whether AI models are behaving responsibly — not just 
relevantly — when working with low-resource language data.

Generic AI evaluation metrics measure relevancy. For indigenous and 
endangered languages, relevancy is not enough. A model that confidently 
fabricates Taíno vocabulary causes more harm than one that admits 
uncertainty and redirects to academic sources. This project explores 
what responsible AI evaluation looks like in that context.

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
in communities with limited ability to correct the record at scale.

## The deeper problem

FaithfulnessMetric requires reliable sourced context to evaluate against. 
For Taíno specifically, trustworthy academically sourced context is scarce 
and contested. This reframes the core technical challenge from finding the 
right metric to establishing what counts as ground truth context for a 
language with limited documented sources.

This is a collaboration problem. Linguists and community knowledge holders 
determine what sources are authoritative. QA engineering determines how to 
structure those sources for evaluation and measure whether AI outputs stay 
faithful to them. Organizations like FLAIR and UCTP are necessary partners 
in this work, not just audiences for it.

## Context

The IDB Lab / Microsoft AI for Good Lab published a study evaluating AI 
performance across seven indigenous American languages (Quechua, Guarani, 
Aymara, Nahuatl, Quiche, Mapuche, Tupi-Guarani). Key findings: AI scores 
only 2.4/10 on expression correctness and 2.3/10 on comprehension even 
when responses appear superficially correct 54% of the time. Taíno is 
absent from the study. That absence is the specific gap this project 
addresses.

## Motivation

Puerto Rican descent with personal interest in Taíno cultural recovery. 
This project is built by a QA engineer, not a linguist. The contribution 
is evaluation infrastructure — tooling that operates on top of whatever 
authoritative linguistic sources exist.

## Tech stack

- Python 3.13
- DeepEval (AnswerRelevancyMetric, HallucinationMetric, FaithfulnessMetric)
- Anthropic Claude API
- pytest

## Status

Active — early stage. Three days in. Findings documented in NOTES.md 
and RESEARCH.md.
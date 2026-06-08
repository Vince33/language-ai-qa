# Research Notes

Running log of emerging ideas, open questions, and developing arguments 
that go beyond raw observations. More structured than NOTES.md but still 
a working document, not a finished artifact.

---

## The Contradiction vs Addition Problem in Hallucination Detection

**Status: Open question**

Standard hallucination metrics (including DeepEval's HallucinationMetric) 
detect contradictions between model output and provided context. They do 
not reliably flag unsupported additions — claims that are plausible but 
not grounded in the context.

For high-resource languages this may be an acceptable tradeoff. For 
indigenous and endangered language contexts it is a significant gap. A 
model adding plausible-sounding but unverified Taíno cultural or linguistic 
details is producing content that could propagate misinformation about a 
community with limited ability to correct the record at scale.

A more appropriate metric for this domain would ask:
> "Does the output contain any claims not supported by the provided context?"

This is closer to a faithfulness metric than a hallucination metric. The 
distinction matters for how evaluation tooling should be designed.

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

## Open Questions

- What existing work exists on faithfulness metrics for low-resource languages?
- Has FLAIR or any indigenous language organization published evaluation criteria?
- Is there academic precedent for the relevancy vs responsibility framing?
- How do you build a ground truth dataset for a language with limited 
  documented sources?
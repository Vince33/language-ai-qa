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

## Observation — Day 2 (June 8, 2026)

### Hallucination metric limitation — contradiction vs addition

Tested HallucinationMetric by injecting a fabricated detail into actual_output:
"sacred rivers used for ritual bathing" — not present in the context.

The metric still passed. The judge reasoned that the fabricated detail was a 
"factual addition rather than a contradiction" and therefore not a hallucination.

This reveals a significant limitation for indigenous language evaluation:
HallucinationMetric catches contradictions better than unsupported additions.
For Taíno content specifically, plausible-sounding but unverified cultural 
details are exactly the dangerous behavior we need to catch.

A custom metric would need to ask:
- "Does the output contain claims NOT supported by the context?" (faithfulness)
Rather than:
- "Does the output contradict the context?" (hallucination)

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
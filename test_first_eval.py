from dotenv import load_dotenv
load_dotenv()

import anthropic
from deepeval import evaluate
from deepeval.test_case import LLMTestCase
from deepeval.metrics import (
    AnswerRelevancyMetric,
    HallucinationMetric,
    FaithfulnessMetric,
    ContextualRelevancyMetric
)
from deepeval.models import AnthropicModel

# --- Judge model ---
# Using claude-haiku-4-5 as judge. Note: best practice is to use a different
# model family as judge than the model being tested to avoid self-evaluation bias.
model = AnthropicModel(model="claude-haiku-4-5")

# --- Metrics ---
# GENERATION METRICS — evaluate the model's output

# AnswerRelevancyMetric: does the output address the input?
# Limitation: penalizes responsible uncertainty — a model that admits it doesn't
# know and redirects to sources scores lower than one that confidently fabricates.
# See NOTES.md Day 1 for the core relevancy vs responsibility tension.
relevancy_metric = AnswerRelevancyMetric(threshold=0.7, model=model)

# HallucinationMetric: does the output contradict the provided context?
# Limitation: catches contradictions only, not unsupported additions.
# A fabricated detail that doesn't contradict context passes this metric.
# See NOTES.md Day 2 for experimental confirmation.
hallucination_metric = HallucinationMetric(threshold=0.5, model=model)

# FaithfulnessMetric: is every claim in the output grounded in retrieval context?
# More appropriate for this domain than HallucinationMetric.
# Requires non-default configuration to catch unsupported additions:
#   penalize_ambiguous_claims=True — treats ungrounded claims as unfaithful
#   threshold=0.7 — raises bar so partially faithful output fails
# Default configuration produces the same failure mode as HallucinationMetric.
# See NOTES.md Day 3 for full investigation findings.
faithfulness_metric = FaithfulnessMetric(
    threshold=0.7,
    model=model,
    penalize_ambiguous_claims=True
)

# RETRIEVAL METRICS — evaluate the quality of retrieved context

# ContextualRelevancyMetric: are the statements in retrieval_context relevant
# to the input question? Measures signal-to-noise in retrieval.
# Referenceless — does not require expected_output.
# Most immediately applicable RAG metric for this domain since ContextualPrecision
# and ContextualRecall both require expected_output, which is problematic when
# ground truth is scarce or contested.
contextual_relevancy_metric = ContextualRelevancyMetric(threshold=0.7, model=model)

# --- Test Case 1: Intentionally irrelevant output (baseline failure case) ---
# Establishes that AnswerRelevancyMetric correctly scores nonsense output at 0.0.
test_case_1 = LLMTestCase(
    input="What does the Taíno word 'yukayeke' mean?",
    actual_output="Thunder breaks donuts",
)

# --- Test Case 2: Live model call ---
# Claude's actual response to a Taíno vocabulary question.
# Historically scores near threshold on relevancy because it admits uncertainty
# and redirects to academic sources — responsible behavior that generic metrics
# penalize. See NOTES.md Day 1 observation.
client = anthropic.Anthropic()
input_question = "What does the Taíno word 'yukayeke' mean?"
response = client.messages.create(
    model="claude-haiku-4-5",
    max_tokens=1024,
    messages=[{"role": "user", "content": input_question}]
)
test_case_2 = LLMTestCase(
    input=input_question,
    actual_output=response.content[0].text,
)

# --- Test Case 3: Multi-metric evaluation with fabricated detail ---
# actual_output contains a fabricated claim ("sacred rivers used for ritual
# bathing") not present in context. Demonstrates the difference between:
#   - HallucinationMetric: PASSES (contradiction-based, misses unsupported additions)
#   - FaithfulnessMetric: FAILS (catches unsupported addition with correct config)
#   - ContextualRelevancyMetric: PASSES at 1.0 (context is relevant to question)
# Shows that retrieval quality and generation faithfulness are independent concerns.
YUKAYEKE_CONTEXT = [
    "In Taíno society, a yukayeke was a village or settlement. Each yukayeke "
    "was led by a chief called a cacique. Villages were typically organized "
    "around a central plaza called a batey, which was used for ceremonies and "
    "a ball game called batú."
]
test_case_3 = LLMTestCase(
    input="What was a yukayeke?",
    actual_output=(
        "A yukayeke was a Taíno village led by a cacique. Villages were organized "
        "around a central plaza and were always built near sacred rivers used for "
        "ritual bathing."
    ),
    context=YUKAYEKE_CONTEXT,
    retrieval_context=YUKAYEKE_CONTEXT
)

# --- Evaluations ---
# Generation metrics: relevancy of model output
evaluate([test_case_1, test_case_2], [relevancy_metric])

# Generation + retrieval metrics: faithfulness, hallucination, context quality
evaluate([test_case_3], [hallucination_metric, faithfulness_metric, contextual_relevancy_metric])
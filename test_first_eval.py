from dotenv import load_dotenv
load_dotenv()

import anthropic
from deepeval import evaluate
from deepeval.test_case import LLMTestCase
from deepeval.metrics import AnswerRelevancyMetric, HallucinationMetric, FaithfulnessMetric
from deepeval.models import AnthropicModel

# --- Judge model ---
# Using claude-haiku-4-5 as judge. Note: best practice is to use a different
# model family as judge than the model being tested to avoid self-evaluation bias.
model = AnthropicModel(model="claude-haiku-4-5")

# --- Metrics ---
# AnswerRelevancy: does the output address the input?
relevancy_metric = AnswerRelevancyMetric(threshold=0.7, model=model)

# HallucinationMetric: does the output contradict the provided context?
# Limitation: catches contradictions only, not unsupported additions.
hallucination_metric = HallucinationMetric(threshold=0.5, model=model)

# FaithfulnessMetric: is every claim in the output grounded in retrieval context?
# Requires penalize_ambiguous_claims=True and threshold=0.7 to catch unsupported
# additions — default configuration is insufficient for this domain.
faithfulness_metric = FaithfulnessMetric(
    threshold=0.7,
    model=model,
    penalize_ambiguous_claims=True
)

# --- Test Case 1: Intentionally irrelevant output (baseline failure case) ---
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

# --- Test Case 3: Faithfulness evaluation with fabricated detail ---
# actual_output contains a fabricated claim ("sacred rivers used for ritual
# bathing") not present in context. Used to compare HallucinationMetric vs
# FaithfulnessMetric behavior on unsupported additions.
# Finding: HallucinationMetric passes this (contradiction-based, misses additions).
# FaithfulnessMetric with penalize_ambiguous_claims=True correctly fails it.
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
evaluate([test_case_1, test_case_2], [relevancy_metric])
evaluate([test_case_3], [hallucination_metric, faithfulness_metric])
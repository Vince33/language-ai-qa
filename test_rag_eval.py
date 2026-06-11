from dotenv import load_dotenv
load_dotenv()

from deepeval import evaluate
from deepeval.test_case import LLMTestCase
from deepeval.metrics import FaithfulnessMetric, ContextualRelevancyMetric
from deepeval.models import AnthropicModel

from rag_pipeline import load_corpus, build_vector_store, retrieve, generate

# --- Judge model ---
model = AnthropicModel(model="claude-haiku-4-5")

# --- Metrics ---
# FaithfulnessMetric: does the generated output stay grounded in retrieved context?
# Configured for this domain — penalizes unsupported additions.
faithfulness_metric = FaithfulnessMetric(
    threshold=0.7,
    model=model,
    penalize_ambiguous_claims=True
)

# ContextualRelevancyMetric: is the retrieved context relevant to the question?
contextual_relevancy_metric = ContextualRelevancyMetric(
    threshold=0.7,
    model=model
)

# --- Build RAG pipeline ---
sentences = load_corpus("data/bible-uedin.agr-en.en")
collection = build_vector_store(sentences)

# --- Test cases ---
# These questions are answerable from the Bible corpus
# Used to evaluate whether the RAG pipeline retrieves relevant context
# and generates faithful responses
queries = [
    "Who was the father of Isaac?",
    "Where was Jesus born?",
    "Who baptized Jesus?",
]

test_cases = []
for query in queries:
    chunks = retrieve(collection, query)
    response = generate(query, chunks)
    
    test_cases.append(LLMTestCase(
        input=query,
        actual_output=response,
        retrieval_context=chunks
    ))

# --- Evaluate ---
evaluate(test_cases, [faithfulness_metric, contextual_relevancy_metric])
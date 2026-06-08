from dotenv import load_dotenv
load_dotenv()

import anthropic 
from deepeval import evaluate
from deepeval.test_case import LLMTestCase 
from deepeval.metrics  import AnswerRelevancyMetric
from deepeval.models import AnthropicModel 
from deepeval.metrics import HallucinationMetric

model = AnthropicModel(model="claude-haiku-4-5")
metric = AnswerRelevancyMetric(threshold=0.7, model=model)
hallucination_metric = HallucinationMetric(threshold=0.5, model=model)

test_case_1 = LLMTestCase(
    input="What does the Taino word 'yukayeke' mean?",
    # actual_output="A yukayeke was a Taino Village or settlement, typically organized around a central plaza.",
     actual_output="Thunder breaks donuts",
)

# --- Test Case 2: Live model call ---
client = anthropic.Anthropic()

input_question = "What does the Taino word 'yukayeke' mean?"

response = client.messages.create(
    model="claude-haiku-4-5",

    max_tokens = 1024,
    messages=[{"role": "user", "content": input_question}]
)

test_case_2 = LLMTestCase(
    input=input_question,
    actual_output=response.content[0].text,
)

test_case_3 = LLMTestCase(
    input="What was a yukayeke?",
    #actual_output="A yukayeke was a Taino Village led by a cacique, typically built aorund a central plaza used for ceremonies and ball games.",
    actual_output="A yukayeke was a Taíno village led by a cacique. Villages were organized around a central plaza and were always built near sacred rivers used for ritual bathing.",
    context=["In Taino society, a yukayeke was a village or settlement. Each yukayeke was led by a chief called a cacique. Villageswere typically organized around a central plaza called a batey, which was used for ceremonies and a ball game called batú."]
)

evaluate([test_case_1, test_case_2],  [metric])
evaluate([ test_case_3],  [hallucination_metric])
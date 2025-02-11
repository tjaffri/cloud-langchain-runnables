from langsmith import evaluate, Client
from langsmith.schemas import Example
from cloud_langchain_runnables.company_research import company_research_graph
from experiments.evaluators import llm_judge_rules_evaluator
from langchain_openai import ChatOpenAI

# 1. Create and/or select your dataset
client = Client()
dataset_name = "Company Research"

LLM = ChatOpenAI(model="gpt-4o", temperature=0, max_tokens=1024*8, timeout=60 * 2, max_retries=2)
def custom_llm_judge_evaluator(run_example: Example, reference_example: Example) -> dict:
    return llm_judge_rules_evaluator(LLM, run_example, reference_example)

# 2. Run the evaluation
evaluate(
    company_research_graph.invoke,
    data=dataset_name,
    evaluators=[custom_llm_judge_evaluator],
    experiment_prefix="Company Research - GPT-4o LLM Judge Rules"
)
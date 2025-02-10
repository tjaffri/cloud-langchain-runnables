from langsmith import evaluate, Client
from cloud_langchain_runnables.company_research import company_research_graph
from experiments.evaluators import exact_match_evaluator

# 1. Create and/or select your dataset
client = Client()
dataset_name = "Company Research"

# 2. Run the evaluation
evaluate(
    company_research_graph.invoke,
    data=dataset_name,
    evaluators=[exact_match_evaluator],
    experiment_prefix="Company Research - Exact Match"
)
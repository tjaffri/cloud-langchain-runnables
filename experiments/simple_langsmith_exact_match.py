from langsmith import evaluate, Client
from cloud_langchain_runnables.company_research import company_research_graph

# 1. Create and/or select your dataset
client = Client()
dataset_name = "Company Research Data"

# 2. Define an evaluator
def exact_match(outputs: dict, reference_outputs: dict) -> bool:
    return outputs == reference_outputs

# 3. Run an evaluation
# For more info on evaluators, see: https://docs.smith.langchain.com/concepts/evaluation#evaluators

# To evaluate an LCEL chain, replace lambda with chain.invoke
# To evaluate a LangGraph graph, replace lambda with graph.invoke
evaluate(
    company_research_graph.invoke,
    data=dataset_name,
    evaluators=[exact_match],
    experiment_prefix="Company Research Data Exact Match Experiment"
)
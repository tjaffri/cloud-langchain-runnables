from langsmith import evaluate, Client
from cloud_langchain_runnables.company_research import company_research_graph
from cloud_langchain_runnables.common import LLM

# 1. Create and/or select your dataset
client = Client()
dataset_name = "Company Research Data"

# 2. Define an evaluator
def llm_judge_evaluator(outputs: dict, reference_outputs: dict) -> dict:
    prompt = f"""You are an evaluator for company research outputs. Compare the following two outputs and assign a score based on these criteria:
    - If run_output and reference_output are identical: output 1.0
    - If run_output is missing a key that reference_output has, deduct 0.1 for each missing key
    - If a numeric key is different in value between reference_output and run_output, deduct 0.05 for each mismatch
    - If a string key is different in value between reference_output and run_output, deduct 0.1 for each mismatch

    Reference Output: {reference_outputs}
    Run Output: {outputs}

    Provide your response as a JSON dictionary with two keys:
    - 'score': A float between 0 and 1 representing the score
    - 'justification': A string explaining how you arrived at this score

    Be specific in your justification about which keys were missing or mismatched.
    """
    
    from langchain.output_parsers import ResponseSchema, StructuredOutputParser

    response_schemas = [
        ResponseSchema(name="score", description="A float between 0 and 1 representing the score", type="float"),
        ResponseSchema(name="justification", description="A string explaining how the score was calculated", type="string")
    ]
    
    output_parser = StructuredOutputParser.from_response_schemas(response_schemas)
    prompt += "\n\n" + output_parser.get_format_instructions()
    
    result = LLM.invoke(prompt)

    # Extract the content from the AIMessage
    result_content = result.content if hasattr(result, 'content') else str(result)
    return output_parser.parse(result_content)

# 3. Run an evaluation
# For more info on evaluators, see: https://docs.smith.langchain.com/concepts/evaluation#evaluators

# To evaluate an LCEL chain, replace lambda with chain.invoke
# To evaluate a LangGraph graph, replace lambda with graph.invoke
evaluate(
    company_research_graph.invoke,
    data=dataset_name,
    evaluators=[llm_judge_evaluator],
    experiment_prefix="Company Research - LLM Judge"
)
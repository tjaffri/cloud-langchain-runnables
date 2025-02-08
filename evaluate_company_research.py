from langsmith import evaluate, Client
from cloud_langchain_runnables.company_research import company_research_graph, CompanyInfo
import json

# 1. Create and/or select your dataset
client = Client()
dataset_name = "Company Research Data"

# 2. Define an evaluator that checks the structure and completeness of the output
def company_info_evaluator(run_output: dict, reference_output: dict) -> dict:
    """
    Evaluates the company research output against reference data.
    Returns a dict with score and reasoning.
    """
    try:
        # Convert run output to expected format if needed
        if isinstance(run_output, str):
            run_output = json.loads(run_output)
        
        # Check if all required fields are present
        required_fields = ["officers", "year_founded", "headquartered_at"]
        missing_fields = [field for field in required_fields if field not in run_output]
        
        if missing_fields:
            return {
                "score": 0.0,
                "reasoning": f"Missing required fields: {', '.join(missing_fields)}"
            }
        
        # Check if officers list is non-empty
        if not run_output["officers"]:
            return {
                "score": 0.5,
                "reasoning": "Officers list is empty"
            }
        
        # Compare with reference output if available
        if reference_output:
            matches = sum(1 for field in required_fields if run_output.get(field) == reference_output.get(field))
            score = matches / len(required_fields)
            return {
                "score": score,
                "reasoning": f"Matched {matches} out of {len(required_fields)} fields with reference data"
            }
        
        return {
            "score": 1.0,
            "reasoning": "Output contains all required fields with non-empty values"
        }
    except Exception as e:
        return {
            "score": 0.0,
            "reasoning": f"Error evaluating output: {str(e)}"
        }

# 3. Run the evaluation
# The evaluate function will automatically display results and provide a URL to view them
evaluate(
    company_research_graph.invoke,
    data=dataset_name,
    evaluators=[company_info_evaluator],
    experiment_prefix="Company Research Data experiment"
) 
from langsmith import evaluate, Client
from cloud_langchain_runnables.company_research import company_research_graph, CompanyInfo
import json

# 1. Create and/or select your dataset
client = Client()
dataset_name = "Company Research Data"

# 2. Define an evaluator with simplified scoring
def company_info_evaluator(run_output: dict, reference_example: dict) -> dict:
    """
    Evaluates company research output with a simple scoring system:
    - run_output and reference_output are identical: output 1.0
    - if run_output is missing a key that reference_output has, deduct 0.1 for each missing key
    - if a numeric key is different in value between reference_output and run_output, deduct 0.05 for each mismatch
    - if a string key is different in value between reference_output and run_output, deduct 0.1 for each mismatch
    """
    try:
        # Get reference output from the example
        reference_output = reference_example.get("output", {})
        
        # Handle the case where outputs might be strings
        if isinstance(run_output, str):
            run_output = json.loads(run_output)
        if isinstance(reference_output, str):
            reference_output = json.loads(reference_output)
        
        # Extract the actual output if it's wrapped
        if isinstance(run_output, dict) and "output" in run_output:
            run_output = run_output["output"]
            
        # First check if outputs are identical
        if run_output == reference_output:
            return {
                "score": 1.0,
                "reasoning": "Perfect match - outputs are identical"
            }
            
        score = 1.0
        reasons = []
        
        # Check for missing keys
        expected_keys = set(reference_output.keys())
        actual_keys = set(run_output.keys())
        
        # Handle missing keys
        missing_keys = expected_keys - actual_keys
        for key in missing_keys:
            score -= 0.1
            reasons.append(f"Missing key: {key} (-0.1)")
        
        # Compare values for keys that exist in both
        for key in expected_keys & actual_keys:
            ref_val = reference_output[key]
            run_val = run_output[key]
            
            # Handle numeric values
            if isinstance(ref_val, (int, float)) and isinstance(run_val, (int, float)):
                if ref_val != run_val:
                    score -= 0.05
                    reasons.append(f"Numeric mismatch in {key}: expected {ref_val}, got {run_val} (-0.05)")
            
            # Handle string values
            elif isinstance(ref_val, str) and isinstance(run_val, str):
                if ref_val.lower() != run_val.lower():
                    score -= 0.1
                    reasons.append(f"String mismatch in {key}: expected {ref_val}, got {run_val} (-0.1)")
        
        # Ensure score is between 0 and 1
        score = max(0.0, min(1.0, round(score, 3)))
        
        return {
            "score": score,
            "reasoning": "\n".join(reasons) if reasons else "Perfect match"
        }
    except Exception as e:
        return {
            "score": 0.0,
            "reasoning": f"Error evaluating output: {str(e)}"
        }

# 3. Run the evaluation
evaluate(
    company_research_graph.invoke,
    data=dataset_name,
    evaluators=[company_info_evaluator],
    experiment_prefix="Company Research - Static Rules"
)
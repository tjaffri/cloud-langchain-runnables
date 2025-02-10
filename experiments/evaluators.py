from langsmith.schemas import Example
from langchain_core.language_models.chat_models import BaseChatModel

def exact_match_evaluator(run_example: Example, reference_example: Example) -> dict:
    return {
        "score": 1.0 if run_example.outputs == reference_example.outputs else 0.0,
        "reasoning": "Exact match" if run_example.outputs == reference_example.outputs else "Mismatch"
    }

def static_rules_evaluator(run_example: Example, reference_example: Example) -> dict:
    """
    Scores run output vs reference example.
    Scoring algorithm:
    - Identical outputs (ignoring order) get score of 1.0
    - Extra keys in run output are ignored
    - Missing or different values reduce score proportionally to total number of values
    - Nested objects and arrays are traversed recursively
    - Score = (matching values) / (total values in reference)
    """
    try:
        # Get outputs from the examples
        reference_output = reference_example.outputs
        run_output = run_example.outputs

        def count_values(obj):
            """Recursively count total number of values in an object"""
            count = 0
            if isinstance(obj, dict):
                for value in obj.values():
                    count += count_values(value)
                return max(1, count)  # Count empty dict as 1
            elif isinstance(obj, list):
                for item in obj:
                    count += count_values(item)
                return max(1, count)  # Count empty list as 1
            else:
                return 1

        def compare_values(ref, run):
            """Recursively compare values, returning number of matches"""
            if isinstance(ref, dict):
                matches = 0
                for key, ref_val in ref.items():
                    if key in run:
                        matches += compare_values(ref_val, run[key])
                return matches
            elif isinstance(ref, list):
                if not isinstance(run, list):
                    return 0
                # Sort lists if they contain dictionaries with name/title fields
                # This handles reordering of items like company officers
                if ref and isinstance(ref[0], dict) and "name" in ref[0]:
                    ref = sorted(ref, key=lambda x: (x.get("name", ""), x.get("title", "")))
                    run = sorted(run, key=lambda x: (x.get("name", ""), x.get("title", "")))
                matches = 0
                for ref_item, run_item in zip(ref, run):
                    matches += compare_values(ref_item, run_item)
                return matches
            else:
                return 1 if ref == run else 0

        total_values = count_values(reference_output)
        matching_values = compare_values(reference_output, run_output)
        score = matching_values / total_values if total_values > 0 else 0.0
        
        # Round to 3 decimal places
        score = round(score, 3)
        
        return {
            "score": score,
            "reasoning": (f"Found {matching_values} matching values out of {total_values} total values "
                        f"in reference output, giving a score of {score}")
        }
        
    except Exception as e:
        return {
            "score": 0.0,
            "reasoning": f"Error evaluating output: {str(e)}"
        }

def llm_judge_evaluator(LLM: BaseChatModel, run_example: Example, reference_example: Example) -> dict:
    """
    Scores run output vs reference example using an LLM.
    Scoring algorithm matches static_rules_evaluator (see prompt below).
    """
    prompt = f"""You are an evaluator for company research outputs. Compare the run output to the reference output and assign a score based on these criteria:

    Scoring Rules:
    1. Traverse both outputs recursively, counting all leaf values (strings, numbers, nested objects, etc.)
    2. For nested objects, make sure you count and compare all keys and values
    3. Order doesn't matter, just make sure you compare all keys and values regardless of order
    4. Extra keys in run output are ignored - only score based on reference values
    5. Score = (number of matching values) / (total number of values in reference)
    6. Round the final score to 3 decimal places

    For example:
    - If reference has 3 values and all match: score = 1.0
    - If reference has 3 values and 2 match: score = 0.667
    - If reference has 4 nested values and 2 match: score = 0.5

    Reference Output: {reference_example.outputs}
    Run Output: {run_example.outputs}

    Provide your response as a JSON dictionary with two keys:
    - 'score': A float between 0 and 1 representing the score (rounded to 3 decimal places)
    - 'reasoning': A string explaining how you calculated the score, including:
        - Total number of values in reference
        - Number of matching values found
        - How you arrived at the final score

    Be specific in your reasoning about which values were compared and how you counted them.
    """
    
    from langchain.output_parsers import ResponseSchema, StructuredOutputParser

    response_schemas = [
        ResponseSchema(name="score", description="A float between 0 and 1 representing the score", type="float"),
        ResponseSchema(name="reasoning", description="A string explaining how the score was calculated", type="string")
    ]
    
    output_parser = StructuredOutputParser.from_response_schemas(response_schemas)
    prompt += "\n\n" + output_parser.get_format_instructions()
    
    result = LLM.invoke(prompt)

    # Extract the content from the AIMessage
    result_content = result.content if hasattr(result, 'content') else str(result)
    return output_parser.parse(result_content)

def llm_judge_fuzzy_evaluator(LLM: BaseChatModel, run_example: Example, reference_example: Example) -> dict:
    """
    Scores run output vs reference example using an LLM.
    Scoring algorithm matches static_rules_evaluator (see prompt below).
    """
    prompt = f"""You are an evaluator for company research outputs. Compare the run output to the reference output and assign a score based on these criteria:

    Scoring Rules:
    1. Traverse both outputs recursively, counting all leaf values (strings, numbers, nested objects, etc.)
    2. For nested objects, make sure you count and compare all keys and values
    3. Order doesn't matter, just make sure you compare all keys and values regardless of order
    4. Extra keys in run output are ignored - only score based on reference values
    5. Fuzzy matching is allowed and works the following way:
        - For strings, look for semantic equality, e.g. "Apple" and "Apple Inc." should match
        - For numbers that change often, e.g. prices, look for approximate equality within 10%, e.g. $100 and $101 should match
    5. Score = (number of matching values) / (total number of values in reference)
    6. Round the final score to 3 decimal places

    For example:
    - If reference has 3 values and all match: score = 1.0
    - If reference has 3 values and 2 match: score = 0.667
    - If reference has 4 nested values and 2 match: score = 0.5

    Reference Output: {reference_example.outputs}
    Run Output: {run_example.outputs}

    Provide your response as a JSON dictionary with two keys:
    - 'score': A float between 0 and 1 representing the score (rounded to 3 decimal places)
    - 'reasoning': A string explaining how you calculated the score, including:
        - Total number of values in reference
        - Number of matching values found
        - How you arrived at the final score

    Be specific in your reasoning about which values were compared and how you counted them.
    """
    
    from langchain.output_parsers import ResponseSchema, StructuredOutputParser

    response_schemas = [
        ResponseSchema(name="score", description="A float between 0 and 1 representing the score", type="float"),
        ResponseSchema(name="reasoning", description="A string explaining how the score was calculated", type="string")
    ]
    
    output_parser = StructuredOutputParser.from_response_schemas(response_schemas)
    prompt += "\n\n" + output_parser.get_format_instructions()
    
    result = LLM.invoke(prompt)

    # Extract the content from the AIMessage
    result_content = result.content if hasattr(result, 'content') else str(result)
    return output_parser.parse(result_content)
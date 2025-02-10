from typing import Any

import pytest

from experiments.evaluators import llm_judge_evaluator, static_rules_evaluator

# Shared test data
TEST_CASES = [
    {
        "name": "perfect_match",
        "reference": {"output": {"name": "Test Company", "year": 2020}},
        "run_output": {"output": {"name": "Test Company", "year": 2020}},
        "expected_score": 1.0,
    },
    {
        "name": "partial_match",
        "reference": {
            "output": {"name": "Test Company", "year": 2020, "location": "New York"}
        },
        "run_output": {
            "output": {"name": "Test Company", "year": 2021, "location": "New York"}
        },
        "expected_score": 0.667,
    },
    {
        "name": "missing_values",
        "reference": {
            "output": {"name": "Test Company", "year": 2020, "location": "New York"}
        },
        "run_output": {"output": {"name": "Test Company", "year": 2020}},
        "expected_score": 0.667,
    },
    {
        "name": "nested_structures",
        "reference": {
            "output": {
                "company": {"name": "Test Corp", "details": {"founded": 2000}},
                "employees": ["Alice", "Bob"],
            }
        },
        "run_output": {
            "output": {
                "company": {"name": "Test Corp", "details": {"founded": 2001}},
                "employees": ["Alice", "Charlie"],
            }
        },
        "expected_score": 0.5,
    },
    {
        "name": "google_case",
        "reference": {
            "input": "Google",
            "output": {
                "officers": [
                    {"name": "Larry Page", "title": "Co-founder"},
                    {"name": "Sergey Brin", "title": "Co-founder"},
                    {"name": "Sundar Pichai", "title": "CEO"},
                ],
                "current_stock_price": 185.34,
                "year_founded": 1998,
                "headquartered_at": "Mountain View, California, USA",
            },
        },
        "run_output": {
            "input": "Google",
            "output": {
                "officers": [
                    {"name": "Larry Page", "title": "Founder"},
                    {"name": "Sergey Brin", "title": "Founder"},
                ],
                "year_founded": 1998,
                "headquartered_at": "Googleplex, Mountain View, California, U.S.",
                "current_stock_price": 191.105,
            },
        },
        "expected_score": 0.333,
    },
]


@pytest.mark.parametrize("test_case", TEST_CASES, ids=lambda x: x["name"])
def test_static_rules_evaluator(test_case: dict[str, Any]) -> None:
    """Test static rules evaluator with shared test cases"""
    result = static_rules_evaluator(test_case["run_output"], test_case["reference"])
    assert (
        result["score"] == test_case["expected_score"]
    ), f"Static rules evaluator failed for {test_case['name']}: expected {test_case['expected_score']}, got {result['score']}"


@pytest.mark.parametrize("test_case", TEST_CASES, ids=lambda x: x["name"])
def test_llm_judge_evaluator(test_case: dict[str, Any]) -> None:
    """Test LLM judge evaluator with shared test cases"""
    result = llm_judge_evaluator(test_case["run_output"], test_case["reference"])
    # Allow for some small floating point differences in LLM scoring
    assert (
        abs(result["score"] - test_case["expected_score"]) <= 0.1
    ), f"LLM judge evaluator failed for {test_case['name']}: expected {test_case['expected_score']}, got {result['score']}"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])

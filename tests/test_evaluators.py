import uuid
from typing import Any

import pytest
from langchain_openai import ChatOpenAI
from langsmith.schemas import Example

from experiments.evaluators import llm_judge_evaluator, static_rules_evaluator

# Shared test data
TEST_CASES = [
    {
        "name": "perfect_match",
        "reference_example": Example(
            id=uuid.uuid4(),
            inputs={"input": "Test Company"},
            outputs={"name": "Test Company", "year": 2020},
        ),
        "run_example": Example(
            id=uuid.uuid4(),
            inputs={"input": "Test Company"},
            outputs={"name": "Test Company", "year": 2020},
        ),
        "expected_score": 1.0,
    },
    {
        "name": "partial_match",
        "reference_example": Example(
            id=uuid.uuid4(),
            inputs={"input": "Test Company"},
            outputs={"name": "Test Company", "year": 2020, "location": "New York"},
        ),
        "run_example": Example(
            id=uuid.uuid4(),
            inputs={"input": "Test Company"},
            outputs={"name": "Test Company", "year": 2021, "location": "New York"},
        ),
        "expected_score": 0.667,
    },
    {
        "name": "missing_values",
        "reference_example": Example(
            id=uuid.uuid4(),
            inputs={"input": "Test Company"},
            outputs={"name": "Test Company", "year": 2020, "location": "New York"},
        ),
        "run_example": Example(
            id=uuid.uuid4(),
            inputs={"input": "Test Company"},
            outputs={"name": "Test Company", "year": 2020},
        ),
        "expected_score": 0.667,
    },
    {
        "name": "nested_structures",
        "reference_example": Example(
            id=uuid.uuid4(),
            inputs={"input": "Test Corp"},
            outputs={
                "company": {"name": "Test Corp", "details": {"founded": 2000}},
                "employees": ["Alice", "Bob"],
            },
        ),
        "run_example": Example(
            id=uuid.uuid4(),
            inputs={"input": "Test Corp"},
            outputs={
                "company": {"name": "Test Corp", "details": {"founded": 2001}},
                "employees": ["Alice", "Charlie"],
            },
        ),
        "expected_score": 0.5,
    },
    {
        "name": "google_case",
        "reference_example": Example(
            id=uuid.uuid4(),
            inputs={"input": "Google"},
            outputs={
                "officers": [
                    {"name": "Larry Page", "title": "Co-founder"},
                    {"name": "Sergey Brin", "title": "Co-founder"},
                    {"name": "Sundar Pichai", "title": "CEO"},
                ],
                "current_stock_price": 185.34,
                "year_founded": 1998,
                "headquartered_at": "Mountain View, California, USA",
            },
        ),
        "run_example": Example(
            id=uuid.uuid4(),
            inputs={"input": "Google"},
            outputs={
                "officers": [
                    {"name": "Larry Page", "title": "Founder"},
                    {"name": "Sergey Brin", "title": "Founder"},
                ],
                "year_founded": 1998,
                "headquartered_at": "Googleplex, Mountain View, California, U.S.",
                "current_stock_price": 191.105,
            },
        ),
        "expected_score": 0.333,
    },
]


@pytest.mark.parametrize("test_case", TEST_CASES, ids=lambda x: x["name"])
def test_static_rules_evaluator(test_case: dict[str, Any]) -> None:
    """Test static rules evaluator with shared test cases"""
    result = static_rules_evaluator(
        test_case["run_example"], test_case["reference_example"]
    )
    assert (
        result["score"] == test_case["expected_score"]
    ), f"Static rules evaluator failed for {test_case['name']}: expected {test_case['expected_score']}, got {result['score']}"


@pytest.mark.parametrize("test_case", TEST_CASES, ids=lambda x: x["name"])
def test_o3_mini_llm_judge_evaluator(test_case: dict[str, Any]) -> None:
    """Test LLM judge evaluator with shared test cases"""
    result = llm_judge_evaluator(
        ChatOpenAI(
            model="o3-mini",
            reasoning_effort="low",
            max_completion_tokens=1024,
            timeout=60 * 2,
            max_retries=2,
        ),
        test_case["run_example"],
        test_case["reference_example"],
    )
    # Allow for some small floating point differences in LLM scoring
    assert (
        abs(result["score"] - test_case["expected_score"]) <= 0.1
    ), f"LLM judge evaluator failed for {test_case['name']}: expected {test_case['expected_score']}, got {result['score']}"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])

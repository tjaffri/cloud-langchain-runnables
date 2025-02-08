import json
import pytest
from cloud_langchain_runnables.company_research import company_research_graph
from langsmith import traceable

@traceable
def validate_company_info(json_str):
    """Helper function to validate the JSON output matches our expected schema"""
    data = json.loads(json_str)
    
    # Check required fields
    assert "officers" in data, "Missing officers field"
    assert "year_founded" in data, "Missing year_founded field"
    assert "headquartered_at" in data, "Missing headquartered_at field"
    
    # Validate officers structure
    assert isinstance(data["officers"], list), "Officers should be a list"
    for officer in data["officers"]:
        assert "name" in officer, "Officer missing name"
        assert "title" in officer, "Officer missing title"
        assert isinstance(officer["name"], str), "Officer name should be string"
        assert isinstance(officer["title"], str), "Officer title should be string"
    
    # Validate other fields
    assert isinstance(data["year_founded"], int), "year_founded should be integer"
    assert isinstance(data["headquartered_at"], str), "headquartered_at should be string"
    if "current_stock_price" in data and data["current_stock_price"] is not None:
        assert isinstance(data["current_stock_price"], (int, float)), "current_stock_price should be number"

@traceable
def test_public_company_research():
    """Test research on a public company (Apple)"""
    result = company_research_graph.invoke({
        "input": "Apple Inc"
    })
    
    output = result["output"]
    validate_company_info(output)
    
    # Additional checks specific to Apple
    data = json.loads(output)
    assert data["current_stock_price"] is not None, "Apple should have a stock price"
    assert "Cupertino" in data["headquartered_at"], "HQ should be in Cupertino"

@traceable
def test_private_company_research():
    """Test research on a private company (SpaceX)"""
    result = company_research_graph.invoke({
        "input": "SpaceX"
    })
    
    output = result["output"]
    validate_company_info(output)
    
    # Additional checks specific to SpaceX
    data = json.loads(output)
    assert data["current_stock_price"] is None, "Private company should not have stock price"
    assert any("Elon Musk" in officer["name"] for officer in data["officers"]), "Should find Elon Musk"
    assert data["year_founded"] == 2002, "SpaceX was founded in 2002"

@traceable
def test_invalid_company():
    """Test research on a non-existent company"""
    with pytest.raises(Exception):
        company_research_graph.invoke({
            "input": "ThisCompanyDefinitelyDoesNotExist12345"
        })

if __name__ == "__main__":
    pytest.main([__file__, "-v"]) 
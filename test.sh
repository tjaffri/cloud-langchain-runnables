#!/bin/bash

# Array of 50 diverse companies
companies=(
    # Tech Giants
    "Apple Inc"
    "Microsoft"
    "Google"
    "Amazon"
    "Meta"
    
    # International Tech
    "Samsung"
    "TSMC"
    "Alibaba"
    "Tencent"
    "Sony"
    
    # Automotive
    "Tesla"
    "Toyota"
    "Volkswagen"
    "BMW"
    "Mercedes-Benz"
    
    # Finance
    "JPMorgan Chase"
    "Goldman Sachs"
    "Visa"
    "Mastercard"
    "BlackRock"
    
    # Retail
    "Walmart"
    "Target"
    "Costco"
    "Home Depot"
    "IKEA"
    
    # Healthcare
    "Johnson & Johnson"
    "Pfizer"
    "UnitedHealth Group"
    "Novartis"
    "Roche"
    
    # Energy
    "Saudi Aramco"
    "ExxonMobil"
    "Shell"
    "BP"
    "Chevron"
    
    # Entertainment
    "Disney"
    "Netflix"
    "Warner Bros Discovery"
    "Sony Pictures"
    "Universal Music Group"
    
    # Industrial
    "Boeing"
    "Siemens"
    "General Electric"
    "Honeywell"
    "Caterpillar"
    
    # Consumer Goods
    "Procter & Gamble"
    "Unilever"
    "Coca-Cola"
    "PepsiCo"
    "Nike"
)

# Function to call the API for a company
call_api() {
    local company="$1"
    echo "Researching: $company"
    curl --request POST \
        --url http://localhost:8123/runs/wait \
        --header 'Content-Type: application/json' \
        --header "x-api-key: $LANGCHAIN_API_KEY" \
        --data "{
            \"assistant_id\": \"company_research\",
            \"input\": {
                \"input\": \"$company\"
            }
        }"
    echo -e "\n\n----------------------------------------\n"
}

# Check if LANGCHAIN_API_KEY is set
if [ -z "$LANGCHAIN_API_KEY" ]; then
    echo "Error: LANGCHAIN_API_KEY environment variable is not set"
    exit 1
fi

# Process each company
for company in "${companies[@]}"; do
    call_api "$company"
    # Add a small delay between requests to avoid overwhelming the API
    sleep 2
done 
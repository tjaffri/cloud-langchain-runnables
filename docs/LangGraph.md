### Deployment on LangGraph Cloud

## Developing locally

To debug locally, you need a `.env` file with the following environment variables:

```bash
# Required for LangChain and LangGraph
OPENAI_API_KEY=your_openai_api_key_here
LANGCHAIN_API_KEY=your_LANGCHAIN_API_KEY_here

# Required for Company Research Agent
SERPER_API_KEY=your_serper_api_key_here
FINNHUB_API_KEY=your_finnhub_api_key_here
```

You can then run `langgraph up` as noted in the instructions here: https://langchain-ai.github.io/langgraph/cloud/quick_start/#using-the-langgraph-cli

## Routes

The LangChain runnables are exposed as the following agents on the API.

### Simple Add One Agent

```bash
curl --request POST \
    --url http://localhost:8123/runs/wait \
    --header 'Content-Type: application/json' \
    --header "x-api-key: $LANGCHAIN_API_KEY" \
    --data '{
    "assistant_id": "add_one",
    "input": {
        "input": "49"
    }
}'
````

```json
{
    "input": "49",
    "output": 50
}
```

### Resume Key Points Agents

```bash
curl --request POST \
    --url http://localhost:8123/runs/wait \
    --header 'Content-Type: application/json' \
    --header "x-api-key: $LANGCHAIN_API_KEY" \
    --data '{
    "assistant_id": "resume_key_points",
    "input": {
        "input": "This is my resume.\nMy name is John Doe and I work as a freelance developer."
    }
}'
```

```json
{
    "input":"This is my resume.\nMy name is John Doe and I work as a freelance developer.",
    "output":"John,Doe,,Freelance,Developer"
}
```

### Resume Summary Agents

```bash
curl --request POST \
    --url http://localhost:8123/runs/wait \
    --header 'Content-Type: application/json' \
    --header "x-api-key: $LANGCHAIN_API_KEY" \
    --data '{
    "assistant_id": "resume_summary",
    "input": {
        "input": "This is my resume.\nMy name is John Doe and I work as a freelance developer."
    }
}'
```

```json
{
    "input": "This is my resume.\nMy name is John Doe and I work as a freelance developer.",
    "output": "John Doe is a freelance developer with experience in the tech industry. His resume highlights his role as an independent professional, showcasing his ability to manage and execute development projects on his own."
}
```

### Company Research Agent

This agent performs comprehensive research about a company using web search and financial APIs.

```bash
curl --request POST \
    --url http://localhost:8123/runs/wait \
    --header 'Content-Type: application/json' \
    --header "x-api-key: $LANGCHAIN_API_KEY" \
    --data '{
    "assistant_id": "company_research",
    "input": {
        "input": "Apple Inc"
    }
}'
```

```json
{
    "input": "Apple Inc",
    "output": {
        "officers": [
            { "name": "Tim Cook", "title": "CEO" },
            { "name": "Katherine Adams", "title": "Senior Vice President and General Counsel" },
            { "name": "Eddy Cue", "title": "Senior Vice President, Services" },
            { "name": "Craig Federighi", "title": "Senior Vice President" },
            { "name": "John Giannandrea", "title": "Senior Vice President" },
            { "name": "Greg "Joz" Joswiak", "title": "Senior Vice President" },
            { "name": "Sabih Khan", "title": "Senior Vice President" },
            { "name": "Deirdre O'Brien", "title": "Senior Vice President" }
        ],
        "current_stock_price": 232.105,
        "year_founded": 1976,
        "headquartered_at": "Cupertino, California, United States"
    }
}
```

The Company Research Agent takes a company name as input and returns:
- List of key company officers and their titles
- Current stock price (if publicly traded)
- Year the company was founded
- Company headquarters location

It uses Google Serper for web search and Finnhub for real-time stock prices.

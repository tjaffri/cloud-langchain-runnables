### Deployment on LangGraph Cloud

## Developing locally

To debug locally, you need a `.env` file with the `$SECRET`, `$OPENAI_API_KEY` and `LANGSMITH_API_KEY` variables. You can then run `langgraph up` as noted in the instructions here: https://langchain-ai.github.io/langgraph/cloud/quick_start/#using-the-langgraph-cli

## Routes

The LangChain runnables are exposed as the following agents on the API.

### Simple Add One Agent

```bash
curl --request POST \
    --url http://localhost:8123/runs/wait \
    --header 'Content-Type: application/json' \
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

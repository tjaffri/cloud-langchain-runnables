### Deployment on LangGraph Cloud

## Developing locally

To debug locally, you need a `.env` file with the `$SECRET`, `$OPENAI_API_KEY` and `LANGSMITH_API_KEY` variables. You can then run `langgraph up` as noted in the instructions here: https://langchain-ai.github.io/langgraph/cloud/quick_start/#using-the-langgraph-cli

## Routes

The LangChain runnables are exposed as the following routes on the API.

### Simple Add One Route

```bash
curl --request POST \
    --url http://localhost:8123/runs/wait \
    --header 'Content-Type: application/json' \
    --data '{
    "assistant_id": "add_one",
    "input": {
        "messages": [
            {
                "role": "user",
                "content": "49"
            }
        ]
    }
}'
````

```json
{"messages":[{"content":"49","additional_kwargs":{},"response_metadata":{},"type":"human","name":null,"id":"7562a25e-47a8-4da6-8b7d-8fe9bd70cdfd","example":false},{"content":"50","additional_kwargs":{},"response_metadata":{},"type":"ai","name":null,"id":"effb7768-2fba-4422-b447-62cdf10fc8ae","example":false,"tool_calls":[],"invalid_tool_calls":[],"usage_metadata":null}]}
```

### Resume Key Points Route

```bash
curl --location --request POST 'http://0.0.0.0:8000/resume_key_points/invoke' \
    --header 'Content-Type: application/json' \
    --header "x-token: $SECRET" \
    --data-raw '{
        "input": {
            "resume_text": "This is my resume.\nMy name is John Doe and I work at a freelance developer."
        }
    }'
```

```json
{"output":{"content":"John,Doe,,freelance,developer","additional_kwargs":{},"response_metadata":{"token_usage":{"completion_tokens":9,"prompt_tokens":96,"total_tokens":105},"model_name":"gpt-4o-2024-05-13","system_fingerprint":"fp_c4e5b6fa31","finish_reason":"stop","logprobs":null},"type":"ai","name":null,"id":"run-af020e8c-a9e7-4327-ba4a-e97897c407ac-0","example":false,"tool_calls":[],"invalid_tool_calls":[],"usage_metadata":{"input_tokens":96,"output_tokens":9,"total_tokens":105}},"metadata":{"run_id":"cb39fe59-7be8-45b1-99a7-89ef89d23216","feedback_tokens":[]}}
```

### Resume Summary Route

```bash
curl --location --request POST 'http://0.0.0.0:8000/resume_summary/invoke' \
    --header 'Content-Type: application/json' \
    --header "x-token: $SECRET" \
    --data-raw '{
        "input": {
            "resume_text": "This is my resume.\nMy name is John Doe and I work at a freelance developer."
        }
    }'
```

```json
{"output":{"content":"John Doe is a freelance developer with experience in the tech industry. His resume highlights his role as an independent professional, showcasing his ability to manage and execute development projects on his own.","additional_kwargs":{},"response_metadata":{"token_usage":{"completion_tokens":36,"prompt_tokens":51,"total_tokens":87},"model_name":"gpt-4o-2024-05-13","system_fingerprint":"fp_c4e5b6fa31","finish_reason":"stop","logprobs":null},"type":"ai","name":null,"id":"run-da8bc26d-98b8-4259-a5f8-1d1c2f86cb27-0","example":false,"tool_calls":[],"invalid_tool_calls":[],"usage_metadata":{"input_tokens":51,"output_tokens":36,"total_tokens":87}},"metadata":{"run_id":"8aa7c82b-4bdc-448c-85ec-223b3fb46e6d","feedback_tokens":[]}}
```

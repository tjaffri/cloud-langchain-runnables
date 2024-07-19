# Sample LangChain Runnables Hosted on Railway 

## Simple Add One Route
curl --location --request POST 'http://localhost:8000/add_one/invoke' \
    --header 'Content-Type: application/json' \
    --header "x-token: $SECRET" \
    --data-raw '{
        "input": 1
    }'
# Sample LangChain Runnables Hosted on Railway 

## Simple Add One Route
curl --location --request POST 'http://0.0.0.0:8000/add_one/invoke' \
    --header 'Content-Type: application/json' \
    --header "x-token: $SECRET" \
    --data-raw '{
        "input": 1
    }'

## Resume Key Points Route
curl --location --request POST 'http://0.0.0.0:8000/resume_key_points/invoke' \
    --header 'Content-Type: application/json' \
    --header "x-token: $SECRET" \
    --data-raw '{
        "input": {
            "resume_text": "This is my resume.\nMy name is John Doe and I work at a freelance developer."
        }
    }'

## Resume Summary Route
curl --location --request POST 'http://0.0.0.0:8000/resume_summary/invoke' \
    --header 'Content-Type: application/json' \
    --header "x-token: $SECRET" \
    --data-raw '{
        "input": {
            "resume_text": "This is my resume.\nMy name is John Doe and I work at a freelance developer."
        }
    }'


# OpenAI Agent Evaluation

A Python-based customer support AI agent with an
evaluation framework for measuring response quality.

## Features

- AI-powered customer support agent
- Knowledge base integration
- JSONL-based evaluation dataset
- Semantic similarity grading
- Cosine similarity scoring
- PASS/FAIL evaluation
- Automated evaluation reports

## Project Structure

- agent.py: Customer support agent
- knowledge_base.py: Company knowledge
- tools.py: Agent tools
- dataset.jsonl: Evaluation dataset
- evaluate.py: Evaluation runner
- semantic_grader.py: Semantic similarity grader
- results/: Evaluation reports

## Installation

Install dependencies:

pip install -r requirements.txt

Configure your API key in openai.env:

OPENAI_API_KEY=your_api_key

## Run Evaluation

python evaluate.py

## Semantic Grading

The project uses Sentence Transformers
with the all-MiniLM-L6-v2 model.

Expected and actual responses are converted
into embeddings.

Cosine similarity is used to calculate
semantic similarity.

Default threshold: 0.75

Responses meeting or exceeding the threshold
are marked PASS.

## Evaluation Metrics

- Total test cases
- Passed test cases
- Failed test cases
- Accuracy percentage
- Semantic similarity scores

## Important Limitations

Semantic similarity does not guarantee
factual correctness.

For production evaluation, combine semantic
grading with rule-based checks and
LLM-as-a-judge evaluation.

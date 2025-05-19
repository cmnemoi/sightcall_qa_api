# Sightcall Q&A API

[![Continuous Integration](https://github.com/cmnemoi/sightcall_qa_api/actions/workflows/continuous_integration.yaml/badge.svg)](https://github.com/cmnemoi/sightcall_qa_api/actions/workflows/continuous_integration.yaml)
[![Continuous Delivery](https://github.com/cmnemoi/sightcall_qa_api/actions/workflows/continuous_delivery.yaml/badge.svg)](https://github.com/cmnemoi/sightcall_qa_api/actions/workflows/continuous_delivery.yaml)
[![codecov](https://codecov.io/gh/cmnemoi/sightcall_qa_api/graph/badge.svg?token=FLAARH38AG)](https://codecov.io/gh/cmnemoi/sightcall_qa_api)

A RAG-based API to answer questions about SightCall using curated data.

Stack:
- [FastAPI](https://fastapi.tiangolo.com/) for the API, [pytest](https://docs.pytest.org/en/stable/) for automated testing
- [PGVector](https://github.com/pgvector/pgvector) for the vector database allowing document retrieval
- [Github Actions](https://github.com/features/actions) for CI/CD pipeline
- [Google Cloud Run](https://cloud.google.com/run) for containerized deployment
- [Terraform](https://www.terraform.io/) for automated infrastructure provisioning

# Installation

## Prerequisites

- [curl](https://curl.se/)
- [Docker Compose](https://docs.docker.com/compose/install/)
- [make](https://www.gnu.org/software/make/)
- [uv](https://docs.astral.sh/uv/getting-started/installation/)

## Setup

1. First, clone and install the project:

```bash
curl -sSL https://raw.githubusercontent.com/cmnemoi/sightcall_qa_api/main/clone-and-install | bash
```

2. Configure your OpenAI API key:
   - Open the `.env` file that was created during installation
   - Find the `OPENAI_API_KEY` variable
   - Replace `sk-` with your actual OpenAI API key

   You can get an API key from [OpenAI's API keys page](https://platform.openai.com/api-keys) if you don't have one already.

## Usage

You can interact with the API by running the following command:

```bash
curl -X POST "http://sightcall-qa.localhost/chat" \
     -H "Content-Type: application/json" \
     -d '{
           "question": "What is SightCall?"
         }'
```

Or by accessing the API OpenAPI / Swagger documentation at http://sightcall-qa.localhost/docs.

## Indexation

To improve the RAG model's responses, you can index SightCall's website into the vector database by running:

```bash
make indexation
```

# Development

- Lint code with `make lint`
- Run tests with `make test`
- Start the API locally with `make watch`

# License

The source code of this repository is licensed under the [AGPL-3.0-or-later License](LICENSE).
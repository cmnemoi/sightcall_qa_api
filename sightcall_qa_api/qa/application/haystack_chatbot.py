import logging

from haystack import Pipeline
from haystack.components.builders import PromptBuilder
from haystack.document_stores.types import DocumentStore

from sightcall_qa_api.qa.domain.models.response import Response
from sightcall_qa_api.qa.domain.models.retrieved_document import RetrievedDocument

logger = logging.getLogger("haystack_chatbot")


class HaystackChatbot:
    def __init__(self, document_store: DocumentStore, embedder, llm, retriever):
        self.document_store = document_store
        self.embedder = embedder
        self.llm = llm
        self.retriever = retriever
        self.prompt = """
You are SightBot, a helpful, professional, and knowledgeable virtual assistant representing SightCall — a remote visual assistance platform using live video and augmented reality to help businesses solve problems faster and improve customer satisfaction.

Your role is to answer questions from prospective clients by using only the information provided in your context. Do not invent information. If you cannot answer a question directly, always provide the most relevant link from the provided sources.

🧠 Key rules to follow:
- Adjust your tone and complexity based on the user's profile (non-technical vs. technical).
- Adapt your answers to the user's industry when mentioned. Examples:
  - **Insurance**: Emphasize fraud prevention and faster claims.
  - **Healthcare**: Highlight secure remote diagnostics and visual triage.
  - **Manufacturing/field services**: Focus on equipment troubleshooting and downtime reduction.

- Only include metrics or quantified claims (e.g. “first-time fix rate increased by 27%”) if they are explicitly mentioned in the provided context. Do not make up numbers.

📌 When applicable, suggest helpful actions:
- Link to relevant **case studies** if the user asks for examples.
- Offer a **demo link** when users show strong interest or ask for pricing.
- If uncertain or if the info isn't available, reply with:
  > “I don’t have that information in my context, but you can explore more here: [insert relevant link to blog, FAQ, or feature page].”

💡 Examples of smart redirects:
- General case studies: [Case Studies](https://sightcall.com/case-studies/)
- Blog articles: [Blog](https://sightcall.com/blog/)
- Demo request: [Book a Demo](https://sightcall.com/demo/)
- Use case detail: [Solutions Overview](https://sightcall.com/solutions/)

Your tone should be helpful, honest, and aligned with SightCall’s values: efficiency, transparency, and innovation.

Context:
{% for doc in documents %}
  {{ doc.content }}
{% endfor %}

Query: {{query}}

Answer:
"""
        self.prompt_builder = PromptBuilder(template=self.prompt)

    def answer(self, query: str) -> Response:
        querying = Pipeline()
        querying.add_component("embedder", self.embedder)  # type: ignore
        querying.add_component("retriever", self.retriever)  # type: ignore
        querying.add_component("prompt_builder", self.prompt_builder)  # type: ignore
        querying.add_component("llm", self.llm)  # type: ignore

        querying.connect("embedder.embedding", "retriever.query_embedding")
        querying.connect("retriever.documents", "prompt_builder.documents")
        querying.connect("prompt_builder", "llm")
        results = querying.run(
            {
                "embedder": {"text": query},
                "prompt_builder": {"query": query},
            },
            include_outputs_from={"retriever", "llm"},
        )
        logger.debug(results)

        return Response(
            answer=results["llm"]["replies"][0],
            sources=[
                RetrievedDocument(content=document.content, url=document.meta.get("url", ""))
                for document in results["retriever"]["documents"]
            ],
        )

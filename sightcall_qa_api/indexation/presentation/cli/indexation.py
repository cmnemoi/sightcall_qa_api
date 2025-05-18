from typing import Annotated

import typer
from haystack.document_stores.types import DuplicatePolicy
from haystack.utils import Secret
from haystack_integrations.document_stores.pgvector import PgvectorDocumentStore
from rich.console import Console

from sightcall_qa_api.config import Config
from sightcall_qa_api.indexation.application.haystack_indexer import HaystackIndexer
from sightcall_qa_api.indexation.domain.models.url import Url
from sightcall_qa_api.indexation.infrastructure.for_production.httpx_client import HTTPXClient

app = typer.Typer()
console = Console()


@app.command()
def indexation(
    sitemap_url: Annotated[str, typer.Argument(help="URL of the sitemap to index")],
    policy: Annotated[
        str, typer.Option(help="Policy for handling duplicate documents")
    ] = DuplicatePolicy.OVERWRITE.value,
    database_url: Annotated[str | None, typer.Option("--database-url", help="Database URL to use")] = None,
) -> None:
    try:
        document_store = PgvectorDocumentStore(
            connection_string=Secret.from_token(database_url) if database_url else Secret.from_env_var("DATABASE_URL"),
            embedding_dimension=3072,
            recreate_table=True,
        )
        indexer = HaystackIndexer(Config(), HTTPXClient(), document_store)
        with console.status("Indexing documents...", spinner="dots"):
            document_count = indexer.run(Url(sitemap_url), DuplicatePolicy(policy))
        console.print(f"Successfully indexed {document_count} documents!")
    except Exception as _:
        console.print_exception()
        raise typer.Exit(code=1)


if __name__ == "__main__":
    app()

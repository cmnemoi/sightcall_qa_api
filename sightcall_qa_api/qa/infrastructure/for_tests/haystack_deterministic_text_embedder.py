import hashlib

from haystack import component


@component
class HaystackDeterministicTextEmbedder:
    """
    A deterministic embedder for testing purposes.

    This component generates consistent embedding vectors for the same input text
    across different Python sessions. It's useful for testing scenarios where
    predictable embedding behavior is required.

    The embedder uses SHA-256 hashing to generate deterministic values and
    distributes these values across the specified embedding dimensions.

    Example:
        ```python
        embedder = HaystackDeterministicTextEmbedder(embeddings_size=384)
        result = embedder.run("example text")
        embedding = result["embedding"]  # List[float] of length 384
        ```
    """

    _BYTE_SCALE = 1.0 / 256.0  # Scale byte values (0-255) to [0, 1)

    def __init__(self, embeddings_size: int = 384) -> None:
        """Initialize the deterministic text embedder with the specified embedding size.

        Args:
            size: The dimensionality of the embedding vectors to generate.
                  Must be a positive integer.

        Raises:
            ValueError: If size is not a positive integer.
        """
        if embeddings_size <= 0:
            raise ValueError("Embedding size must be a positive integer")

        self._embedding_size = embeddings_size

    @component.output_types(embedding=list[float])
    def run(self, text: str) -> dict[str, list[float]]:
        """Generate a deterministic embedding for the input text.

        Args:
            text: The text to generate an embedding for.

        Returns:
            A dictionary containing the embedding vector under the 'embedding' key.
        """
        return {"embedding": self._generate_embedding_values(text)}

    def _generate_embedding_values(self, text: str) -> list[float]:
        if not text:
            return [0.0] * self._embedding_size

        hasher = hashlib.sha256()
        hasher.update(text.encode("utf-8"))
        hash_bytes = hasher.digest()

        return [float(hash_bytes[i % len(hash_bytes)]) * self._BYTE_SCALE for i in range(self._embedding_size)]

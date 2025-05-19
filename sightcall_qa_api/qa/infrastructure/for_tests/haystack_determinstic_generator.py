from haystack import component


@component
class HaystackDeterminsticTextGenerator:
    """
    Always returns the same answer for any input prompt.

    This generator is useful for testing purposes.

    ### Usage example

    ```python
    generator = HaystackDeterminsticTextGenerator(answer="42")
    result = generator.run("What is the meaning of life?")
    answer = result["replies"][0]  # Always "42"
    ```
    """

    def __init__(self, answer: str = ""):
        """Initialize the deterministic text generator with the specified answer.

        :param answer: The answer to return for any input prompt.
        """
        self.answer = answer

    @component.output_types(replies=list[str])
    def run(self, prompt: str) -> dict[str, list[str]]:
        """Generate a deterministic answer for the input prompt.

        :param prompt: The prompt to generate an answer for.
        :return: A dictionary containing the answer under the 'replies' key.
        """
        return {"replies": [self.answer]}

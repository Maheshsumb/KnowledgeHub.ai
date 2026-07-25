class ConversationFormatter:
    """
    Formats a list of Message objects into a plain-text conversation
    string suitable for inclusion in an LLM prompt.

    Designed to be swapped for OpenAI / Gemini / Claude structured
    formats later without touching ChatService.
    """

    def format(
        self,
        messages: list,
    ) -> str:

        if not messages:
            return ""

        lines = []

        for message in messages:
            lines.append(
                f"{message.role.title()}: {message.content}"
            )

        return "\n".join(lines)

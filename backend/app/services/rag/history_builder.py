class HistoryBuilder:

    def build(
        self,
        messages,
    ) -> str:

        history = ""

        for message in messages:

            history += (
                f"{message.role.title()}: "
                f"{message.content}\n"
            )

        return history
class PromptBuilder:
    """
    Builds structured prompts for Retrieval-Augmented Generation (RAG).

    Prompt layout:
      1. System Instructions  — tells the model who it is and how to behave
      2. Few-shot Examples    — calibrate the model's expected output style
      3. Conversation History — (optional) recent turns for reference resolution
      4. Retrieved Context    — evidence from the knowledge base
      5. Current Question     — what the user is asking right now
    """

    @staticmethod
    def build(
        question: str,
        context: str,
        history: str = "",
    ) -> str:

        # ── 1. System instructions ──────────────────────────────────────
        prompt = """\
You are KnowledgeHub AI, an enterprise AI assistant.

Your primary source of truth is the Retrieved Context below.
Use Conversation History ONLY to resolve references such as "it", "that", \
"this", "he", "she", or "they" — never to invent facts.

Rules:
1. Answer strictly from the Retrieved Context.
2. Do not make up, infer, or extrapolate information.
3. If the answer is not present in the context, respond with:
   "I couldn't find that information in the uploaded documents."
4. Be concise and professional.
5. When possible, mention which document the information came from.

====================

Examples:

[Example 1]
Context: "Employees are entitled to 20 days of paid leave per year \
(source: Employee Handbook v2)."
Question: "How many vacation days do I get?"
Answer: "According to the Employee Handbook v2, you are entitled to \
20 days of paid leave per year."

[Example 2]
Context: "The server will be down for maintenance from 2 AM to 4 AM on Sunday."
Question: "What is the capital of France?"
Answer: "I couldn't find that information in the uploaded documents."
"""

        # ── 2. Conversation History (optional) ──────────────────────────
        if history.strip():
            prompt += f"""
====================

Conversation History:

{history}
"""

        # ── 3. Retrieved Context ────────────────────────────────────────
        prompt += f"""
====================

Retrieved Context:

{context}

====================

Current Question:

{question}

====================

Answer:
"""
        return prompt.strip()
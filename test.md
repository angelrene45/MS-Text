This slide explains the anatomy of a semantic model — essentially, what components make it up and how each one contributes to accuracy and performance.

A semantic model connects business language to data, so the AI understands exactly what we mean when we ask a question.

Let’s walk through the main parts:

First, Metadata.
This defines the model’s name and description — it helps route questions to the right dataset, especially when multiple models exist.

Next, Tables and Relationships.
These define the structure — the dimensions and how they’re connected. This ensures valid joins, filters, and aggregations without hallucinations or mismatched data.

Search Services come next.
They enable fuzzy matching for values like customer names or venues, helping the AI interpret natural language queries more effectively.

Custom Instructions add business-specific rules — for example, defining that “Q1 starts on February 2nd.”
This helps clarify exceptions and unique SQL logic.

And finally, Verified Queries.
These are real-world questions with validated SQL. They train the model to answer similar questions accurately in the future.

Overall, these components work together to make the AI smarter, more precise, and more aligned with the organization’s data and language.

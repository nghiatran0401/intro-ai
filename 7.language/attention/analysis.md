### Layer 2, Head 5

This attention head appears to pay attention to the relationship between verbs and their direct objects. When a verb appears in the sentence, this head tends to attend strongly to the noun that serves as the direct object of that verb. This pattern helps BERT understand the action-object relationships in sentences.

Example Sentences:

- "The cat chased the [MASK] around the yard."
- "She bought a [MASK] from the store."

### Layer 5, Head 8

This attention head seems to focus on the relationship between pronouns and the nouns they refer to. When a pronoun (like "he", "she", "it", "they") appears in the sentence, this head attends to the noun phrase that the pronoun is referring to earlier in the sentence. This helps BERT track referential relationships and maintain coherence across the sentence.

Example Sentences:

- "The teacher gave the student a book and [MASK] read it carefully."
- "After the dog barked, [MASK] ran away quickly."

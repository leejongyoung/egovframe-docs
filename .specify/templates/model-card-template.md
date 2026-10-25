# Domain model card: <concept or feature name>

Use this template for one actual concept before writing its specification or bug assessment.
Save the completed card under `.specify/model-cards/<concept>.md` on `work`.
Follow the [constitution](../memory/constitution.md); link policy instead of copying it here.
This card describes domain meaning, not AI model training or evaluation.

## One-sentence definition

Define the concept in one sentence, naming its actors, object, and relevant boundary.

## Why it is needed

Describe the concrete user or maintainer problem, who benefits, and why existing behavior is
insufficient. Link a public issue or documented use case when available.

## Existing models and terminology

List related entities, interfaces, schemas, UI terms, or documentation that this concept reuses.
For each, link the source and explain whether it is equivalent, narrower, or intentionally different.
Distinguish published contracts from an observed implementation and from an unverified hypothesis.

## Synthetic example data

Provide the smallest fictitious input and state needed to understand the concept. Include types,
units, optional values, and constraints where meaningful. Never use real credentials or personal data.

## Successful behavior

Give concrete input/precondition -> expected output/state examples, including relevant edge cases.
Cite the source of each expected behavior; label proposed behavior as a proposal.

## Rejected or invalid behavior

Give invalid input/precondition -> expected rejection/error/no-op examples. Explain which boundary
enforces each rule and which consumer observes the result. Mark unknown semantics explicitly.

## Outside this concept's responsibility

List responsibilities owned by another component or system and changes intentionally excluded.
Name the relevant boundary so future plans do not expand the scope silently.

## Rule sources and assumptions

| Rule | Source and revision/date | Evidence kind | Assumptions or limits |
| --- | --- | --- | --- |
| Describe a concrete rule | Link the exact file, public contract, or issue | Published / observed / proposed / unverified | State what is not established |

Do not turn a public issue claim or agent inference into an agreed requirement without evidence.

## Open questions

List unresolved decisions, who can resolve them, and what evidence is needed. Separate blockers
requiring a product policy decision from implementation details that preserve the existing contract.
Write “None identified” only after checking the relevant evidence.

## Next step and evidence of completion

Link the appropriate specification or bug assessment, then the plan and actual verification when
those exist. Record only performed checks and their results; leave future work clearly pending.

---
applyTo: "**/*.ttl"
---

# SAMM aspect model review

The formal MS2 criteria are checked automatically by a script. Only review what needs judgement.

Review the human-readable texts (`samm:preferredName`, `samm:description`) of all elements in the changed aspect models.
Read the whole model and use its structure (element names and types, links between elements, characteristics, constraints, enumeration values, units, example values) as reference to check these texts.

## Report only these findings

- **Copy-Paste:** the text refers to or describes a different element than the one it belongs to.
- **Typo:** a word is misspelled.
- **Encoding:** characters or markup are broken.
- **URL:** a link is broken.
- **Content:** the `samm:preferredName` or `samm:description` contradicts the model itself or other texts in the same model.
- **Abbreviation (MS2-10):** an abbreviation is uncommon and not explained anywhere in the model.
- **Aspect name (MS2-14):** the Aspect name must be singular, unless its only property is a Collection, List or Set. In that case it must be plural.
- **Unit (MS2-15):** a text names a unit that the characteristic does not define, or the units differ.
- **Constraint (MS2-16):** a text states a restriction (range, length, format, pattern) that is not modelled as a constraint.
- **See (MS2-17):** a text names or links an external standard, but the element has no `samm:see` reference to it.
- **Enumeration:** an element whose name or description indicates a classification (e.g. type, category, class, classification, status, kind, level) is not modelled as an enumeration. Free values cannot be processed automatically and break interoperability.
- **Example value (MS2-18):** the `samm:exampleValue` does not fit the description, enumeration values or constraints.

## Never report

If unsure, do not report.

## Output

One inline review comment per finding on the affected line:

- First line: `**[Category]** element · attribute`, followed by the finding.
- Then a GitHub suggestion block (```` ```suggestion ````) with the complete corrected line, so the author can apply it with one click. Change only what the finding is about.
- If there is no concrete fix, explain the finding without a suggestion block.

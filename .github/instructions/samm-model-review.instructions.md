---
applyTo: "**/*.ttl"
excludeAgent: "coding-agent"
---

# SAMM aspect model review

The formal MS2 criteria are checked automatically by a script. Only review what needs judgement.

Review the human-readable texts (`samm:preferredName`, `samm:description`) of all elements in the changed aspect models, and whether the modelling matches what these texts state.
Read the whole model and use its structure (element names and types, links between elements, characteristics, constraints, enumeration values, units, example values) as reference.

**No findings is a valid result.** There is no minimum and no maximum number of findings: report every finding that meets the bar below, and nothing else.

## Report only these findings

Check the model once per category: one separate pass for each category below.

- **Copy-Paste:** the text refers to or describes a different element than the one it belongs to, or was copied from another specification without adaption (e.g. mentions an "XML element").
- **Typo:** a word or element name is misspelled, split or joined wrongly, or spelled inconsistently with the same term elsewhere in the model.
- **Encoding:** characters or markup are broken, e.g. literal line breaks (`\n`) inside a text.
- **URL:** a link is visibly malformed (e.g. contains spaces, is cut off, or has a missing scheme).
- **Content:** the text contradicts the model itself or other texts in the same model, or refers to an element that does not exist in the model.
- **Abbreviation (MS2-10):** an abbreviation is uncommon and not explained anywhere in the model.
- **Aspect name (MS2-14):** the Aspect name must be singular, unless its only property is a Collection, List or Set. In that case it must be plural.
- **Unit (MS2-15):** a text names a unit that the characteristic does not define, or the units differ.
- **Constraint (MS2-16):** a text states a restriction on a single value (range, length, format, pattern) that is not modelled as a constraint.
- **See (MS2-17):** a text names or links an external standard, but the element has no `samm:see` reference to it.
- **Enumeration:** an element whose name or description indicates a classification (e.g. type, category, class, classification, status, kind, level) is not modelled as an enumeration. Free values cannot be processed automatically and break interoperability.
- **Example value (MS2-18):** the `samm:exampleValue` does not fit the description, enumeration values or constraints.

## Bar for a finding

Report a finding only if both apply:

- You can quote the exact text that is wrong.
- You can name the concrete error, not just a possible improvement.

## Never report

- Wording, style or grammar preferences when the text is correct and understandable.
- Rephrasings that do not fix a concrete error.
- Missing detail when the text is correct.
- Restrictions SAMM cannot model, such as dependencies between properties. They belong in the description.
- Anything outside the categories above.

## Examples

Findings:

- Typo: `samm:preferredName "inorganic Or Fossi lBased Content"` - should be `"inorganic or fossil-based content"`.
- Encoding: `samm:description "ID of the bio-based content \ncertificate."` - line break inside the text.
- Content: description refers to "BioBasedSecondary", but the model only has `secondaryBioBasedMaterialContent`.
- Copy-Paste: "The part type from which the serialized part has been instantiated." in a part type model without a serialized part.

No findings:

- "Must add up to 100 percent to the max value of bioBasedContent" - SAMM cannot model dependencies between properties.
- A correct, understandable description that could be phrased differently.

## Output

If there are no findings, post no comments.

One inline review comment per finding on the affected line:

- First line: `**[Category]** element · attribute`, followed by the finding.
- Then a GitHub suggestion block (```` ```suggestion ````) with the complete corrected line, so the author can apply it with one click. Change only what the finding is about.
- If there is no concrete fix, explain the finding without a suggestion block.

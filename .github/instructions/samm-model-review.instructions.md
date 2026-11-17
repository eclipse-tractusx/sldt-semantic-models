---
applyTo: "**/*.ttl"
---

# SAMM aspect model review

The formal MS2 criteria are checked automatically by a script. Only review what needs judgement.

Review the human-readable texts (`samm:preferredName`, `samm:description`) of all elements in the changed aspect models.
Read the whole model and use its structure (element names and types, links between elements, characteristics, constraints, enumeration values, units, example values) as reference to check these texts.

Go through every element one by one and check each text individually. Simple findings (typos, broken encoding, wrong element references) are as important as complex ones - do not skip them in favour of a few complex findings.

**No findings is a valid and expected result.** Most models have none. There is no minimum and no maximum number of findings: report every finding that meets the bar below, and nothing else.

## Report only these findings

- **Copy-Paste:** the text refers to or describes a different element than the one it belongs to, or was copied from another specification without adaption (e.g. mentions an "XML element").
- **Typo:** a word or element name is misspelled, split or joined wrongly, or spelled inconsistently with the same term elsewhere in the model.
- **Encoding:** characters or markup are broken, e.g. literal line breaks (`\n`) inside a text.
- **URL:** a link is broken.
- **Content:** the text contradicts the model itself or other texts in the same model, or refers to an element that does not exist in the model.
- **Abbreviation (MS2-10):** an abbreviation is uncommon and not explained anywhere in the model.
- **Aspect name (MS2-14):** the Aspect name must be singular, unless its only property is a Collection, List or Set. In that case it must be plural.
- **Unit (MS2-15):** a text names a unit that the characteristic does not define, or the units differ.
- **Constraint (MS2-16):** a text states a restriction on a single value (range, length, format, pattern) that is not modelled as a constraint. Restrictions SAMM cannot model (e.g. several values adding up to 100 %) belong in the description and are no finding.
- **See (MS2-17):** a text names or links an external standard, but the element has no `samm:see` reference to it.
- **Enumeration:** an element whose name or description indicates a classification (e.g. type, category, class, classification, status, kind, level) is not modelled as an enumeration. Free values cannot be processed automatically and break interoperability.
- **Example value (MS2-18):** the `samm:exampleValue` does not fit the description, enumeration values or constraints.

## Bar for a finding

Report a finding only if all of these apply:

- It matches one of the categories above.
- You can quote the exact text that is wrong.
- You can name the concrete error, not just a possible improvement.
- A domain expert reading the model would agree that it is an error.

## Never report

- Wording, style or grammar preferences when the text is correct and understandable.
- Rephrasings that do not fix a concrete error.
- Missing detail when the text is correct.
- Anything outside the categories above.
- If unsure, do not report.

## Output

If there are no findings, post no comments.

One inline review comment per finding on the affected line:

- First line: `**[Category]** element · attribute`, followed by the finding.
- Then a GitHub suggestion block (```` ```suggestion ````) with the complete corrected line, so the author can apply it with one click. Change only what the finding is about.
- If there is no concrete fix, explain the finding without a suggestion block.

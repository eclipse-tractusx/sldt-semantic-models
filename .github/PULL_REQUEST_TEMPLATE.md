## Description
<!-- Please provide a short description about what this PR changes and reference an issue that was initially created to introduce the new aspect model -->

 -->

Closes #

<!-- The MS2 and MS3 criteria are intended for merges to the main-branch. For small bug-fixes or during the model development, for instance, when merging to a feature branch, you may decide to not fill out the checklists. However, we recommend to follow the MS2 checklist during the development. The MS3 checklist becomes relevant for merges to the main-branch. -->
## MS2 Criteria
(to be filled out by PR reviewer)
- [ ] the model **validates** with the SAMM SDS SDK in the version specified in the Readme.md of this repository by the time of the MS2 check  (e.g., 'java -jar samm-cli.jar aspect \<path-to-aspect-model\> validate ). The  SAMM CLI is available [here](https://eclipse-esmf.github.io/esmf-developer-guide/tooling-guide/samm-cli.html) and in [GitHub](https://github.com/eclipse-esmf/esmf-sdk/releases/tag/v2.6.0)
- [ ] use **Camel-Case** (e.g., "MyModelElement" or "TimeDifferenceGmtId", when in doubt follow https://google.github.io/styleguide/javaguide.html#s5.3-camel-case)
- [ ] the identifiers for all model elements **start with a capital letter** except for properties
- [ ] the identifier for **properties starts with a small letter**
- [ ] all model elements **at least contain the fields "preferred name" and "description"** in English language. The description must be comprehensible. It is not required to write full sentences but style should be consistent over the whole model
- [ ] Property and the referenced Characteristic should not have the same name
- [ ] the versioning in the URN **follows semantic versioning**, where minor version bumps are backwards compatible and major version bumps are not backwards compatible. 
- [ ] use **abbreviations only when necessary** and if these are sufficiently common
- [ ] **avoid redundant prefixes in property names** (consider adding properties to an enclosing Entity or even adapt the namespace of the model elements, e.g., instead of having two properties `DismantlerId` and `DismantlerName` use an Entity `Dismantler` with the properties `name` and `id` or use a URN like `io.catenax.dismantler:0.0.1`)
- [ ] fields `preferredName` and `description` are not the same
- [ ] **`preferredName` should be human readable** and follow normal orthography (e.g., no camel case but normal word separation)
- [ ] name of aspect is singular except if it only has one property which is a Collection, List or Set. In theses cases, the aspect name is plural.
- [ ] units are referenced from the SAMM unit catalog whenever possible
- [ ] **use constraints** to make known constraints from the use case explicit in the aspect model 
- [ ] when relying on **external standards**, they are referenced through a **"see"** element
- [ ] all properties with an [simple type](https://eclipse-esmf.github.io/samm-specification/2.0.0/datatypes.html) have an example value
- [ ] metadata.json exists with status "release"
- [ ] generated json schema validates against example json payload
- [ ] file RELEASE_NOTES.md exists and contains entries for proposed model changes 
- [ ] all contributors to this model are mentioned in copyright header of model file

## MS3 Criteria
(to be filled out by semantic modeling team before merge to main-branch)
- [ ] All required reviewers have approved this PR (see reviewers section)
- [ ] The new aspect (version) will be implemented by at least one data provider
- [ ] The new aspect (version) will be consumed by at least one data consumer
- [ ] There exists valid test data
- [ ] In case of a new (incompatible) major version to an existing version, a migration strategy has been developed
- [ ] The model has at least version '1.0.0'
- [ ] If a previous model exists, model deprecation has been checked for previous model
- [ ] The release date in the Release Note is set to the date of the MS3 approval

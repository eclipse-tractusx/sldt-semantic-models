## Description
<!-- Please provide a short description about what this PR changes and reference an issue that was initially created to introduce the new aspect model -->

 -->

Closes #

<!-- The MS2 and MS3 criteria are intended for merges to the main-branch. For small bug-fixes or during the model development, for instance, when merging to a feature branch, you may decide to not fill out the checklists. However, we recommend to follow the MS2 checklist during the development. The MS3 checklist becomes relevant for merges to the main-branch. -->

## MS2 Criteria

(to be filled out by PR reviewer)
- [ ] [MS2-01] the model **validates** with the SAMM SDS SDK in the version specified in the Readme.md of this repository by the time of the MS2 check  (e.g., 'java -jar samm-cli.jar aspect \<path-to-aspect-model\> validate ). The  SAMM CLI is available [here](https://eclipse-esmf.github.io/esmf-developer-guide/tooling-guide/samm-cli.html) and in [GitHub](https://github.com/eclipse-esmf/esmf-sdk/releases/tag/v2.15.1)
- [ ] [MS2-02] generated json schema validates against example json payload
- [ ] [MS2-03] all artifact types generate successfully
- [ ] [MS2-04] metadata.json exists with status "release"
- [ ] [MS2-05] all external / imported models have the state "release"
- [ ] [MS2-06] the versioning in the URN **follows semantic versioning**, where minor version bumps are backwards compatible and major version bumps are not backwards compatible. 
- [ ] [MS2-07] file RELEASE_NOTES.md exists and contains entries for proposed model changes 
- [ ] [MS2-08] all contributors to this model are mentioned in copyright header of model file
- [ ] [MS2-09] all model elements **at least contain the fields "preferred name" and "description"** in English language. The description must be comprehensible. It is not required to write full sentences but style should be consistent over the whole model
- [ ] [MS2-10] use **abbreviations only when necessary** and if these are sufficiently common
- [ ] [MS2-11] **avoid redundant prefixes in property names** (consider adding properties to an enclosing Entity or even adapt the namespace of the model elements, e.g., instead of having two properties `DismantlerId` and `DismantlerName` use an Entity `Dismantler` with the properties `name` and `id` or use a URN like `io.catenax.dismantler:0.0.1`)
- [ ] [MS2-12] fields `preferredName` and `description` are not the same
- [ ] [MS2-13] **`preferredName` should be human readable** and follow normal orthography (e.g., no camel case but normal word separation)
- [ ] [MS2-14] name of aspect is singular except if it only has one property which is a Collection, List or Set. In theses cases, the aspect name is plural.
- [ ] [MS2-15] units are referenced from the SAMM unit catalog whenever possible
- [ ] [MS2-16] **use constraints** to make known constraints from the use case explicit in the aspect model
- [ ] [MS2-17] when relying on **external standards**, they are referenced through a **"see"** element
- [ ] [MS2-18] all properties with an [simple type](https://eclipse-esmf.github.io/samm-specification/2.1.0/datatypes.html) have an example value
- [ ] [MS2-19] the identifiers for all model elements **start with a capital letter** except for properties
- [ ] [MS2-20] payload names and property identifiers must not contain two consecutive underscores ('__') at any position (e.g. `my__model` is not allowed)
- [ ] [MS2-21] use **Camel-Case** (e.g., "MyModelElement" or "TimeDifferenceGmtId", when in doubt follow https://google.github.io/styleguide/javaguide.html#s5.3-camel-case)
- [ ] [MS2-22] the identifier for **properties starts with a small letter**
- [ ] [MS2-23] Property and the referenced Characteristic should not have the same name

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

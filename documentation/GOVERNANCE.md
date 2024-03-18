# Aspect Model Governance Process
This repository hosts the Turtle files for the Tractus-X Aspect models. The models are based on the SAMM Aspect Meta Model to semantically describe the data that gets exchanged by solutions using Eclipse Tractus-X. These models need to be aligned and agreed upon within and preferably across the use cases targeted by Tractus-X. To achieve this agreement and visibility across the whole project, there is a dedicated governance process enabled for the models in this repository.
The following page introduces this process, the involved roles, and the states in which a model can be.

## Process
### Roles

| Role | Description |
| ---- | ------ |
| Domain Expert |  Domain experts know their specific use case and bring in practical input and requirements regarding data that needs to be consumed and provided as part of solutions in that application. |
| Modeling Expert | Modeling experts are knowledgeable about the modeling approach based on SAMM and have an overview of other already existing models. |
| Model Developers | Group of Domain and Modeling experts who jointly perform a modeling activity (create, update or delete model) |
| Modeling Team | Regular meeting round to discuss and moderate the modeling activities. |
| Use Case | Application or scenario were the need for the model creation or update arises. In general, it is assumed that a use case consists of at least one data provider and one data consumer |

### Modeling Stage 1 (MS1) Request for Model

When there is a requirement for a new or modified Aspect model, a domain expert from that use case initiates the modeling process by creating a new issue on GitHub (Tab: Issues -> Button: New Issue or [this link](https://github.com/eclipse-tractusx/sldt-semantic-models/issues/new/choose)).
Depending on the type of request (new model, model update, model deprecation), one may use different templates for the issue.
Based on the information given in the issue description, the modeling team decides whether to approve and to progress with the development of this model.
In that case, the modeling team assigns the label "MS1-Approved" and names at least one modeling expert in the GitHub issue who will support the domain experts in resolving the issue.

With the MS1 checklist and approval, the idea is to initiate the exchange between domain and modeling experts in an early development phase.
This way, model developers get fast feedback before investing time and effort on models for which they might not get an agreement within the modeling team.
The discussion of the model modifications shall further create awareness of currently ongoing modeling activities across modelers and use cases to avoid duplicate models and development for the same topic.

### Modeling Stage 2 (MS2) Valid Model
In the next step, the assigned domain experts and the modeling experts perform the modeling work and create a solution to fulfill the initial request.
This work happens on a dedicated development branch preferably in a forked repository (for details regarding Forks in GitHub consult the [GitHub documentation](https://docs.github.com/en/pull-requests/collaborating-with-pull-requests/working-with-forks/about-forks)).
As a result of this phase, the model developers propose the changes by creating a Pull-Request (PR) to commit the content of the new or updated model to the main-branch of the Tractus-X model repository.
To create a PR, select "New pull request" in the "Pull requests" tab.
The PR should link the initial issue requesting the change, e.g., by mentioning #{Issue-Number} in the description.
There is a template for this PR, which contains a checklist of modeling-specific guidelines.
It is the task of the modeling expert to check that the proposed model conforms to all items and best practices in the modeling checklist.
To indicate the conclusion of the modeling phase and that the model is ready for release and adoption, the modeling expert adds the label "MS2-Approved" to the PR.
If a proposal attempts to model the hierarchical relationship between parts, the Domain Expert and Reviewer are jointly
responsible for adherence to the schema of the Data Chain Template ([CX-0045](https://catena-x.net/fileadmin/user_upload/Standard-Bibliothek/Update_Januar_2024/CX-0045-AspectModelDataChainTemplate-v1.2.0.pdf) - link downloads pdf).
This is given if the generated json-payloads of Bills of Material (BoM, downward) and Usage (upward) conform to the
json-schemas given in the standard.

### Modeling Stage 3 (MS3) Release Model
The domain expert then checks with the use case team from which the initial modeling request originated to whether the proposed changes fulfill the requirements and that the use case will use it. There is a MS3 checklist in the PR template to guide the approval. This checklist, for example, asks whether there is at least one data provider and one data consumer planing to exchange data based on the definition in the proposed model. There is no specific process for getting the approval for the use case since this strongly depends on its working mode. However, one proven practice is to post the model and visualization in the working space of the use case team and ask for comments during a dedicated review period which could be one week. After the approval of the use case, the modeling team checks during one of its meetings that the proposed changes align with the other models in Tractus-X and that the model is ready for adoption from a modeling standpoint. The discussion of the model also helps the modeling team members to keep track of current modeling activities. If the use case and the modeling team approve the PR, the modeling team assigns the label "MS3-Approved" and merges the PR into the main branch of this Tractus-X models repository.

## Labels
To fascilitate the governance and keep track of ongoing PRs and issue in GitHub we use a set of labels as described in the following table:

| label | description |
----- | -------
Model_Update | A request for updating an existing model
New_Model | A request for a new model
Deprecate | A request for deprecating an existing model
MS1_Approved | Checklist "MS1 Request for Model Developement" is approved.
MS2_Approved | Checklist "MS2 Valid Model" is approved.
MS3_Approved | Checklist "MS3 Release Model" is approved. The associated pull request can be merged to the "main-branch".
Review_Required | For this PR or issue a review by a modeling expert is requested.
Modeling_Team | This issue or PR should be discussed in the modeling team.

Only project committer of the Eclipse Tractus-X project are allowed to assign labels to issues and PRs.
To nevertheless allow the structured marking of issues and PRs for committers to the Eclipse Tractus-X project, we use structured comments.

Thus, if you want to mark an issue or a PR, please add the aforementioned labels as a comment to the issue or PR. E.g., if you want to indicate that a PR should be discussed by the modeling team, add a comment

```
Modeling_Team
```
to the PR. We have filters, which check for such comments.

## Standardizing a model
If a model is used in a standard, this should be indicated by changing the status of the model to status "STANDARDIZED".
A model with can only reach status "STANDARDIZED" if it is "RELEASED" beforehand.
A model with status "STANDARDIZED" can only be moved to status "DEPRECATED" if the corresponding standard is "DEPRECATED" as well.

## Retiring a model
Once a model gets the status "DEPRECATED" it should not be used anymore by new use cases. Existing applications should look for a way to migrate to an alternative version or model. In alignment with the overall release cycles of Tractus-X, the modeling team tags the current main branch with the corresponding Tractus-X release and publishes modeling release notes. These release notes contain a hint about all model versions that changed the status to "DEPRECATED" since the previous Tractus-X release. The modeling team will delete these models two Tractus-X releases cycles later (independent of major or minor version change). So use cases are advised to react to the deprecation of models within the next release cycle.

For clarification of the deprecation strategy the following example: A model *A* was released with version 1.0.0 in Tractus-X v2.0.0. In v2.1.0 of Tractus-X a new version 2.0.0 of model *A* was released and version 1.0.0 of model *A* was deprecated. In v3.0.0 of Tractus-X both version 1.0.0 and 2.0.0 of model *A* are still present in the repository.
In the curse of the development cycle towards v3.1.0 of Tractus-X version 1.0.0 of model *A* is deleted so that version 1.0.0 of model *A* is not present in the repository anymore and only version 2.0.0 of model *A* is present when Tractus-X v3.1.0 is released.

## Versioning
The semantic modeling in Tractus-X follows [Semantic Versioning](https://semver.org/). Since the version is included in the Aspect Model's URI
(i.e. `urn:bamm:io.catenax.batch:1.0.2#Batch`), applications that work on the model may have incompatible API-changes even when the changes in the model
are marginal. The same phenomenon may occur with the [CX-standard-documents](https://catena-x.net/de/standard-library) that reference
a semantic model. Inspired by the definitions of SemVer, the following best practices shall be followed here:

- No increment: Trivial changes that do not affect the functional parts of the model may be changed via PR without an incremented version number.
  Changes must not affect the functional generated json-schema. This particularly applies to copyright-headers and descriptions,
  as long as the descriptions do not change the inherent meaning of a Property/Trait etc.
- Patch: A patch is a change in the model that does not add or remove functionality. This could for example be
  updating a model with an additional `bamm:see` attribute that has equivalent semantics to the aspect.
  Standard documents must be adjusted to reflect the patched versions.
- Minor: There are no minor increments of aspect models.
- Major: Major increments are constituted by breaking API changes such as adding, removing or (in cumolo) renaming
  elements (optional or non-optional) of a semantic model. Changing the meaning/semantics or the data type of an element
  is a major change too.

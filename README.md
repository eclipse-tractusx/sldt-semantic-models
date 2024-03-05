# Aspect Models for Eclipse Tractus-X Semantic Layer (SLDT)
The repository contains the aspect models based on [SAMM (Semantic Aspect Meta Model)](https://eclipse-esmf.github.io/samm-specification/2.0.0/index.html) for the Tractus-X project for Catena-X.

**Currently, we assume the usage of the version 2.6.0 of the [SAMM-CLI](https://eclipse-esmf.github.io/esmf-developer-guide/2.6.0/tooling-guide/samm-cli.html) and version 5.1.1 of the [Aspect Model Editor](https://eclipse-esmf.github.io/ame-guide/5.1.1/introduction.html) **.

# Using the models
The models can locally be processed with the [SAMM CLI](https://eclipse-esmf.github.io/esmf-developer-guide/2.6.0/tooling-guide/samm-cli.html), which is documented [here](https://eclipse-esmf.github.io/esmf-developer-guide/2.6.0/tooling-guide/samm-cli.html).
It allows you to generate different artifacts (diagrams, example payload, java class files) out of it.

For convenience you can also look into the `gen` folder of each model, which already contains often used  artifacts generated from the model.

# Status of model
Each model has its life cycle and can thus have a different status. This information always corresponds to a specific version of the model. To indicate the state of the model version in Git, one creates a file with the name `metadata.json` and places it in the same directory as the corresponding model file. It is also possible to load the models into the [Semantic Hub](https://github.com/eclipse-tractusx/sldt-semantic-hub) which has a corresponding state management. An example `metadata.json` looks like this:

```
{ "status" : "deprecate"} 
```

The following table lists the possible values for `status` and what they mean:

status | status in Semantic Hub | description
----| ---- | ---- |
draft | DRAFT | This version of the model is under development and can change at any time.
release | RELEASED | The version of the model is considered as stable and any modifications to the model trigger a new release and subsequentially a new version.
standardize | STANDARDIZED | The version of the model is the basis for an official Catena-x standard, published [here](https://catena-x.net/de/standard-library).
deprecate | DEPRECATED | The version of the model has reached its end-of-life and should not be used anymore because it will be deleted later.

The `metadata.json` is only relevant for model files on the branch `main`. All other branches are development branches, and the models from these branches or forks are therefore implicitly in status "DRAFT".

# How to contribute
We have a governance process for the joint development of new and updated models which we describe [in more details under this link](CONTRIBUTING.md).

## Summary of Governance Process
The governance process is **triggered by a domain expert** requesting a new model or model update. A **modeling team then reviews** the request to identify whether it is of interest for Catena-X and Tractus-X and whether there is not already another model which can solve the raised issue (indicating label **MS1-Approved**).

Once the request is accepted, **a modeling expert and the requesting domain expert create a solution**. The modeling expert then evaluates whether the new or updated model follows the modeling guidelines in Tractus-X (indicating label **MS2-Approved**). In the last step, the **requesting use case and the modeling team approve** that the resulting model fulfills the initial requirement and can be adopted (indicating label **MS3-Approved**). As a result, the content of the new model version cannot change, and adopters from use cases are safe to use the model.

We do this process for each version of a model. So there can be multiple versions of the model with different content in different phases of the model life-cycle.

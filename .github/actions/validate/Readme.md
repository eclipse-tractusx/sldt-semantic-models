<!--
#######################################################################
# Copyright (c) 2023 Contributors to the Eclipse Foundation
#
# See the NOTICE file(s) distributed with this work for additional
# information regarding copyright ownership.
#
# This work is made available under the terms of the
# Creative Commons Attribution 4.0 International (CC-BY-4.0) license,
# which is available at
# https://creativecommons.org/licenses/by/4.0/legalcode.
#
# SPDX-License-Identifier: CC-BY-4.0
#######################################################################
-->
# Note on updating ESMF SDK 
The action uses the [ESMF SDK](https://github.com/eclipse-esmf/esmf-sdk). In case of an update you need to change the variable ``bamm_version`` to the required version of the ESMF SDK in the file [action.yml](action.yml).

# Detect Changes Action
This action validates whether and which changes in the repository need to be applied to an instance of the Semantic Hub being associated with the repository.
The action expects multiple arrays which either contain added, modified, renamed and deleted files from the last commit. 

The actual deployment to an Semantic Hub instance is done through the Upload-action which expects a JSON-file with the changes to apply. Because of that, the result of the validation action is an archived JSON-file communicating these detected changes. 


## Test Cases
For future developments, we propose the following test cases to be evaluated:

### main branch

| Model | metadata.json | expected deployed model status |
----| ---- | ----- |
add model | add with status RELEASED | RELEASED
add model | none | RELEASED
existing model | add metadata.json with status DEPRECATED | DEPRECATED
add model | existing metadata.json with status DEPRECATED | DEPRECATED
add two models to same namespace | add with status RELEASED | one model RELEASED and warning
add two models to same namespace | none | one model RELEASED (no warning yet)
delete model with status DEPRECATED  | not relevant | model is deleted in Semantic Hub 
delete model with status RELEASED | not relevant | model is still and Semantic Hub and log error response from Semantic Hub that model cannot be deleted
modify model | no addition or modification | log warning and no update of model in Semantic Hub

### other branch
On any other branch besides the main-branch the metadata.json should be ignored. This results in the following test cases: 

| Model | metadata.json | expected deployed model status |
----| ---- | ----- |
add model | none | DRAFT
add model | add metadata.json with status DEPRECATED | DRAFT
existing model | add metadata.json with status RELEASED | DRAFT
delete model | not relevant | delete model from Semantic Hub




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
# Upload Action
This action expects an JSON file with models to upload and URNs to delete in the current root directory. Based on this information, the action synchronizes the changes in the Git repository to a Semantic Hub instance. The action thus further requires the URL to the Semantic Hub instance and a token to access this instance as input paramters. 

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




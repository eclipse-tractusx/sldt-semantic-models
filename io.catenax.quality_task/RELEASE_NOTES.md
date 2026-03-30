# Changelog
All notable changes to this model will be documented in this file.

## [Purpose of this model]
This aspect model was created in the Catena-X use case quality. The purpose of this aspect model is to describe a quality task between companies.

## [3.0.0] - 2025-05-13
### Added
- model feature additionalInformation key:value pair added

### Changed
- to reduce redundancies in modelling some properties are now used form share quality core model
- listOfQualityTasks from version 2.0.0 has changed to qualityTasks only
- qualityTasks_creationDate is now mandatory
- qualityTasks_companies_name now mandatory

### Removed


## [2.0.0] - 2024-01-22
### Added
- metaInformation added to root entity: Gives data consumer necessary information how data provider created this data set
- integration of shared UUID characteristic and RegEx for the vehicle Catena-X identifier
- integration of the shared BPNL trait
- integration of shared e-Mail trait
- using of Catena-X UUID as qualityTaskId

### Changed
- qTask aspect model is now able to held also lists of qTasks
- changed all properties to optional except one unique identifier per entity
- change property cxbpn cxBusinessPartnerNumber

### Removed

## [1.0.0] - 2022-12-13
### Added
- initial version of this model

### Changed
n/a

### Removed


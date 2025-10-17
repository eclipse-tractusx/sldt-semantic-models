# Changelog
All notable changes to this model will be documented in this file.

## [Unreleased]

## [3.0.0] - 2025-07-07
A conversion table from previous version 2.0.0 to 3.0.0 of this model is provided with the updated KIT Quality Management for CX release Saturn.

### Added
- model feature additionalInformation key:value pair added

### Changed
- to reduce redundancies in modelling some properties are now used form share quality core model
- using parts definition from shared quality core model (via samm:extends) to unify ECU properties 
- at least one primary identifier per entity is now mandatory
- diagnosticSessions_anonymizedVIN, diagnosticSessions_sessionStart, diagnosticSessions_qualityTaskId are now mandatory properties

### Removed
- diagnosticSessions_ecuList_hwPartNumber
 redundant property to diagnosticSessions_ecus_partNumber




## [2.0.0] - 2024-01-29
### Added
- metaInformation property added to root entity
- integration of the shared UUID characteristic and RegEx for Catena-X identifiers
- introducing new characteristic for unique identifiers
- end date of a diagnostic session added
- procedures entity added to support failure-tree-based analysis in the workshop: Procedures can have sub-procedures could also be linked to ecuList
- for Ecus: calibration and variant coding properties

### Changed
- changed all properties to optional except unique identifier per entity
- Clear structure: session has ecuList as child, ecuList has dtcList as child, dtcList has envConditionList as child

### Removed
- vehicle entity: Properties now located one level up on DiagnosticSession
- eventList: Removed completely - instead procedures list was introduced

## [1.0.0] - 2022-12-13 -> deprecated
### Added
- initial version of this model

### Changed
n/a

### Removed


# Changelog
All notable changes to this model will be documented in this file.

## [Unreleased]
- Version 2.0.0 of model is deprecated. It has a wrong regex for BPNS validation from the old shared model for BPNS trait.

## [3.0.0] - 2025-05-05
A conversion table from previous version 2.1.0 to 3.0.0 of this model is provided with the updated KIT Quality Management for CX release Saturn.

### Added

### Changed
- to reduce redundancies in modelling some properties are now used form share quality core model
- listOfManufacturedParts
 from version 2.1.0 has changed to manufacturedParts only
- using parts definition from shared quality core model (via samm:extends) to unify manufacturedParts properties 
- at least one primary identifier per entity is now mandatory
- manufacturedParts_partName and manufacturedParts_plant_plantIdentifier are now mandatory properties

### Removed
- listOfManufacturedParts_parentPartNumber,listOfManufacturedParts_parentSerialNumber,listOfManufacturedParts_productionLine


## [2.1.0] - 2024-02-19
### Added
- optional properties added: parentSerialNumber and parentPartNumber

### Changed
- reference to shared aspect model for BPNS was changed to latest version

### Removed

## [2.0.0] - 2024-01-29 -> deprecated
### Added
- metaInformation property added to root entity
- integration of the shared UUID characteristic and RegEx for Catena-X identifiers
- integration of BPNS as additional plant identifier using BPNS trait from shared aspect model
- introducing new characteristic for unique identifiers

### Changed
- changed all properties to optional except one unique identifier per entity

### Removed
- Manufacturing entity -> all properties are now located on ManufacturedPart entity

## [1.0.0] - 2022-12-13 -> deprecated
### Added
- initial version of this model

### Changed
n/a

### Removed


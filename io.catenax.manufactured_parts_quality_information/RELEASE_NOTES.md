# Changelog
All notable changes to this model will be documented in this file.

## [Unreleased]
- Version 2.0.0 of model is deprecated. It has a wrong regex for BPNS validation from the old shared model for BPNS trait.

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


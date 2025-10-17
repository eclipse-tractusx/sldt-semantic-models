# Changelog
All notable changes to this model will be documented in this file.

## [Unreleased]

## [3.0.0] - 2025-07-07
A conversion table from previous version 2.0.0 to 3.0.0 of this model is provided with the updated KIT Quality Management for CX release Saturn.

### Added
- model feature additionalInformation key:value pair added

### Changed
- to reduce redundancies in modelling some properties are now used form share quality core model
- listOfClaims from version 2.0.0 has changed to claims only
- using parts definition from shared quality core model (via samm:extends) to unify part's properties for claimed parts and spare parts
- at least one primary identifier per entity is now mandatory
- claims_anonymizedVIN, claims_countryCode, claims_qualityTaskId are now mandatory properties

### Removed
- listOfClaims_repairCountryCode: redundant property

## [2.0.0] - 2024-01-29
### Added
- metaInformation property added to root entity
- integration of the shared UUID characteristic and RegEx for Catena-X identifiers
- introducing new characteristic for unique identifiers

### Changed
- changed all properties to optional except one unique identifier per entity
- spare part entity is now child of a claimed part
- properties of ClaimPart and SparePart entity are aligned with ManufacturedQualityPartInformation aspect model

### Removed
- Vehicle entity -> all properties are now located on claim entity

## [1.0.0] - 2022-12-13 -> deprecated
### Added
- initial version of this model

### Changed
n/a

### Removed


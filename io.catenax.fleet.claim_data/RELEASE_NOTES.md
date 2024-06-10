# Changelog
All notable changes to this model will be documented in this file.

## [Unreleased]

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


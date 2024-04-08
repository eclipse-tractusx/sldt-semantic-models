# Changelog
All notable changes to this model will be documented in this file.

## [3.0.0] 2024-02-05
### Added
- Integration of the new shared PartClassification 1.0.0 aspect model as child-property of the PartTypeInformation
- Added possibility to add date information excluding time
- Include additional RegEx values for the local identifier key

### Changed
- Change (shared) partSiteInformation to be a child-property of the manufacturerInformation

## [2.0.0] 2023-11-30
### Added
- integration of the sites property and its childtree of the shared PartSiteInformationAsBuilt (1.0.0) aspect model as optional content
- integration of the shared UUID characteristic and RegEx for the catenaXId property

### Changed
- migrated current aspect model from BAMM to SAMM

### Removed
- removed existing characteristic and RegEx of the catenaXId property and replaced it with content of the shared UUID aspect model (see added information)

## [1.0.0]
### Added
- initial version of model

### Changed
n/a

### Removed

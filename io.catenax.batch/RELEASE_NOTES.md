# Changelog
All notable changes to this model will be documented in this file.

## [3.0.0] 2024-02-05
### Added
- Integration of the new shared PartClassification 1.0.0 aspect model as child-property of the PartTypeInformation
- Added possibility to add date information excluding time
- Include additional RegEx values for the local identifier key

### Changed
- Change (shared) partSiteInformation to be a child-property of the manufacturerInformation

## [2.0.1] 2023-12-04
### Added
- integration of the sites property and its childtree of the shared PartSiteInformationAsBuilt (1.0.0) aspect model as optional content
- integration of the shared UUID characteristic and RegEx for the catenaXId property

### Changed
- n/a

### Removed
- removed existing characteristic and RegEx of the catenaXId property and replaced it with content of the shared UUID aspect model (see added information)

## [2.0.0] - 2023-09-04
### Added
- added KeyRegularExpression

### Changed
- changed description of KeyCharacteristic

### Removed
- properties customerId and nameAtCustomer

## [1.0.2] - 2022-11-23
### Added
- initial model
- fix in example value
- fix regex

### Changed
n/a

### Removed


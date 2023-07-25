# Changelog
All notable changes to this model will be documented in this file.

## [Unreleased]

## [2.0.0]
### Added
- added `customers` to reflect that the relation to parent items is not known at all times. Instead a reference to the customer is made.
- restructured `parentParts` to be enclosed 
- added optional `businessPartner` to enable decentralized Digital Twin registry


### Changed
- renamed `parentParts` to `parentItems`
- made `parentItems` optional to reflect that parent items are not known at all times
- fixed example value for `measurementUnit`
- fixed link to samm unit catalogue for `measurementUnit`
- renamed `parentCatenaXId` to `catenaXId`
- improved some descriptions to reflect change from `part` to `item`
- generally improved some descriptions

### Removed

## [1.0.1] - 2022-08-11
### Added
- initial version of model
- small bugfix

### Changed
n/a

### Removed


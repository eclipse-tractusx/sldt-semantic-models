# Changelog
All notable changes to this model will be documented in this file.

## [3.0.0] - 2024-02-26
### Changed
- changed `parentItems` property to be a mandatory child of the `SingleLevelUsageAsBuilt` aspect property instead of a child of the `customers` property
- changed `customers` property to be a list of BPNL
- replaced the `quantityNumber` and `measurementUnit` properties with the `itemUnit` and `quantityValue` properties of the shared quantity 2.0.0 aspect model
- replaced the whole `CatenaXIdTraitCharacteristic` and its childs with the `UuidV4Trait` of the shared uuid 2.0.0 aspect model
- replaced the whole `BpnTrait` and its childs with the `BpnlTrait` of the shared business_partner_number 2.0.0 aspect model
- description of some objects were adjusted


## [2.0.0] - 2023-09-01
### Added
- added `customers` to reflect that the relation to parent items is not known at all times. Instead a reference to the customer is made.
- restructured `parentParts` to be enclosed 
- added mandatory `businessPartner` to enable decentralized Digital Twin registry


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

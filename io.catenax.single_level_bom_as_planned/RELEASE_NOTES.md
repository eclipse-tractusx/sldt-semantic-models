# Changelog
All notable changes to this model will be documented in this file.

## [3.0.0] - 2024-02-26
### Changed
- replaced the `quantityNumber` and `measurementUnit` properties with the `itemUnit` and `quantityValue` properties of the shared quantity 2.0.0 aspect model
- replaced the whole `CatenaXIdTraitCharacteristic` and its childs with the `UuidV4Trait` of the shared uuid 2.0.0 aspect model
- replaced the whole `BpnTrait` and its childs with the `BpnlTrait` of the shared business_partner_number 2.0.0 aspect model
- replaced the existing `Timestamp` characteristics of `validFrom` and `validTo` with a new `DateTimeTrait`, to permit date information excluding time
- description of some objects were adjusted

## [2.0.0] - 2023-09-01
### Added
- mandatory `businessPartner` to each child item

### Changed
- changed `childCatenaXId` to `catenaXId`
- changed `childParts` to `childItems`
- changed several descriptions to use `item` instead of `part` where applicable
- updated reference for SAMM Unit Catalog to a more readable one

### Removed
n/a

## [1.1.0]
### Added
- optional validity period for child-parent relation

### Changed
- descriptions to more explicitly describe handling of versions of child parts
- updated reference for SAMM Unit Catalog to a more stable one
- all characteristics, entities, and constraints now have proper names, preferred names and descriptions
- fixed some typos in preferred names and descriptions

### Removed

## [1.0.1] - 2022-08-11
### Added
- initial version of model
- small bugfix

### Changed
n/a

### Removed

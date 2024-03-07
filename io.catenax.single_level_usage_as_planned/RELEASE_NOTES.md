## Changelog
All notable changes to this model will be documented in this file.

## [2.0.0] - 2024-02-26
### Added
- added new `customers` property as child of the `SingleLevelUsageAsPlanned` aspect property including its `ListOfCustomersCharactersistics` and `Customer` entity
- added new `businessPartner` property with its `BpnlTrait` of the shared business_partner_number 2.0.0 aspect model
- added new links from the `customers` entity to the `businesspartner`, `createdOn` and `lastModifiedOn` properties

### Changed
- changed `parentCatenaXId` to `catenaXId` to be conform with the data chain template
- renamed `parentParts` property to be `parentItems`
- changed `parentItems` property to be a mandatory child of the `SingleLevelUsageBuilt` aspect property instead of a child of the `customers` property
- replaced the `quantityNumber` and `measurementUnit` properties with the `itemUnit` and `quantityValue` properties of the shared quantity 2.0.0 aspect model
- replaced the existing `Timestamp` characteristics of `validFrom` and `validTo` with a new `DateTimeTrait`, to permit date information excluding time
- replaced the whole `CatenaXIdTraitCharacteristi`c and its childs with the `UuidV4Trait` of the shared uuid 2.0.0 aspect model
- description of some objects were adjusted


## [1.1.0]
### Added
- optional validity period for child-parent relation

### Changed
- descriptions to more explicitly describe handling of versions of child parts
- updated reference for SAMM Unit Catalog to a more stable one
- all characteristics, entities, and constraints now have proper names, preferred names and descriptions
- fixed some typos in preferred names and descriptions


### Removed

## [1.0.0] - 2022-12-07
### Added
- initial model

### Changed
n/a

### Removed

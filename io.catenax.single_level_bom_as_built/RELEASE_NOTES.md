# Changelog
All notable changes to this model will be documented in this file.

## [3.0.0] - 2024-02-26
### Changed
- replaced the `quantityNumber` and `measurementUnit` properties with the `itemUnit` and `quantityValue` properties of the shared quantity 2.0.0 aspect model
- replaced the whole `CatenaXIdTraitCharacteristic` and its childs with the `UuidV4Trait` of the shared uuid 2.0.0 aspect model
- replaced the whole `BpnTrait` and its childs with the `BpnlTrait` of the shared business_partner_number 2.0.0 aspect model
- description of some objects were adjusted

## [2.0.0] - 25.09.2023
### Added
- property called hasAlternative
- Boolean characteristic

### Changed
- Description of the main property 'SingleLevelBomAsBuil' was adapted to the new requirements of the model

### Removed
- 


## [1.0.0]
### Added
- renamed model from `io.catenax.assembly_part_relationship:1.1.1#AssemblyPartRelationship`
- optional business partner reference (BPNL) for each child item

### Changed
- changed several descriptions due to aspect renaming
- changed `childCatenaXId` to `catenaXId`
- changed `childParts` to `childItems`
- changed several descriptions to use `item` instead of `part` where applicable
- fixed camelCase for `NumberOfObjects` characteristic

### Removed
- removed lifecycle context property from child item


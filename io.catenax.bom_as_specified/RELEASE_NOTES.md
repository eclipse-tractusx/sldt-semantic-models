# Changelog
All notable changes to this model will be documented in this file.

## [2.0.0] - 2023-06-30
### Added

### Changed

### Removed
- Deprecation of model 2.0.0 due to its new name which requires another namespace. Hence, the 2.0.0 model can be found in the new namespace io.catenax.single_level_bom_as_specified as version 1.0.0

## [2.0.0] - 2023-04-24
### Added
- added new properties: createdOn, lastModifiedOn

### Changed
- changed model name from BomAsSpecified to SingleLevelBomAsSpecified for consistency reasons with other Bom models
- changed existing properties: identifier -> catenaXId, item -> childParts
- minor adjustments of exemplary values to reflect current state of the model

### Removed
- removed non-needed properties: index, quantity


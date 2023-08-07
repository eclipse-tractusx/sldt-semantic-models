# Changelog
All notable changes to this model will be documented in this file.

## [Unreleased]

## [1.0.0] - 2023-08-07
### Added
- added new properties: partGeometry (represting the side a part belongs to, e.g. left or right) and manufacturerId (BPN of the manufacturer)

### Changed

### Removed

## [1.0.0] - 2023-06-30
### Added
- added new properties: createdOn, lastModifiedOn

### Changed
- changed model name from BomAsSpecified to SingleLevelBomAsSpecified for consistency reasons with other Bom models
- moved new model to a new namespace 
- changed existing properties: identifier -> catenaXId, item -> childParts
- minor adjustments of exemplary values to reflect current state of the model

### Removed
- removed non-needed properties: index, quantity
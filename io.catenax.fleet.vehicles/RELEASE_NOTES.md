# Changelog
All notable changes to this model will be documented in this file.

## [Unreleased]
- Version 2.0.0 of model is deprecated. It has a wrong regex for BPNS validation from the old shared model for BPNS trait.

## [3.0.0] - 2024-04-29
### Added
- Added optional property components: to be able to store focus components in the semantic model as requested by BMW

### Changed


### Removed

## [2.1.0] - 2024-02-19 -> deprecated
### Added

### Changed
- reference to shared aspect model for BPNS was changed to latest version

### Removed


## [2.0.0] - 2024-01-22 -> deprecated
### Added
- metaInformation added to root entity: Gives data consumer necessary information how data provider created this data set
- integration of shared UUID characteristic and RegEx for the vehicle Catena-X identifier
- introducing new characteristic to mark unique identifiers
- integration of separate aspect model Vehicle.ProductDescription:3.0.0 into this model to do necessary adaptions that were decided in Catena-X Quality use case team: Most of the properties should be set to optional

### Changed
- changed all properties to optional except one unique identifier per entity
- properties that were linked to OEM entity are now one level up 
- fuel type property now linked to engine property
- entity production was renamed to productionPlant to increase clarity

### Removed
- link to Vehicle.ProductDescription:3.0.0: Previous linked model now integrated and adapted
Streamlining of aspect model:
- remove of body entity + body properties as it was never used
- remove of all KBA properties: Focusing on NHTSA properties only 
- remove of oem entity: Properties now located on vehicle level
- remove of fuel entity: Properties now located on vehicle and engines level
- remove of sale entity: Properties now located on vehicle level
- remove of production entity: Properties now located on vehicle level

## [1.0.0] - 2023-05-15 -> deprecated
### Added
- initial version of this model

### Changed
n/a

### Removed


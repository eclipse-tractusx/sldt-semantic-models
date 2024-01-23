# Changelog
All notable changes to this model will be documented in this file.

## [Purpose of this model]
This aspect model was created in the Catena-X use case quality. The purpose of this aspect model is to transfer general information of a list/fleet of vehicles - primarily how the vehicles are equipped, when they were built and which engines are installed.

## [2.0.0] - 2024-01-22
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

## [1.0.0] - 2023-05-15
### Added
- initial version of this model

### Changed
n/a

### Removed


# Changelog
All notable changes to this model will be documented in this file.

## [Unreleased]
- Version 1.0.0 is now set to deprecated: Some important attributes were missing. Use version 2.0.0 instead

## [3.0.0] - 2024-01-22
### Added
- metaInformation property added to root entity
- integration of the shared UUID characteristic and RegEx for the vehicle Catena-X identifie
- introducing new characteristic for unique identifiers
- introduced new prarent properties that could be used for Tier-n collaboration

### Changed
- changed all properties to optional except one unique identifier per entity

### Removed
- oem properties -> replaced by parent properties

## [2.0.0] - 2023-06-23 -> deprecated
### Added
- property manufacturerAnalysisID: ID of internal system from manufacturer
- property customerAnalysisID: ID of internal system from customer
- property anonymizedVin to match PartsAnalyses data with Vehilce.ProductDescription data
- additionalInformation: a key/value list to add additional data

### Changed
- catenaXIdentifier renamed to catenaXPartId: To emphasize that this is a CX part ID (not CX vehicle ID)
- customerPartIdentifier renamed to customerPartNumber: to avoid confusion because this property is not unique 
- manufacturerPartIdentifier renamed to manufacturerPartNumber: to avoid confusion because this property is not unique
- nameAtManufacturer to manufacturerPartName: All properties from manufacturer have no the prefix manufacturer for better readability

### Removed

## [1.0.0] - 2022-12-13 -> deprecated
### Added
- initial version of this model

### Changed
n/a

### Removed
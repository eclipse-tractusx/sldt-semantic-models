# Changelog
All notable changes to this model will be documented in this file.

## [5.0.0] - 2024-05-21
### Changed
- structure and pattern below chemicalName and chemicalId changed for materials
- header example value made more generic
- codeKey is now open and no longer an enumeration
- description text added for packaging sustainability information in the attribute structure for sources

### Added
- lastModification in metadata (optional)
- otherOperatorsId in operation (optional)
- otherOperatorsRole in operation (optional)
- purpose attribute added in commercial

### Deleted
- codeDescription deleted due to duplication with codeKey

## [4.0.0] - 2024-02-19
### Changed
- Either-or possibilities are deleted in order to only allow one possible verifiable input
- Changed descriptions to reference the latest regulation from January 9th, 2024.
- Changed general structure
- Changed structure for some document links to reuse existing structure
- Changed the way how to refer to serial, batch and model information through shared aspects
- Changed reference for part classification
- Attributes made optional (volume, grossVolume)
- Changed structure for critical raw materials
- Changed structure for sustainability attributes


### Added
- New attribute structure for hazardous classification of material (mandatory)
- New attribute backupReference
- New attribute registrationIdentifier
- Added constraints to allow only positive values and percentages
- New attribute structure for material footprint (optional)
- New attribute generalPerformanceClass (optional)
- New attribute repairabilityScore (optional)
- New attribute durabilityScore (optional)



## [3.0.0] - 2023-12-04
### Added
General
- payload names are added where missing and needed
- all company identifiers can now be a company name, full address and contact or a simple identifier with a type
- all site identifiers can now be a name and full address or a simple identifier

Metadata
- passportIdentifier added which can be a UUID in the case of catena-X

Characteristics
- physical dimensions linked to shared.quantity

Sustainability
- state has a more defined enumeration
- carbon and environmental footprint have new properties "performance class", "manufacturing plant" and "declaration"
- renewable and recycled content are now identified trough a share

Identification
- a list of identifiers can be provided

Operation
- manufacturing date is mandatory

Handling
- spare part producers changed to spare part sources
- hazardClass optional added


## [2.0.0] - 2023-08-28
### Added
- converted to SAMM 2.0.0
- This data model is based on the proposed Ecodesign Regulation ("Proposal for a REGULATION OF THE EUROPEAN PARLIAMENT AND OF THE COUNCIL establishing a framework for setting ecodesign requirements for sustainable products and repealing Directive 2009/125/EC" ESPR from March 30th, 2022 with some additional data points which can be found in the adopted Amendments from July 12th 2023 (Amendments adopted by the European Parliament on 12 July 2023 on the proposal for a regulation of the European Parliament and of the Council establishing a framework for setting eco-design requirements for sustainable products and repealing Directive 2009/125/EC)


## [1.0.0] - 2023-07-10
### Added
- model renamed and created

### Changed
n/a

### Removed
n/a



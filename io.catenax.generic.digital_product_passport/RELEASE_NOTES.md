# Changelog
All notable changes to this model will be documented in this file.

## [3.0.0] - 2023-12-11
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
- carbon footprint is separate and anymore a list
- carbon and environmental footprint have new properties "performance class", "manufacturing plant" and "declaration"
- renewable and recycled content are now identified trough a share
- critical material is now a list with names and percentages

Typology
- class is now mandatory

Identification
- a list of identifiers can be provided

Operation
- manufacturing date is mandatory

Handling
- spare parts are now mandatory and the list of suppliers are connected to the spare parts
- hazardClass added


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



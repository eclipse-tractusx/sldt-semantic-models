# Changelog

All notable changes to this model will be documented in this file.

## [4.0.0] xx.xx.2026
### Removed
- businessPartnerNumber (root) - It is redundant; certificate holder is now derived from:  certifiedLocations[locationRole="MAIN_LOCATION"].bpnl
- enclosedSites + enclosedSiteBpn - Replaced by certifiedLocations

### Added
- certifiedLocations
- certificateId
- changeCounter
- locationRole
- version (document)
- language (document)

### Changed
- trustLevel - New enumeration low / medium / high per CCM KIT Trust Level concept
- documentId  - casing fixed to lowerCamelCase per Tractus-X naming conventions;
- DocumentEntity can be a list of documents
- certificateVersion changed to certificateTypeVersion

## [3.1.0] 24.03.2025

### Changed
- EnclosedSiteBpn property accepts either BPNA or BPNS. (previous version was only BPNS)

## [3.0.0] 16.12.2024

### Changed
- New data attributes added for entity Document: creationDate, contentType and contentBase64
- New data attributes for entity Issuer: issuerName and issuerBpn.
- issuerBpn changed to optional
- fixed typos, added missing descriptions 

## [2.0.0] 29.08.2024

### Changed

- Updated enclosedSiteBpn property to accept both site and address type for Business Partner Certificate.
- Updated validator object. Now validator object is optional including validatorName and validatorBpn attributes, for increased flexibility in validation details.

## [1.0.0] 11.03.2024

- initial version of the aspect model for Business Partner Certificate.

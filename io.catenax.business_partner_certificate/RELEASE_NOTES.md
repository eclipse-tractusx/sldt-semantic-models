# Changelog

All notable changes to this model will be documented in this file.

## [4.0.0] r27.03
### Removed
- businessPartnerNumber (root) - Removed due to redundancy. The certificate holder is now derived from: certifiedLocations[locationRole="Certificate Holder"].bpnl
- enclosedSites and enclosedSiteBpn - Replaced by the new certifiedLocations structure.
- areaOfApplication (root)
- contentBase64

### Added
- certifiedLocations
- certificateId
- iatfCertificateNumber
- revision
- certificateHolder
- language (document-level)

### Changed
- trustLevel - Updated to a new enumeration: low, medium, high, aligned with the CCM KIT Trust Level concept.
- documentId - Renamed to follow lowerCamelCase in accordance with Tractus-X naming conventions.
- DocumentEntity - Now supports multiple documents (list instead of single instance)
- certificateVersion → certificateTypeVersion - Renamed for improved clarity and consistency.
- validatorBpn → validatorBpnl
- issuerBpn → issuerBpnl

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

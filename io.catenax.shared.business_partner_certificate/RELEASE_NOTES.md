# Changelog

All notable changes to this model will be documented in this file.

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

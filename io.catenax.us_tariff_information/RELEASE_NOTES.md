# Changelog
All notable changes to this model will be documented in this file.

## [2.0.0] - 2025-12-16
### Added
- partName
- partOriginCountry
- partValue
- active

### Changed
- htsCode --> customClassificationCode
- htsCodingSystem --> customClassificationCodingSystem
- value --> partValue.amount
- currency --> partValue.currency
- processingCountry uses 3 letter country code instead of 2 letter code
- originWeight --> kg is unit by default
- partWeight --> kg is unit by default
- materialClassification --> is now imported from a shared model --> requires three levels of classification instead of one
- ProcessingTypeCharacteristic --> fixed typo in values (Pourring --> Pouring)
- originCountry --> materialOriginCountry
- certificateId --> documentID

### Removed
- processing.successor


## [1.0.0] - 2025-07-17
### Added
- initial model

### Changed
n/a

### Removed
n/a

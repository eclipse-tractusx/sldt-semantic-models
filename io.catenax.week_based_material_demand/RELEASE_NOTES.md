# Changelog

All notable changes to this model will be documented in this file.

## [3.0.0] - 2024-03-11

### Added

- added `materialDemandIsInactive` as mandatory flag in aspect model header
- added `materialGlobalAssetId` as optional property in aspect model header
- added `unitOfMeasureIsOmitted` as mandatory property in aspect model header
- added `unit:secondUnitOfTime`, `unit:minuteUnitOfTime`, `unit:hourUnitOfTime` and `unit:cycle` to list of unit of measure for load information

### Changed

- migrated from SAMM version `2.0.0` to `2.1.0`
- unitOfMeasure uses value list of shared aspect `urn:samm:io.catenax.shared.quantity` now. Units are now represented as reference units instead of common codes
- made `unitOfMeasure` optional
- using external references of `urn:samm:io.catenax.shared.business_partner_number`, `urn:samm:io.catenax.shared.quantity` and `urn:samm:io.catenax.shared.uuid` of version `2.0.0` for respective property definitions
- changed property name of `calendarWeeks` to `pointInTime`

### Removed

- removed 'blank' value in list of `unitOfMeasure`. `unitOfMeasureIsOmitted` flag taking over the function of the 'blank' value

## [2.0.0]

### Changed

- migrated from BAMM to SAMM

## [1.0.1] - 2023-05-10

### Changed

- Changed description for property `changedAt`

## [1.0.0]

- initial version of the aspect model for week based material demands

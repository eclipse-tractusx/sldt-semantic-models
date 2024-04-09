# Changelog

All notable changes to this model will be documented in this file.

## [3.0.0] - 2024-03-11

### Added

- added `capacityGroupIsInactive` as mandatory flag in aspect model header
- added `demandVolatilityParameters` as optional entity in aspect model header
- added `agreedCapacity` as optional property in capacities set

### Changed

- migrated from SAMM version `2.0.0` to `2.1.0`
- updated external references of `urn:samm:io.catenax.shared.business_partner_number`, `urn:samm:io.catenax.shared.quantity` and `urn:samm:io.catenax.shared.uuid` to version `2.0.0`

## [2.0.0] - 2023-11-07

### Added

- `linkedCapacityGroups` added as optional property in aspect model header
- added `loadFactor` as optional property in LinkedDemandSeries entity
- added `unit:secondUnitOfTime`, `unit:minuteUnitOfTime`, `unit:hourUnitOfTime` and `unit:cycle` to list of unit of measure for load information
- added `deltaProductionResult` as optional property in Capacity entity
- added `unitOfMeasureIsOmitted` as mandatory property in aspect model header

### Changed

- made `linkedDemandSeries` property optional
- made `capacities` property optional
- `unitOfMeasure` uses value list of shared aspect Quantity now. Units are now represented as reference units instead of common codes
- changed property name of `calendarWeeks` to `pointInTime`
- migrated from BAMM to SAMM namespace

### Removed

- removed `blank` value in list of `unitOfMeasure`. `unitOfMeasureIsOmitted` flag taking over the function of the `blank` value

## [1.0.1] - 2023-05-10

### Changed

- Changed description for property `changedAt`

## [1.0.0]

- initial version of the aspect model for week-based capacity groups

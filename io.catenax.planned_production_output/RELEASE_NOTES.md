# Changelog
All notable changes to this model will be documented in this file.

## [2.0.0] - 2024-02-19
### Added
n/a

### Changed
- Update Collections to Set for stronger semantics
  - PositionsCollection -> PositionsSet
  - AllocatedPlannedProductionOutputCollection -> AllocatedPlannedProductionOutputSet
- lastUpdatedOnDateTime
  - move from position to AllocatedPlannedProductionOutput
  - use samm datatype instead of custom Characteristic
- estimatedTimeOfCompletion -> use samm datatype instead of custom Characteristic
- updated dependencies
  - io.catenax.shared.uuid
  - io.catenax.shared.quantity
  - io.catenax.shared.business_partner_number
- migrated samm version from 2.0.0 to 2.1.0
- updated materialGlobalAssetId description to point to part type twin
- make materialGlobalAssetId mandatory

### Removed
- Harmonization for Industry Core
  - materialNumberSupplier
  - materialNumberCustomer

## [1.0.0] - 2023-11-20
### Added
- initial model


# Changelog
All notable changes to this model will be documented in this file.

## [1.0.0] - 2024-02-26
### Added
- initial model adjusted based on io.catenax.material_demand:1.0.0
  - removed all material related information except for materialGlobalAssetId
  - removed demandId
  - replaced unitOfMeasure and demand by io.catenax.shared.quantity:2.0.0
  - migrated to samm 2.1.0
  - removed unitOfMeasureIsOmmitted

### Changed
- compared to io.catenax.material_demand:1.0.0
  - renamed expectedSupplierLocation to expectedSupplierLocationBpns
  - renamed customerLocation to customerLocationBpns
  - replaced pointInTime by day
  - moved changedAt to DemandSeries and renamed to lastUpdatedOn including semanticxs

### Removed
- compared to io.catenax.material_demand:1.0.0
  - removed all material related information except for materialGlobalAssetId (materialDescriptionCustomer, materialNumberSupplier, materialNumberCustomer)
  - removed demandId
  - removed unitOfMeasureIsOmmitted
  - removed demandRate and updated semantics
  - removed supplier and customer

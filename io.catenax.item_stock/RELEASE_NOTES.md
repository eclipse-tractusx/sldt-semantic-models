# Changelog
All notable changes to this model will be documented in this file.

## [2.0.0] - 2024-02-19
### Added
n/a

### Changed
- Update Collections to Set for stronger semantics
  - PositionsCollection -> PositionsSet
  - AllocatedStockCollection -> AllocatedStockSet
- lastUpdatedOnDateTime
  - move from position to allocatedStock
  - use samm datatype instead of custom Characteristic
  - fixed semantics from supplier specific, to more generic partner specific
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
initial model as update of product stock model
- updated model to also cover customer side
- renamed product stock to item stock (aspect)
- renamed materialNumberCatena-X to materialGlobalAssetId for agnostic digital twin usage.
- usage of shared aspect
  - for uuid for materialGlobalAssetId
  - for Quantity characteristic
  - for bpn for BPNS, L, A information
- positions for customer side stock MAY NOT contain order position references
- added property direction to indicate OUTBOUND (formerly known as product stock) and INBOUND (material stock)
- replaced property locationId of either type BPNS or BPNA by properties stockLocationBPNS and stockLocationBPNA
- renamed Characteristic for MaterialNumber to MaterialNumberCharacteristic
- updated lastUpdatedOn to be DateTime instead of Date. 

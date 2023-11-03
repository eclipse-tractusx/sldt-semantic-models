# Changelog
All notable changes to this model will be documented in this file.

## [2.0.0] - 2023-10-09
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

## [1.0.0] - 2023-06-05
### Added
- initial model


# Changelog

All notable changes to this model will be documented in this file.

### [3.0.0] - 2024-01-30
- migrated from samm 2.0.0 to samm 2.1.0

## [2.0.0] - 2023-11-28
### Added
- add / integrate shared UUID characteristic and RegEx for the properties messageId and relatedMessageId
- add / integrate shared BPN-L characteristic and RegEx for the properties senderBpn and receiverBpn

### Changed
- fixed bug of missing connection between messageId property and the idTrait to link the UUIDv4 RegEx
- fixed bug of missing connection between relatedMessageId property and the idTrait to link the UUIDv4 RegEx
- fixed bug of missing connection between version property and the SemanticVersioningTrait to link the semVer RegEx

### Removed
- removed existing characteristic of the properties messageId and relatedMessageId and replaced it with content of shared aspect models (see added information)
- removed existing characteristic of the properties senderBpn and reveiverBpn and replaced it with content of shared aspect models (see added information)

## [1.0.0] 2023-07-31

- initial version of the aspect model for the Message Header

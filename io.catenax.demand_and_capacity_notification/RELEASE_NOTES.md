# Changelog

All notable changes to this model will be documented in this file.

## [3.0.0] - 2025-06-23

### Added

- added field `resolvingMeasureDescription`

### Changed

- `sourceNotificationId`:
  - renamed to `sourceNotificationId` and elaborated semantics
  - now is mandatory
- `relatedNotificationId`:
  - changed to be a collection (`relatedNotificationIds`)
  - added logic when a notification can be considered a related notification
- `leadingRootCauseEnumeration`: added `insolvency`
- Introduce a Set of Material Entities with `materialNumberCustomer`, `materialNumberSupplier` and `materialGlobalAssetId`
  - `materialNumberSupplier` and `materialNumberCustomer` use the `PartIdCharacterstic` from `PartTypeInformation`
  - `materialGlobalAssetId` uses the UUID characteristic directly

### Removed

## [2.0.0] - 2024-03-11

### Added

- notificationId: mandatory id for notifications
- relatedNotificationId: optional id to refer to a notification along the tiers

### Changed

- relatedSourceMessageId: renamed to sourceNotificationId and reframed semantics
- preferredName of TextLengthConstraint was CamelCase

### Removed


## [1.0.0] - 2024-02-19
### Added
- initial model

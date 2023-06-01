# Changelog
All notable changes to this model will be documented in this file.

## [Unreleased]

## [1.0.0]
### Added
- renamed model from `io.catenax.assembly_part_relationship:1.1.1#AssemblyPartRelationship`
- optional business partner reference (BPNL) for each child item

### Changed
- changed several descriptions due to aspect renaming
- changed `childCatenaXId` to `catenaXId`
- changed `childParts` to `childItems`
- changed several descriptions to use `item` instead of `part` where applicable
- fixed camelCase for `NumberOfObjects` characteristic

### Removed
- removed lifecycle context property from child item


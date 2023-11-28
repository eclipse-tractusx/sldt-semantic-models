# Changelog
All notable changes to this model will be documented in this file.

## [2.0.0] 2023-12-04
### Added
- integration of the sites property and its childtree of the shared PartSiteInformationAsBuilt (1.0.0) aspect model as optional content
- integration of the shared UUID characteristic and RegEx for the catenaXId property

### Changed
- migrated current aspect model from BAMM to SAMM

### Removed
- removed existing characteristic and RegEx of the catenaXId property and replaced it with content of the shared UUID aspect model (see added information)

## [1.0.1]
### Added
n/a

### Changed
- fixed casing in example value for `key` of `localIdentifier` to lower case

### Removed
n/a

## [1.0.0]
### Added
- renamed model from `io.catenax.serial_part_typization:2.0.0#SerialPartTypization`

### Changed
- changed several descriptions due to aspect renaming

### Removed
n/a

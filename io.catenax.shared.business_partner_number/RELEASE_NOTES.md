# Changelog
All notable changes to this model will be documented in this file.

## [2.0.0] - 2024-02-05
### Added
n/a

### Changed
- updated regexes
  - from `^BPNL[0-9]{8}[a-zA-Z0-9]{4}$` to `^BPNL[a-zA-Z0-9]{12}$`
  - semantic descriptions as checksum is not two UPPERCASE but two alphanumeric digits
- fixed typo in prefferedName of BpnlTrait


### Removed
n/a

## [1.0.0] - 2023-09-11
### Added
- initial model

### Changed
n/a

### Removed
n/a

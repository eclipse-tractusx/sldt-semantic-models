# Changelog

All notable changes to this model will be documented in this file.

## [Purpose of this model]

The Battery Pass Aspect Model is designed to enable transparent, standardized, and interoperable documentation of battery-related data across the entire lifecycle - from raw material extraction to manufacturing, usage, and end-of-life recycling. Its primary purpose is to support compliance with the EU Battery Regulation, which mandates the use of Digital Product Passports (DPPs) for batteries used in electric vehicles.

## [3.0.0] - 2025-03-21

### Changed
- Certificate of Analysis (CoA), Technical Information & Safety Data Sheets (SDS) can be included in Chemical Material Passport in structured or (less favored for legacy in) binary formats.

### Removed

## [2.0.0] - 2024-05-21

### Changed

- connection update to @prefix ext-passport: <urn:samm:io.catenax.generic.digital_product_passport:5.0.0#>
- changed safetyDocument to safetyDocumentation and changed payload name
- moved methodName together with "condition" and "description" of the method
- changed payload name from unspecific to generic on highest level

## [1.0.0] - 2024-04-22

### Added

- initial model

### Changed

n/a

### Removed


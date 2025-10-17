# Changelog

All notable changes to this model will be documented in this file.

## [Purpose of this model]

The "Chemical Material Passport" data model implements a digital product passport for chemical and intermediate products.  It addresses the description of raw materials and (chemical) products, the starting point for essential automotive components and the processing of the like. The Chemical Material Passport is intended to summarize all relevant information as required by regulation, in particular the EU Ecodesign Regulation (ESPR) but also enabling partners in the value chain to exchange information about this material in digital formats, including safety data sheets, certificates of analysis and other data.

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


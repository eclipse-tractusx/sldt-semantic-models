# Changelog

All notable changes to this model will be documented in this file.

## [3.0.0] 26.09

### Added
- added optional property _attachmentUrl_ (xsd:anyURI) to the measurement object to reference related artifacts, e.g. images, instead of embedding links in the description text
- added enumeration _MeasurementTypeEnumeration_ with the values simpleMeasurement, functionalMeasurement and qualitativeMeasurement

### Changed
- renamed property _manufacturerId_ to _manufacturerBpn_ and changed its characteristic from BpnlTrait to AnyBpnCharacteristic to allow BPNL, BPNS or BPNA
- updated reference to the shared business partner number model from 2.0.0 to 3.0.0
- changed property _measurementType_ from optional free text to mandatory, constrained to _MeasurementTypeEnumeration_
- adapted preferred names and descriptions of a few properties to be more understandable

### Removed
- removed property _revisionIndex_, as part-instance information is carried by the digital twin and the Industry Core submodels
- removed properties _localIdentifiers_ and _customerPartId_ (and the reference to io.catenax.serial_part) for the same reason

## [2.0.0] 2025-04-07

### Changed
- changed current datatype of the property _value_ from float to string
- adapted description of a few properties to be more understandable
- adapted the exampleValue of a few properties to be more understandable

## [1.0.0] 2024-12-16

### Added

- added data model for measurement results of special characteristics

# Changelog

All notable changes to this model will be documented in this file.

## [7.0.0] R26.03

### Added

- new attribute "specVersion"
- adding applicability field before the attribute "predecessor"
- new attribute "economicOperatorNames"
- new attribute "economicOperatorContact"
- new attribute "economicOperatorAddress"
- new attribute "codeDescription" 
- new attribute "productImages" 
- new attribute "facilityAddress"
- new attribute "manufacturerNames"
- new attribute "manufacturerContact"
- new attribute "manufacturerAddress"
- new attribute "importerNames"
- new attribute "importerContact"
- new attribute "importerAddress"
- new subsection with applicability field extendedProducerResponsibilityScheme"
- new attribute "collectionPointIdentification"
- new attribute "collectionPointAddress"
- new attribute "territoriesOfApplication"
- new attribute "symbolsOfExtendedProducerResponsibilityScheme"
- new attribute "otherOperatorNames"
- new attribute "otherOperatorContact"
- new attribute "otherOperatorAddress"
- new attribute "sparePartProviderAddress"
- new attribute "sparePartProviderContact"
- new attribute "lifeDescription"
- new subsection: itemQuantityInPackage
- new attribute "itemQuantityInPackageUnit"
- new attribute "itemQuantityInPackageValue"
- new subsection: otherCharacteristics
- new attribute "otherCharacteristicName"
- new attribute "otherCharacteristicOutcome"
- new attribute "facilityAddress"
- new subsection: reusability with applicability field
- new attribute "reuseInfo"
- new subsection:reusSystem with applicability field
- new attribute "calculationKey" for rotation
- new attribute "calculationValue" for rotation
- new attribute "calculationKey" for trip
- new attribute "calculationValue" for trip
- new attribute "facilityIdentification"
- new attribute "collectionPointIdentification"
- new attribute "collectionPointAddress"
- new attribute "symbolOfDepositAndReturnSystem"
- new attribute with applicability field:"recycleabilityPerformanceGrade"
- new subsection for components with applicability fields
- new attribute "componentName"
- new attribute "componentCode"
- new attribute "componentDescription"
- new attribute "componentSortingInformation"
- new attribute "componentLocations"
- new attribute "componentPassportIdentifier"
- new attribute "materialType"
- new attribute "materialOrigin"
- new attribute "materialPassportIdentifier"
- new attribute "materialLocations"
- new subsection concentrationRanges with minConcentration and maxConcentration  
- new subsection "declarableIngredient" with applicability field
- new attribute "declarableIngredientListDocumentId"
- new attribute "declarableIngredientListName"
- new attribute "declarableIngredientDocuments"
- new section: compliances
- new attribute "requirementName"
- new attribute "complianceCountries"
- new attribute "complianceStatement"
- new attribute "reasonsForExemption"
- new attribute "remarks"
- new attribute "complianceDocuments"

### Changed

- changing name of attribute from "status" into "passportStatus"
- changing name of attribute from "economicOperatorId" into "economicOperatorIdentification"
- changing name of attribute from "carrier" into "carrierPositions"
- changing name of attribute from "facility" into "facilityIdentification"
- changing name of attribute from "manufacturerId" into "manufacturerIdentification"
- changing name of attribute from "Id" into "importerIdentification"
- changing name of attribute from "Id" into "otherOperatorIdentification"
- changing name of attribute from "role" into otherOperatorRole"
- changing name of attribute from "Id" into "sparePartProviderIdentification"
- changing name of attribute from "unit" into "lifeUnit"
- changing name of attribute from "value" into "lifeValue"
- changing name of attribute from "type" into "lifeType"
- changing name of attribute from "status" into "productStatus"
- changing name of attribute from "value" into "footprintValue"
- changing name of attribute from "lifecycle" into "footprintLifecycle"
- changing name of attribute from "unit" into "footprintUnit"
- changing name of attribute from "type" into "footprintType"
- changing name of attribute from "facility" into "facilityIdentification"
- changing name of attribute from "Id" into "materialId"
- changing name of attribute from "name" into "materialName"
- changing name of attribute from "type" into "materialListTypeId"
- changing name of attribute from "Id" into "materialId"
- changing name of attribute from "concentration" into "concentrationValue"
- changing name of attribute from "statement" into "hazardStatement"
- changing name of attribute from "documents" into "materialDocuments"
- changing name of attribute from "class" into "hazardClass"
- changing name of attribute from "category" into "hazardCategory"
- changing name of attribute from "locations" into "substanceOfConcernLocations"
- changing name of attribute from "concentrationRange" into "substanceOfConcernConcentrationRange"

### Deleted

- delete sparePart subcategory
- delete materialComposition with applicability field

## [6.1.0] - 2025-10-06

### Added

- new attribute added: specVersion (Optional)

## [6.0.0] - 2025-04-24

### Changed

- new attribute added: language
- new attribute added: purchaseOrder
- new attribute added: recallInformation

## [5.0.0] - 2024-05-21

### Changed

- structure and pattern below chemicalName and chemicalId changed for materials
- header example value made more generic
- codeKey is now open and no longer an enumeration
- description text added for packaging sustainability information in the attribute structure for sources

### Added

- lastModification in metadata (optional)
- otherOperatorsId in operation (optional)
- otherOperatorsRole in operation (optional)
- purpose attribute added in commercial

### Deleted

- codeDescription deleted due to duplication with codeKey

## [4.0.0] - 2024-02-19

### Changed

- Either-or possibilities are deleted in order to only allow one possible verifiable input
- Changed descriptions to reference the latest regulation from January 9th, 2024.
- Changed general structure
- Changed structure for some document links to reuse existing structure
- Changed the way how to refer to serial, batch and model information through shared aspects
- Changed reference for part classification
- Attributes made optional (volume, grossVolume)
- Changed structure for critical raw materials
- Changed structure for sustainability attributes

### Added

- New attribute structure for hazardous classification of material (mandatory)
- New attribute backupReference
- New attribute registrationIdentifier
- Added constraints to allow only positive values and percentages
- New attribute structure for material footprint (optional)
- New attribute generalPerformanceClass (optional)
- New attribute repairabilityScore (optional)
- New attribute durabilityScore (optional)

## [3.0.0] - 2023-12-04

### Added

General

- payload names are added where missing and needed
- all company identifiers can now be a company name, full address and contact or a simple identifier with a type
- all site identifiers can now be a name and full address or a simple identifier

Metadata

- passportIdentifier added which can be a UUID in the case of catena-X

Characteristics

- physical dimensions linked to shared.quantity

Sustainability

- state has a more defined enumeration
- carbon and environmental footprint have new properties "performance class", "manufacturing plant" and "declaration"
- renewable and recycled content are now identified trough a share

Identification

- a list of identifiers can be provided

Operation

- manufacturing date is mandatory

Handling

- spare part producers changed to spare part sources
- hazardClass optional added

## [2.0.0] - 2023-08-28

### Added

- converted to SAMM 2.0.0
- This data model is based on the proposed Ecodesign Regulation ("Proposal for a REGULATION OF THE EUROPEAN PARLIAMENT AND OF THE COUNCIL establishing a framework for setting ecodesign requirements for sustainable products and repealing Directive 2009/125/EC" ESPR from March 30th, 2022 with some additional data points which can be found in the adopted Amendments from July 12th 2023 (Amendments adopted by the European Parliament on 12 July 2023 on the proposal for a regulation of the European Parliament and of the Council establishing a framework for setting eco-design requirements for sustainable products and repealing Directive 2009/125/EC)

## [1.0.0] - 2023-07-10

### Added

- model renamed and created

### Changed

n/a

### Removed

n/a

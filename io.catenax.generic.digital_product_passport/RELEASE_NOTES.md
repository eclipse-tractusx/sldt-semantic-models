# Changelog

All notable changes to this model will be documented in this file.

## [7.0.0] R26.03

### Added

- new attribiut "specVersion"
- adding applicability field before the attribiut "predecessor"
- new attribiut "economicOperatorNames"
- new attribiut "economicOperatorContact"
- new attribiut "economicOperatorAddress"
- new attribiute "codeDescription" 
- new attribiute "productImages" 
- new attribiute "facilityAddress"
- new attribiute "manufacturerNames"
- new attribiute "manufacturerContact"
- new attribiute "manufacturerAddress"
- new attribiute "importerNames"
- new attribiute "importerContact"
- new attribiute "importerAddress"
- new subsection with applicability field extendedProducerResponsibilityScheme"
- new attribiute "collectionPointIdentification"
- new attribiute "collectionPointAddress"
- new attribiute "teritoriesOfApllication"
- new attribiute "symbolsOfExtendedProducerResponsibilityScheme"
- new attribiute "otherOperatorNames"
- new attribiute "otherOperatorContact"
- new attribiute "otherOperatorAddress"
- new attribiute "sparePartProviderAddress"
- new attribiute "sparePartProviderContact"
- new attribiute "lifeDescription"
- new subsection: itemQuantityInPackage
- new attribiute "itemQuantityInPackageUnit"
- new attribiute "itemQuantityInPackageValue"
- new subsection: otherCharacteristics
- new attribiute "otherCharacteristicName"
- new attribiute "otherCharacteristicOutcome"
- new attribiute "facilityAddress"
- new subsection: reusability with applicability field
- new attribiute "reuseInfo"
- new subsection:reusSystem with applicability field
- new attribiute "calculationKey" for rotation
- new attribiute "calculationValue" for rotation
- new attribiute "calculationKey" for trip
- new attribiute "calculationValue" for trip
- new attribiute "facilityIdentification"
- new attribiute "collectionPointIdentification"
- new attribiute "collectionPointAddress"
- new attribiute "symbolOfDepositAndReturnSystem"
- new attribiute with aplicability field:"recycleabilityPerformanceGrade"
- new subsection for components with applicability fields
- new attribiute "componentName"
- new attribiute "componentCode"
- new attribiute "componentDescription"
- new attribiute "componentSortingInformation"
- new attribiute "componentLocations"
- new attribiute "componentPassportIdentifier"
- new attribiute "materialType"
- new attribiute "materialOrigin"
- new attribiute "materialPassportIdentifier"
- new attribiute "materialLocations"
- new subsection concentrationRanges with minConcentration and maxConcentration  
- new subsection "declarabeIngredientLists" with applicability field
- new attribiute "declarabeIngredientListDocumentId"
- new attribiute "declarabeIngredientListName"
- new attribiute "declarabeIngredientDocuments"
- new section: compliances
- new attribiute "requirementName"
- new attribiute "complianceCountries"
- new attribiute "complianceStatement"
- new attribiute "reasonsForExemption"
- new attribiute "remarks"
- new attribiute "complianceDocuments"

### Changed

- changing name of attribiut from "status" into "passportStatus"
- changing name of attribiut from "economicOperatorId" into "economicOperatorIdentification"
- changing name of attribiut from "carrier" into "carrierPositions"
- changing name of attribiut from "facility" into "facilityIdentification"
- changing name of attribiut from "manufacturerId" into "manufacturerIdentification"
- changing name of attribiut from "Id" into "importerIdentification"
- changing name of attribiut from "Id" into "otherOperatorIdentification"
- changing name of attribiut from "role" into otherOperatorRole"
- changing name of attribiut from "Id" into "sparePartProviderIdentification"
- changing name of attribiut from "unit" into "lifeUnit"
- changing name of attribiut from "value" into "lifeValue"
- changing name of attribiut from "type" into "lifeType"
- changing name of attribiut from "status" into "productStatus"
- changing name of attribiut from "value" into "footprintValue"
- changing name of attribiut from "lifecycle" into "footprintLifecycle"
- changing name of attribiut from "unit" into "footprintUnit"
- changing name of attribiut from "type" into "footprintType"
- changing name of attribiut from "facility" into "facilityIdentification"
- changing name of attribiut from "Id" into "materialId"
- changing name of attribiut from "name" into "materialName"
- changing name of attribiut from "type" into "materialListTypeId"
- changing name of attribiut from "Id" into "materialId"
- changing name of attribiut from "concentration" into "concentrationValue"
- changing name of attribiut from "statement" into hazardStatement"
- changing name of attribiut from "documents" into "materialDocuments"
- changing name of attribiut from "class" into "hazardClass"
- changing name of attribiut from "category" into "hazardCategory"
- changing name of attribiut from "locations" into "substanceOfConcernLocations"
- changing name of attribiut from "concentrationRange" into "substanceOfConcerConcentrationRange"

### Deleted

- delete sparePart subcategory
- delete materialComposition eith applicability field

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

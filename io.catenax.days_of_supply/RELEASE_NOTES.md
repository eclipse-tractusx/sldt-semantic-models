# Changelog
All notable changes to this model will be documented in this file.

## [1.0.0] - 2024-02-12
### Added
initial model adjusted from product stock model 1.0.0.
removed positions collection and refined allocatedStocks into allocatedDaysOfSupply
QuantityCharacteristic changed from Collection to SortedSet to reflect the date-daysOfSupply sorted pair
definitions for aspect model provided

## [2.0.0] - 2024-03-04
### Added
lastUpdatedOnDateTime property (samm-c:Timestamp) to describe when the data was last updated

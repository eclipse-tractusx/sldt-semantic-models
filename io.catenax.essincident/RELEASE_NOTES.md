# Changelog
All notable changes to this model will be documented in this file.

## [Unreleased]

## [4.0.0] - 2024-05-27
### Changed
- add field essIncidentModerator with trait BPNL
- set fields to optional:
- incidentDisplayId
- incidentShareFlag
- essIncidentIssuerId
- flagAnonymous


## [3.0.0] - 2024-02-19
### Changed
- updated version of model
- update reference to shared aspect address
- update BPN-L/S/A and refer to shared model
- update IDs and refer to shared Uuidv4Characteristic
- delete product number
- update copyright information


## [2.0.0] - 2023-08-21
### Changed
- updated version of model
- change headline to subject
- change ess incident issuer name to first name, add last name
- change field descriptions 
- use reference to shared aspect address, replace formerly used fields for address information 
- keep ess originator country subdivision (not in shared aspect)
- keep ess incident issuer country subdivision (not in shared aspect)


### Added
- incident external notes and external subject for external communication
- incident master operating company id and sub case operating company id
- incident display id
- incident status information
- incident share flag
- incident system id
- regular expressions for UUIDv4 and BPN

### Removed
- incident duration
- batch number
- unique part number
- ess originator bpn available
- ess originator cx member
- ess incident issuer company name



## [1.0.0] - 2022-11-18
### Added
- initial version of model



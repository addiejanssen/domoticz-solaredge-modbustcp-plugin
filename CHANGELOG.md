# Change Log

This is the changelog of the Domoticz SolarEdge_ModbusTCP plugin.

## [2.0.1] - 2022-10-02

This is a pre-release of the 2.x.x version of the plugin which will support reading meter and battery data next to the inverter data.

### Contributors

Many thanks to @sorinpopa for allowing me to use his inverter for testing the new functionality

### Changed

This is a major rewrite of the plugin and is only tested by a very small group of users so far.
And although it was tested by them, we may not yet have found all issues with it.

We would love to receive feedback on this version in the Discussions before we are going to release it to the public!

This version of the plugin now supports reading 3 meters and 2 batteries (limits set by SolarEdge specification).

The plugin uses tables to map the values returned by the inverter to devices recognized by Domoticz:
- This version has been tested with the SE-MTR-3Y-400V-A meter which is reported as "Wye 3P1N Three Phase Meter" in the plugin
- We added the "Single Phase Meter" meter table based on the "Wye 3P1N Three Phase Meter"
  - This is a best guess and needs confirmation from the community
- We have not added any specific battery table yet, since we need actual data to implement the tables

The plugin will use a table with all potential values as returned by SolarEdge and
may therefore display values that are not applicable for that particular type of meter.
When you encounter this, please share your meter data in the Discussions so we can refine the meter tables.

We have not defined any battery table at this moment.
When you have a battery attached to your inverter, please share your data in the Discussions so we can build those tables.

## [1.1.1] - 2022-09-18

This is the latest and last version of the 1.x.x series of the plugin.
The 1.x.x. versions only supports reading inverter data
and does not support meters and batteries.

### Added

- It is now possible to set the Modbus device address

### Changed

- Switched to [solaredge_modbus](https://github.com/nmakel/solaredge_modbus) library version 0.7.0
    - Renamed various P1/P2/P3 values to L1/L2/L3


## [version] - yyyy-mm-dd
### Added
### Changed
### Fixed

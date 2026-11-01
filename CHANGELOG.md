# Change Log

This is the changelog of the Domoticz SolarEdge_ModbusTCP plugin.

## [2.1.1] - yyyy-mm-dd

This is the first (pre-release) of the 2.1.x version of the plugin.
This version should be considered as an __alpha__ version - __it needs testing and community feedback__!

The main focus of this version is to replace the (archived) [solaredge_modbus](https://github.com/nmakel/solaredge_modbus) library and to fix the errors in battery detection.

According to SolarEdge, their inverters follow the [SunSpec Specifications](https://sunspec.org/specifications/).
A scanner was created and the community was asked to run it against their SolarEdge inverters to understand how these inverters respond.

Based on the community feedback, it is clear that the inverters indeed follow the SunSpec specification regarding the detection of supported information models.
It became clear the they return far more information than documented by SolarEdge and, very important, that the documentation of SolarEdge matches the SunSpec specifications.
The SunSpec specification defines battery related information models as well.
However, based on the scan results it looks like SolarEdge has not implemented those information models in their inverters and continues to use their vendor specific approach.

The codebase of the plugin has undergone a major restructure to replace the `solaredge_modbus` library.

The 2.1.x version now follows the SunSpec specification to identify the inverter and its capabilities, but continues to use the SolarEdge specification regarding batteries.
This has resulted in a new approach to find attached meters and batteries.

Another major change relates to how the plugin creates and updates Domoticzs devices.
Each "type of" device now has its own python class.
For example: when displaying the frequency (which is not natively supported by Domoticz), the FrequencyDevice class "knows" how to create a custom device and how to update the values of it.
This approach resulted in much easier to create and maintain mapping tables (which have moved into their own file as well).

### WARNING

This version of the plugin requires a newer version of `pymodbus` which is __INCOMPATIBLE__ with the 1.1.x and 2.0.x versions of the plugin.

__DO NOT OVERWRITE__ your current 1.1.x or 2.0.x plugin with this 2.1.x version at this point in time, but run them __next to each other__.

> Action: create wiki page with installation instructions!

### Added

- This version introduces its own code to interact with the SolarEdge inverters.
- The plugin now uses the SunSpec documented process to identify supported information models.
- Domoticz devices now have their own python class which means that all measurements of a particular type will have exactly the same behavior.

### Changed

- Major restructuring of the code base and the device mapping tables.
- Removed the (archived) [solaredge_modbus](https://github.com/nmakel/solaredge_modbus) library.
- Removed the option to enable/disable calculations. Calculations are now defined per device class and can not be turned on or off.
- Removed the option to scan for particular hardware components. As of this version, the plugin should be able to take care of it itself.
- The log level settings have been renamed and limited to "Normal", "Info" and "Debug".

### Fixed

- Battery detection should filter out "ghost" devices by not only checking the returned device address, but also making sure that there's a valid manufacturer name.

## [2.0.7] - 2026-09-21

This is a pre-release of the 2.0.x version of the plugin which will support reading meter and battery data next to the inverter data.

The focus of this release is fixing issues and making the plugin more robust.

### Fixed

- Fixed missing offset in processValues.
  Thanks goes out to [JayDotR](https://forum.domoticz.com/memberlist.php?mode=viewprofile&u=42451)
  for finding the bug and providing the fix.

## [2.0.6] - 2026-09-20

This is a pre-release of the 2.0.x version of the plugin which will support reading meter and battery data next to the inverter data.

The focus of this release is fixing issues and making the plugin more robust.

### Added

- Added disconnect from the inverter when Domoticz is stopping the plugin.

### Changed

- Restructured the repository. Code has moved into the `src` folder.
- The `helpers.py` code has been cleaned up.
- The Average() and Maximum() classes stored their samples in a fixed size list.
  As a result, the calculation could use values that were very old; for example
  the last value of one day and the first value of the following day.
  This has been changed into a list of timestamp/sample tuples allowing us to
  expire samples based on the timestamp.

### Fixed

- Some graphs showed long slopes for particular values.
  The plugin would not update values when the new value was the same as the previous value.
  Thanks goes out to [CreasolTech](https://github.com/CreasolTech) for coming up with the solution.
  We now force storing the value at least once every 5 minutes.
- The inverter may not always return information of meters or batteries.
  This would result in key errors.
  Added a check if information is available; if not, a message is logged.

## [2.0.5] - 2026-09-13

This is a pre-release of the 2.0.x version of the plugin which will support reading meter and battery data next to the inverter data.

### Changed

- Check keys in device details and response from inverter to prevent key missing errors.
- Recognize v1.x.x Mode4 (math toggle) parameter values.
- Recognize v1.x.x Mode5 (log level) parameter values.
- Updated the requirements to the latest supported versions of `solaredge_modbus` and `pymodbus`.

## [2.0.4] - 2023-07-23

This is a pre-release of the 2.0.x version of the plugin which will support reading meter and battery data next to the inverter data.

> This is an Alpha version!
> Use at your own risk, but be aware that historical (battery) information may be lost in next versions!

### Fixed

- Updated the formatting of SOE and SOH values of the batteries. Thank you [Peter Vermaas](https://github.com/PeterVermaas)!

## [2.0.3] - 2022-12-28

This is a pre-release of the 2.0.x version of the plugin which will support reading meter and battery data next to the inverter data.

> This is an Alpha version!
> Use at your own risk, but be aware that historical (battery) information may be lost in next versions!

### Added

A battery table has been added to process the information returned by the inverter.
This is a first attempt to display battery information in Domoticz.
The devices in Domoticz may not show correct information at this point in time.

### Fixed

- The plugin now provides an option to select if it should scan for batteries and/or meters.
  This allows skipping ghost devices reported by the inverter.

## [2.0.2] - 2022-10-29

This is a pre-release of the 2.0.x version of the plugin which will support reading meter and battery data next to the inverter data.

### Added

Tested with the latest version (0.7.2) of the `solaredge_modbus` library.

### Changed

During testing it was found that certain inverters return battery information while there were no batteries attached to the inverter.
First investigations shows that this might be an issue caused by the `solaredge_modbus` library.
We will contact the developer of that library to further investigate.
For now, battery support has been turned off.

### Fixed

- In certain situations, the plugin could run into uninitialized variables.
- The timeout value used for communication with the inverter has been increased (from 5 to 15 seconds).

## [2.0.1] - 2022-10-02

This is a pre-release of the 2.0.x version of the plugin which will support reading meter and battery data next to the inverter data.

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

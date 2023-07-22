# Domoticz SolarEdge_ModbusTCP plugin

A Domoticz plugin to collect data from SolarEdge power inverters over ModbusTCP.

The plugin uses the `solaredge_modbus` library (<https://github.com/nmakel/solaredge_modbus>) to communicate with the inverter.

The 1.x.x versions of the plugin only read the inverter data.

The 2.x.x versions supports reading inverter, meter and battery data.

## Requirements

The inverter needs to be connected to the network (either wired or wireless) and Modbus must be enabled on the device. Please consult the documentation of your inverter to find out how to enable Modbus.

## Installation of the plugin

Install `Domoticz` and make sure that `python 3.x` is installed on the computer.

Download the plugin zip-file from [releases](https://github.com/addiejanssen/domoticz-solaredge-modbustcp-plugin/releases)

Unpack the contents of the zip-file into a folder in the `plugins` folder of your Domoticz installation.

Go to the folder where the plugin files were extracted to and install the dependencies:

```
sudo pip3 install -r requirements.txt
```

Then restart Domoticz and the plugin should become visible in the hardware dropdown list.

## Updating the plugin

Updating the plugin can be done by removing the previous version and do a clean install again. Make sure to stop the Domoticz service before you start or at least stop all hardware that is related to the plugin.

Make sure that the requirements listed in the `requirements.txt` file are met. If newer versions of the `solaredge_modbus` library are required, make sure that you remove the older versions to prevent version conflicts.

## Configuration in Domoticz

Once the plugin is installed, a new hardware type will be available: `SolarEdge ModbusTCP`.

To add the inverter, go to `Setup` -\> `Hardware` and add the inverter:

-   Enter a `name` for the inverter.
-   Select `SolarEdge ModbusTCP` from the `type` dropdown list.
-   Enter the IP address or the DNS name of the inverter in the `Inverter IP Address` field.
-   Enter the port number (default: 502) of the inverter in the `Inverter Port Number` field.
-   Enter the Modbus device address (default: 1) of the inverter in the `Inverter Modbus device address` field.
-   Select `Yes` in the `Add missing devices` to create the devices when the inverter is added. Select `No` after deleting unused devices. Leaving the option set to `Yes` will recreate the deleted devices once Domoticz is restarted.
-   Select an `Interval` (default: 5 seconds); this defines how often the plugin will collect the data from the inverter. Short intervals will result in more accurate values and graphs, but also result in more network traffic and a higher workload for both Domoticz and the inverter.
-   Optionally change the `Auto Avg/Max math`; this defaults to `Enabled` which means that the Domoticz graphs for most values will be averaged over time. When selecting `Disabled`, the Domoticz graphs will be based on the last retrieved value.
-   Optionally change the `Log level`; this defaults to `Normal` which logs basic information in the Domoticz logfile. Selecting `Verbose` is helpful showing the data that is retrieved from the inverter. The `Verbose+` and `Verbose++` options are for debugging purposes and log a lot of information.
-   `Add` the inverter.

This should result in a lot of new devices in the `Setup` -\> `Devices` menu.
# Multical 21


Multical 21 custom component for Home Assistant.
![image](https://user-images.githubusercontent.com/6593720/220913633-3daa874f-3ed3-4e39-b827-ec7a1ce1f6dd.png)

## Requirements

To use this custom component, you'll need an optical eye and connect your machine running Home Assistant directly with the optical eye to the Kamstrup multical 21 meter.
The optical eye looks like this:<br>
![image](https://user-images.githubusercontent.com/6593720/220914030-3ca8bec3-b302-4ed7-a0b8-c4858b0c8120.png)
I ordered it from [here](https://www.aliexpress.com/item/1005004567409202.html?spm=a2g0o.order_list.order_list_main.18.43e81802zaII7n)
You can also 3d Print [this mount ](https://makerworld.com/en/models/490708#profileId-404169)

## Installation

### HACS

This component can be installed directly via HACS. Search for "Multical 21" in the HACS integration list and click "Download".


### Manual

1. Open the directory for your HA configuration (where you find `configuration.yaml`).
2. If you do not have a `custom_components` directory, create it.
3. Download the `custom_components/multical_21/` directory from this repository as a ZIP and extract it, or clone the repository.
4. Copy the `multical_21` folder into your `custom_components` directory.
5. Restart Home Assistant.
6. In the HA UI go to "Settings" → "Devices & Services", click "Add Integration" and search for "Multical 21".

## Configuration is done in the UI

It's recommended to use devices as `/dev/serial/by-id` and not `/dev/ttyUSB1` as the port. This is because the first example is a stable identifier, while the second can change when USB devices are added or removed, or even when you perform a system reboot.<br>
The port should look like this: `/dev/serial/by-id/usb-FTDI_FT230X_Basic_UART_D307PBVY-if00-port0`.

Some meters contain a battery, and communicating with the meter does impact battery life. By default, this component updates every `3600` seconds (1 hour). This is configurable. You can also configure the serial timeout. The default value is `1.0` seconds. If you get the error `Finished update, No readings from the meter. Please check the IR connection` you can try to increase this value. Fractional numbers are allowed (eg. `0.5`).
Both settings can be changed by pressing "Configure" on the Integrations page.

## Collect logs

When you want to report an issue, please add logs from this component. You can enable logging for this component by configuring the logger in Home Assistant as follows:
```yaml
logger:
  default: warn
  logs:
    custom_components.multical_21: debug
```
More info can be found on the [Home Assistant logger integration page](https://www.home-assistant.io/integrations/logger)

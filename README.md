# Kamstrup 403

[![GitHub Release][releases-shield]][releases]
[![GitHub Repo stars][stars-shield]][stars]
[![License][license-shield]](LICENSE)
[![GitHub Activity][commits-shield]][commits]
[![Code coverage][codecov-shield]][codecov]
[![hacs][hacs-shield]][hacs]
[![hacs][hacs-installs-shield]][hacs]
[![Project Maintenance][maintenance-shield]][maintainer]
[![BuyMeCoffee][buymecoffeebadge]][buymecoffee]

Multical 403 custom component for Home Assistant.

<img width="660" alt="info" src="https://user-images.githubusercontent.com/2211503/200671065-201f84bc-0d01-4a87-8fd9-3da3beedfb5d.png">

## Requirements

To use this custom component, you'll need an optical eye and connect your machine running Home Assistant directly with the optical eye to the Kamstrup meter.
The optical eye looks like this:<br>
![cable](https://user-images.githubusercontent.com/2211503/136630069-9da49f09-6f9c-4618-8255-40195405f21a.jpg)

## Installation

### HACS

This component can easily be installed in your Home Assistant using HACS.


### Manual

1. Using the tool of choice open the directory (folder) for your HA configuration (where you find `configuration.yaml`).
2. If you do not have a `custom_components` directory (folder) there, you need to create it.
3. In the `custom_components` directory (folder) create a new folder called `multical_21`.
4. Download _all_ the files from the `custom_components/multical_21/` directory (folder) in this repository.
5. Place the files you downloaded in the new directory (folder) you created.
6. Restart Home Assistant
7. In the HA UI go to "Configuration" -> "Integrations" click "+" and search for "Multical 21"

Using your HA configuration directory (folder) as a starting point you should now also have these files:

```text
custom_components/multical_21/translations/en.json
custom_components/multical_21/translations/nl.json
custom_components/multical_21/__init__.py
custom_components/multical_21/config_flow.py
custom_components/multical_21/const.py
custom_components/multical_21/kamstrup.py
custom_components/multical_21/manifest.json
custom_components/multical_21/sensor.py
```

## Configuration is done in the UI

It's recommended to use devices as `/dev/serial/by-id` and not `/dev/ttyUSB1` as the port. This is because the first example is a stable identifier, while the second can change when USB devices are added or removed, or even when you perform a system reboot.<br>
The port should look like this: `/dev/serial/by-id/usb-FTDI_FT230X_Basic_UART_D307PBVY-if00-port0`.

Some meters contain a battery, and communicating with the meter does impact battery life. By default, this component updates every `3600` seconds (1 hour). This is configurable. Also, since version `2.0.1` you can also configure the serial timeout. The default value is `1.0` seconds, if you get the error `Finished update, No readings from the meter. Please check the IR connection` you can try to increase this value. Fractional numbers are allowed (eg. `0.5`).
You can do this by pressing `configure` on the Integrations page:

<img width="300" alt="integration" src="https://user-images.githubusercontent.com/2211503/200671075-39c7a812-42a2-4a4d-8934-6ea37517a400.png"> <img width="300" alt="configure" src="https://user-images.githubusercontent.com/2211503/201747344-b019693a-1d88-4ca1-9a28-87fa24992e13.png">

## Collect logs

When you want to report an issue, please add logs from this component. You can enable logging for this component by configuring the logger in Home Assistant as follows:
```yaml
logger:
  default: warn
  logs:
    custom_components.kamstrup_403: debug
```
More info can be found on the [Home Assistant logger integration page](https://www.home-assistant.io/integrations/logger)

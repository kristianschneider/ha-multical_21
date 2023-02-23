[![GitHub Release][releases-shield]][releases]
[![GitHub Activity][commits-shield]][commits]
[![License][license-shield]][license]

[![hacs][hacsbadge]][hacs]
[![Project Maintenance][maintenance-shield]][user_profile]
[![BuyMeCoffee][buymecoffeebadge]][buymecoffee]

_Component to integrate with [multical_21][multical_21]._

**This component will set up the following platforms.**

Platform | Description
-- | --
`sensor` | Show info from the meter.

{% if not installed %}
## Installation

1. Click install.
1. In the HA UI go to "Configuration" -> "Integrations" click "+" and search for "Multical 21".

{% endif %}


## Configuration is done in the UI

It's recommended to use devices as `/dev/serial/by-id` and not `/dev/ttyUSB1` as the port, as the first one should be stable, while the second one can change when you add/remove usb (serial) adapters, or even when you perform a system reboot.
The port will become something like: `/dev/serial/by-id/usb-FTDI_FT230X_Basic_UART_D307PBVY-if00-port0`.

***


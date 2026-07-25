"""Sensor platform for multical_21."""

from homeassistant.components.sensor import (
    SensorDeviceClass,
    SensorEntity,
    SensorEntityDescription,
    SensorStateClass,
)
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.typing import StateType
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from . import KamstrupConfigEntry, KamstrupUpdateCoordinator
from .const import DEFAULT_NAME

DESCRIPTIONS: list[SensorEntityDescription] = [
    SensorEntityDescription(
        key="68",  # 0x0044
        name="V1",
        icon="mdi:water",
        device_class=SensorDeviceClass.WATER,
        state_class=SensorStateClass.TOTAL_INCREASING,
    ),
    SensorEntityDescription(
        key="243",  # 0x00f3
        name="V1Reverse",
        icon="mdi:water-sync",
        device_class=SensorDeviceClass.WATER,
        state_class=SensorStateClass.TOTAL_INCREASING,
    ),
    SensorEntityDescription(
        key="74",  # 0x004a
        name="Flow",
        icon="mdi:waves",
        device_class=SensorDeviceClass.VOLUME_FLOW_RATE,
        state_class=SensorStateClass.MEASUREMENT,
    ),
    SensorEntityDescription(
        key="1004",  # 0x03ec
        name="HoursCounter",
        icon="mdi:clock",
        device_class=SensorDeviceClass.DURATION,
        state_class=SensorStateClass.MEASUREMENT,
        entity_registry_enabled_default=False,
    ),
    SensorEntityDescription(
        key="99",  # 0x0063
        name="Info",
        icon="mdi:information",
        device_class=None,
        state_class=None,
        entity_registry_enabled_default=False,
    ),
]


async def async_setup_entry(
    hass: HomeAssistant,
    entry: KamstrupConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up Kamstrup sensors based on a config entry."""
    coordinator = entry.runtime_data

    async_add_entities(
        KamstrupMeterSensor(
            coordinator=coordinator,
            entry_id=entry.entry_id,
            description=description,
        )
        for description in DESCRIPTIONS
    )


class KamstrupSensor(CoordinatorEntity[KamstrupUpdateCoordinator], SensorEntity):
    """Defines a Kamstrup sensor."""

    _attr_has_entity_name = True

    def __init__(
        self,
        coordinator: KamstrupUpdateCoordinator,
        entry_id: str,
        description: SensorEntityDescription,
    ) -> None:
        """Initialize Kamstrup sensor."""
        super().__init__(coordinator=coordinator)

        self.entity_description = description
        # The unique_id format is kept identical to previous releases so
        # existing registry entries (and their entity_ids) are preserved.
        self._attr_unique_id = f"{entry_id}-{DEFAULT_NAME} {description.name}"
        self._attr_device_info = coordinator.device_info


class KamstrupMeterSensor(KamstrupSensor):
    """Defines a Kamstrup meter sensor."""

    async def async_added_to_hass(self) -> None:
        """Run when entity about to be added to hass."""
        await super().async_added_to_hass()
        self.coordinator.register_command(self.int_key)

    async def async_will_remove_from_hass(self) -> None:
        """Run when entity will be removed from hass."""
        await super().async_will_remove_from_hass()
        self.coordinator.unregister_command(self.int_key)

    @property
    def int_key(self) -> int:
        """Get the key as an int"""
        return int(self.entity_description.key)

    @property
    def native_value(self) -> StateType:
        """Return the state of the sensor."""
        if self.coordinator.data and self.coordinator.data.get(self.int_key):
            return self.coordinator.data[self.int_key].get("value", None)

        return None

    @property
    def native_unit_of_measurement(self) -> str | None:
        """Return the unit of measurement of the sensor, if any."""
        if self.coordinator.data and self.coordinator.data.get(self.int_key):
            return self.coordinator.data[self.int_key].get("unit", None)

        return None

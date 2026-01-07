from __future__ import annotations

import logging

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.components.select import SelectEntity
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)
_LOGGER.warning("ledble_ledlamp: select.py imported")

MUSIC_OPTIONS = ["Music 1", "Music 2", "Music 3", "Music 4"]


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    lamp = hass.data[DOMAIN][entry.entry_id]
    async_add_entities([LEDBLEMusicModeSelect(lamp, entry)], True)
    _LOGGER.warning("ledble_ledlamp: select async_setup_entry called")



class LEDBLEMusicModeSelect(SelectEntity):
    """Select entity to switch LEDDMX-03 music modes (1..4)."""

    _attr_has_entity_name = True
    _attr_icon = "mdi:music"
    _attr_options = MUSIC_OPTIONS

    def __init__(self, lamp, entry: ConfigEntry) -> None:
        self._lamp = lamp
        self._entry = entry
        self._attr_unique_id = f"{entry.entry_id}_music_mode"
        self._attr_name = "Music mode"
        self._current: str | None = None

    @property
    def current_option(self) -> str | None:
        return self._current

    async def async_select_option(self, option: str) -> None:
        # option: "Music N"
        try:
            mode = int(option.split()[-1])
        except Exception:
            _LOGGER.warning("Invalid music option: %s", option)
            return

        await self._lamp.set_music_mode(mode)
        self._current = option
        self.async_write_ha_state()

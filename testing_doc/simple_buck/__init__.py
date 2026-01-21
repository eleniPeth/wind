# Scripts/buck/__init__.py

from .controller import (
    PIController,
    get_pwr_target,     # power-lookup
)
from .hardware import (
    init_adc,
    init_pwm,
    read_voltage,
    read_current,       # now available at package level
    set_duty_cycle,
    shutdown,
)


__all__ = [
    "PIController",
    "get_voltage_target",
    "get_pwr_target",
    "init_adc",
    "init_pwm",
    "read_voltage",
    "read_current",
    "set_duty_cycle",
    "shutdown",
]

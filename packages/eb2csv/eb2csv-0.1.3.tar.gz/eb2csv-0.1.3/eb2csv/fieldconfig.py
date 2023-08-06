# -*- coding: utf-8 -*-

from collections import namedtuple


class FieldConfig(namedtuple('FieldConfig', ['name', 'unit', 'display_precision', 'type', 'verbose_name', 'category'])):
    """
    Meta data records for the LiveData attributes.
    """
    def to_dict(self):
        return {
            'name': self.name,
            'unit': self.unit,
            'displayPrecision': self.display_precision,
            'type': self.type,
            'verboseName': self.verbose_name,
            'category': self.category,
        }


ELECTRICITY = 'ELECTRICITY'
FLUID = 'FLUID'
GENERIC = 'GENERIC'
DMG_MACHINE = 'DMG_MACHINE'

field_configs = [
    FieldConfig('timestamp', 's', 0, 'posix', 'POSIX timestamp', None),
    FieldConfig('working_hours', 'h', None, 'float', 'Working hours', ELECTRICITY),
    FieldConfig('frequency', 'Hz', 3, 'float', 'Frequency', ELECTRICITY),

    FieldConfig('voltage_L1', 'V', 1, 'float', 'Voltage L1', ELECTRICITY),
    FieldConfig('voltage_L2', 'V', 1, 'float', 'Voltage L2', ELECTRICITY),
    FieldConfig('voltage_L3', 'V', 1, 'float', 'Voltage L3', ELECTRICITY),
    FieldConfig('max_voltage_L1', 'V', 1, 'float', 'Maximum voltage L1', ELECTRICITY),
    FieldConfig('max_voltage_L2', 'V', 1, 'float', 'Maximum voltage L2', ELECTRICITY),
    FieldConfig('max_voltage_L3', 'V', 1, 'float', 'Maximum voltage L3', ELECTRICITY),
    FieldConfig('min_voltage_L1', 'V', 1, 'float', 'Minimum voltage L1', ELECTRICITY),
    FieldConfig('min_voltage_L2', 'V', 1, 'float', 'Minimum voltage L2', ELECTRICITY),
    FieldConfig('min_voltage_L3', 'V', 1, 'float', 'Minimum voltage L3', ELECTRICITY),
    FieldConfig('avg_voltage_L1', 'V', 1, 'float', 'Average voltage L1', ELECTRICITY),
    FieldConfig('avg_voltage_L2', 'V', 1, 'float', 'Average voltage L2', ELECTRICITY),
    FieldConfig('avg_voltage_L3', 'V', 1, 'float', 'Average voltage L3', ELECTRICITY),

    FieldConfig('current_L1', 'A', 1, 'float', 'Current L1', ELECTRICITY),
    FieldConfig('current_L2', 'A', 1, 'float', 'Current L2', ELECTRICITY),
    FieldConfig('current_L3', 'A', 1, 'float', 'Current L3', ELECTRICITY),
    FieldConfig('max_current_L1', 'A', 1, 'float', 'Maximum current L1', ELECTRICITY),
    FieldConfig('max_current_L2', 'A', 1, 'float', 'Maximum current L2', ELECTRICITY),
    FieldConfig('max_current_L3', 'A', 1, 'float', 'Maximum current L3', ELECTRICITY),
    FieldConfig('min_current_L1', 'A', 1, 'float', 'Minimum current L1', ELECTRICITY),
    FieldConfig('min_current_L2', 'A', 1, 'float', 'Minimum current L2', ELECTRICITY),
    FieldConfig('min_current_L3', 'A', 1, 'float', 'Minimum current L3', ELECTRICITY),
    FieldConfig('avg_current', 'A', 1, 'float', 'Average current', ELECTRICITY),
    FieldConfig('avg_current_L1', 'A', 1, 'float', 'Average current L1', ELECTRICITY),
    FieldConfig('avg_current_L2', 'A', 1, 'float', 'Average current L2', ELECTRICITY),
    FieldConfig('avg_current_L3', 'A', 1, 'float', 'Average current L3', ELECTRICITY),

    FieldConfig('active_pwr_L1', 'W', 1, 'float', 'Active power L1', ELECTRICITY),
    FieldConfig('active_pwr_L2', 'W', 1, 'float', 'Active power L2', ELECTRICITY),
    FieldConfig('active_pwr_L3', 'W', 1, 'float', 'Active power L3', ELECTRICITY),
    FieldConfig('reactive_pwr_L1', 'var', 1, 'float', 'Reactive power L1', ELECTRICITY),
    FieldConfig('reactive_pwr_L2', 'var', 1, 'float', 'Reactive power L2', ELECTRICITY),
    FieldConfig('reactive_pwr_L3', 'var', 1, 'float', 'Reactive power L3', ELECTRICITY),
    FieldConfig('apparent_pwr_L1', 'VA', 1, 'float', 'Apparent power L1', ELECTRICITY),
    FieldConfig('apparent_pwr_L2', 'VA', 1, 'float', 'Apparent power L2', ELECTRICITY),
    FieldConfig('apparent_pwr_L3', 'VA', 1, 'float', 'Apparent power L3', ELECTRICITY),

    FieldConfig('sum_apparent_pwr', 'VA', 1, 'float', 'Apparent power', ELECTRICITY),
    FieldConfig('sum_active_pwr', 'W', 1, 'float', 'Active power', ELECTRICITY),
    FieldConfig('sum_reactive_pwr', 'var', 1, 'float', 'Reactive power', ELECTRICITY),
    FieldConfig('avg_active_pwr', 'W', 1, 'float', 'Average active power', ELECTRICITY),
    FieldConfig('avg_reactive_pwr', 'var', 1, 'float', 'Average reactive power', ELECTRICITY),
    FieldConfig('avg_active_pwr_in', 'W', 1, 'float', 'Average active power in', ELECTRICITY),
    FieldConfig('avg_active_pwr_out', 'W', 1, 'float', 'Average active power out', ELECTRICITY),
    FieldConfig('avg_reactive_pwr_in', 'var', 1, 'float', 'Average reactive power in', ELECTRICITY),
    FieldConfig('avg_reactive_pwr_out', 'var', 1, 'float', 'Average reactive power out', ELECTRICITY),
    FieldConfig('max_active_pwr', 'W', 1, 'float', 'Maximum active power', ELECTRICITY),
    FieldConfig('min_active_pwr', 'W', 1, 'float', 'Minimum active power', ELECTRICITY),
    FieldConfig('max_reactive_pwr', 'var', 1, 'float', 'Maximum reactive power', ELECTRICITY),
    FieldConfig('min_reactive_pwr', 'var', 1, 'float', 'Minimum reactive power', ELECTRICITY),
    FieldConfig('active_energy_in', 'Wh', 0, 'float', 'Active energy in', ELECTRICITY),
    FieldConfig('active_energy_out', 'Wh', 0, 'float', 'Active energy out', ELECTRICITY),
    FieldConfig('reactive_energy_in', 'varh', 0, 'float', 'Reactive energy in', ELECTRICITY),
    FieldConfig('reactive_energy_out', 'varh', 0, 'float', 'Reactive energy out', ELECTRICITY),

    FieldConfig('sum_pwr_factor', '', 3, 'float', 'Power factor', ELECTRICITY),
    FieldConfig('avg_pwr_factor', '', 3, 'float', 'Average power factor', ELECTRICITY),
    FieldConfig('min_pwr_factor', '', 3, 'float', 'Minimum power factor', ELECTRICITY),
    FieldConfig('max_pwr_factor', '', 3, 'float', 'Maximum power factor', ELECTRICITY),

    FieldConfig('ct_primary', 'A', 0, 'int', 'CT primary current', ELECTRICITY),
    FieldConfig('ct_secondary', 'A', 0, 'int', 'CT secondary current', ELECTRICITY),
    FieldConfig('ct_ratio', '', 3, 'float', 'CT ratio', ELECTRICITY),
    # Fluid
    FieldConfig('mass_flow', 'kg/h', 2, 'float', 'Mass flow', FLUID),
    FieldConfig('avg_mass_flow', 'kg/h', 2, 'float', 'Average mass flow', FLUID),
    FieldConfig('min_mass_flow', 'kg/h', 2, 'float', 'Minimum mass flow', FLUID),
    FieldConfig('max_mass_flow', 'kg/h', 2, 'float', 'Maximum mass flow', FLUID),
    FieldConfig('volume_flow', u'm³/h', 2, 'float', 'Volume flow', FLUID),
    FieldConfig('avg_volume_flow', u'm³/h', 2, 'float', 'Avergae volume flow', FLUID),
    FieldConfig('min_volume_flow', u'm³/h', 2, 'float', 'Minimum volume flow', FLUID),
    FieldConfig('max_volume_flow', u'm³/h', 2, 'float', 'Maximum volume flow', FLUID),
    FieldConfig('temperature', u'°C', 2, 'float', 'Temperature', FLUID),
    FieldConfig('temperature2', u'°C', 2, 'float', 'Temperature 2', FLUID),
    FieldConfig('dewpoint', u'°C', 2, 'float', 'Dew point', FLUID),
    FieldConfig('rel_humidity', u'% r.H.', 2, 'float', 'Relative humidity', FLUID),
    FieldConfig('level', '%', 2, 'float', 'Level', FLUID),
    FieldConfig('total_mass_pos', 'kg', 2, 'float', 'Total mass positiv', FLUID),
    FieldConfig('total_mass_neg', 'kg', 2, 'float', 'Total mass negativ', FLUID),
    FieldConfig('total_mass', 'kg', 2, 'float', 'Total mass', FLUID),
    FieldConfig('total_volume_pos', u'm³', 2, 'float', 'Total volume positiv', FLUID),
    FieldConfig('total_volume_neg', u'm³', 2, 'float', 'Total volume negativ', FLUID),
    FieldConfig('total_volume', u'm³', 2, 'float', 'Total volume', FLUID),
    FieldConfig('total_energy_pos', 'Wh', 2, 'float', 'Total energy positiv', FLUID),
    FieldConfig('total_energy_neg', 'Wh', 2, 'float', 'Total energy negativ', FLUID),
    FieldConfig('total_energy', 'Wh', 2, 'float', 'Total energy', FLUID),
    FieldConfig('pressure', 'bar', 2, 'float', 'Pressure', FLUID),
    FieldConfig('power', 'W', 2, 'float', 'Power', FLUID),
    FieldConfig('avg_power', 'W', 2, 'float', 'Average power', FLUID),
    FieldConfig('min_power', 'W', 2, 'float', 'Minimum power', FLUID),
    FieldConfig('max_power', 'W', 2, 'float', 'Maximum power', FLUID),
    # Auxiliary
    FieldConfig('digital_in', '', None, 'bool', 'Digital In', GENERIC),
    FieldConfig('counter', '', 0, 'int', 'Counter', GENERIC),
    FieldConfig('analog_in', '', 5, 'float', 'Analog In', GENERIC),
    # RTU-Gateway
    FieldConfig('cycle_duration', 's', 1, 'float', 'Read cycle duration', 'gateway'),
    # DMG machine (UDI client)
    FieldConfig('dmg_machine_gauge_present', '', None, 'bool', 'Energy gauge is connected', DMG_MACHINE),
    FieldConfig('dmg_machine_serial_number', '', None, 'string', 'Ident code/serial number', DMG_MACHINE),
    FieldConfig('dmg_machine_signal_light', '', 0, 'int', 'Signal light bits', DMG_MACHINE),
    FieldConfig('dmg_production_parts_actual', '', 0, 'int', 'User specific counter', DMG_MACHINE),
    FieldConfig('dmg_production_parts_total', '', 0, 'int', 'Parts since NC start', DMG_MACHINE),
    FieldConfig('dmg_production_parts_desired', '', 0, 'int', 'Parts requested', DMG_MACHINE),
    FieldConfig('dmg_production_part_name', '', None, 'string', 'Name of active workpiece', DMG_MACHINE),
    FieldConfig('dmg_production_selected_prog', '', None, 'string', 'Selected program', DMG_MACHINE),
]
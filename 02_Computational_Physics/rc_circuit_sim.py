"""
rc_circuit_sim.py
Simulates the voltage across a capacitor in a simple RC circuit.
Designed as a small Engineering Physics practice script.
"""

import math


def capacitor_voltage(source_voltage, resistance_ohm, capacitance_farad, time_seconds, charging=True):
    """
    Calculates capacitor voltage during RC charging or discharging.

    Formula:
        Charging:    Vc(t) = Vs * (1 - e^(-t / RC))
        Discharging: Vc(t) = Vs * e^(-t / RC)
    """
    if resistance_ohm <= 0 or capacitance_farad <= 0:
        raise ValueError("Resistance and capacitance must be positive.")
    if time_seconds < 0:
        raise ValueError("Time cannot be negative.")

    time_constant = resistance_ohm * capacitance_farad

    if charging:
        return source_voltage * (1 - math.exp(-time_seconds / time_constant))

    return source_voltage * math.exp(-time_seconds / time_constant)


def print_rc_table(source_voltage, resistance_ohm, capacitance_farad):
    """Prints capacitor voltage at several useful time points."""
    time_constant = resistance_ohm * capacitance_farad
    time_points = [0, 0.5, 1, 2, 3, 5]

    print("\n" + "=" * 55)
    print(" RC CIRCUIT CAPACITOR VOLTAGE SIMULATION")
    print("=" * 55)
    print(f" Source Voltage : {source_voltage:>8.2f} V")
    print(f" Resistance     : {resistance_ohm:>8.2f} ohm")
    print(f" Capacitance    : {capacitance_farad:>8.6f} F")
    print(f" Time Constant  : {time_constant:>8.4f} s\n")

    print(" Time       Charging Voltage     Discharging Voltage")
    print("-" * 55)

    for multiplier in time_points:
        current_time = multiplier * time_constant
        charging_v = capacitor_voltage(source_voltage, resistance_ohm, capacitance_farad, current_time)
        discharging_v = capacitor_voltage(
            source_voltage,
            resistance_ohm,
            capacitance_farad,
            current_time,
            charging=False,
        )

        print(f" {multiplier:>4.1f} tau   {charging_v:>10.3f} V          {discharging_v:>10.3f} V")

    print("=" * 55 + "\n")


if __name__ == "__main__":
    # Example: a 5V sensor circuit with a 10k ohm resistor and 100 uF capacitor.
    print_rc_table(source_voltage=5.0, resistance_ohm=10_000.0, capacitance_farad=100e-6)

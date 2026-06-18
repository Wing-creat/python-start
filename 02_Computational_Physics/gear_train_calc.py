# gear_train_calc.py
# A short gear ratio example for a compound gear train.

def calculate_gear_train(input_rpm, input_torque, gear_pairs):
    """Return the final RPM and torque after passing through each gear pair."""
    rpm = input_rpm
    torque = input_torque

    for driving, driven in gear_pairs:
        if driving <= 0 or driven <= 0:
            raise ValueError("gear teeth counts must be greater than zero.")

        ratio = driven / driving
        rpm = rpm / ratio
        torque = torque * ratio

    return rpm, torque


if __name__ == "__main__":
    gears = [(10, 30), (12, 48)]

    final_rpm, final_torque = calculate_gear_train(
        input_rpm=6000.0,
        input_torque=15.0,
        gear_pairs=gears,
    )

    print("Gear Train Example")
    print(f"gear pairs: {gears}")
    print(f"final speed: {final_rpm:.2f} RPM")
    print(f"final torque: {final_torque:.2f} Nm")

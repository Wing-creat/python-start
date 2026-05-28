"""
gear_train_calc.py
Calculates the final output RPM and torque of a compound mechanical gear train.
Designed for Engineering Physics simulations.
"""

def calculate_gear_train(input_rpm, input_torque, gear_pairs):
    """
    Iterates through a series of gear pairs to calculate the final mechanical output.
    
    Args:
        input_rpm (float): The initial rotational speed in Revolutions Per Minute.
        input_torque (float): The initial torque in Newton-meters.
        gear_pairs (list of tuples): A list containing pairs of (driving_teeth, driven_teeth).
    """
    current_rpm = input_rpm
    current_torque = input_torque
    
    print("\n" + "=" * 55)
    print(" MECHANICAL GEAR TRAIN KINEMATIC ANALYSIS")
    print("=" * 55)
    print(f" Initial Input : {current_rpm:>8.2f} RPM | {current_torque:>8.2f} Nm\n")
    
    for index, (driving, driven) in enumerate(gear_pairs):
        # Calculate gear ratio (driven teeth / driving teeth)
        # Assuming 100% efficiency for theoretical kinematic limits
        ratio = driven / driving
        current_rpm = current_rpm / ratio
        current_torque = current_torque * ratio
        
        print(f" Stage {index + 1}       : Driving ({driving}) -> Driven ({driven}) | Ratio: {ratio:.2f}")
        print(f" Current Output: {current_rpm:>8.2f} RPM | {current_torque:>8.2f} Nm\n")
        
    print("-" * 55)
    print(f" Final Output  : {current_rpm:>8.2f} RPM | {current_torque:>8.2f} Nm")
    print("=" * 55 + "\n")

if __name__ == "__main__":
    # Example simulation: A high-RPM motor passing through a two-stage reduction gearbox
    # Stage 1: 10 teeth driving 30 teeth (3:1 reduction)
    # Stage 2: 12 teeth driving 48 teeth (4:1 reduction)
    gears = [(10, 30), (12, 48)]
    
    calculate_gear_train(input_rpm=6000.0, input_torque=15.0, gear_pairs=gears)
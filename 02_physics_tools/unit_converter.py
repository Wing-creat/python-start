# unit_converter.py

def engineering_converter():
    print("--- 🔧 Engineering Unit Converter ---")
    print("1: Inches (in) to Centimeters (cm)")
    print("2: Pounds (lbs) to Kilograms (kg)")
    print("3: Fahrenheit (F) to Celsius (C)")
    
    choice = input("Select conversion type (1/2/3): ")
    
    try:
        if choice == '1':
            inches = float(input("Enter length in inches: "))
            cm = inches * 2.54
            print(f"Result: {inches} in = {cm:.4f} cm")
        elif choice == '2':
            lbs = float(input("Enter mass in pounds: "))
            kg = lbs * 0.453592
            print(f"Result: {lbs} lbs = {kg:.4f} kg")
        elif choice == '3':
            f_temp = float(input("Enter temperature in Fahrenheit: "))
            c_temp = (f_temp - 32) * 5.0/9.0
            print(f"Result: {f_temp} F = {c_temp:.2f} C")
        else:
            print("Invalid selection.")
    except ValueError:
        print("Error: Please enter numerical values.")

if __name__ == "__main__":
    engineering_converter()
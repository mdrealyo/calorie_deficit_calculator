from colorama import init, Fore, Back
import os, time

init()

def reset():
    print(Fore.RESET)

os.system("cls")

def calculate_bmr(weight, height_feet, height_inches, age, gender):
    height_in_cm = (height_feet * 30.48) + (height_inches * 2.54)  # Convert height from feet and inches to cm
    weight_in_kg = weight * 0.453592  # Convert weight from pounds to kg

    if gender.lower() == 'male':
        bmr = 10 * weight_in_kg + 6.25 * height_in_cm - 5 * age + 5
    elif gender.lower() == 'female':
        bmr = 10 * weight_in_kg + 6.25 * height_in_cm - 5 * age - 161
    else:
        return "Invalid gender. Please specify 'male' or 'female'."

    return round(bmr)

def calculate_daily_calories_for_weight_loss(current_weight, target_weight, months, bmr):
    weight_loss_per_month = (current_weight - target_weight) / months
    total_calories_to_lose = weight_loss_per_month * 3500  # 1 pound of fat = 3500 calories
    daily_caloric_deficit = total_calories_to_lose / 30  # Average days in a month
    daily_caloric_intake = bmr - daily_caloric_deficit
    return round(daily_caloric_intake)

def generate_report(current_weight, target_weight, height_feet, height_inches, gender, bmr):
    height = f"{height_feet} feet {height_inches} inches"
    activity_multipliers = {
        'sedentary': 1.2,
        'light': 1.375,
        'moderate': 1.55,
        'active': 1.725,
        'very active': 1.9
    }

    report = f"""
CURRENT WEIGHT = {current_weight} -- TARGET WEIGHT = {target_weight}
Height = {height}
Gender = {gender}
BMR = {bmr}

HOW MUCH TO EAT A DAY TO MAINTAIN BODY WEIGHT
Your BMR is: {bmr}
ACTIVITY LEVELS:
"""
    for level, multiplier in activity_multipliers.items():
        report += f"    {level}: {round(bmr * multiplier)}\n"

    report += "\nHOW MUCH TO EAT A DAY TO BECOME DREAM WEIGHT IN EACH MONTH\n"
    for month in range(1, 13):
        daily_caloric_intake = calculate_daily_calories_for_weight_loss(current_weight, target_weight, month, bmr)
        report += f"MONTH {month}\nACTIVITY LEVELS:\n"
        for level, multiplier in activity_multipliers.items():
            report += f"    {level}: Eat {round(daily_caloric_intake * multiplier)} each day\n"
        report += "\n"

    with open("calorie_report.txt", "w") as file:
        file.write(report)

def get_valid_input(prompt, input_type, min_value=None, max_value=None):
    while True:
        try:
            value = input_type(input(prompt))
            if min_value is not None and value < min_value:
                print(f"{Fore.RED}Invalid input. Value must be at least {min_value}.{Fore.RESET}")
            elif max_value is not None and value > max_value:
                print(f"{Fore.RED}Invalid input. Value must be at most {max_value}.{Fore.RESET}")
            else:
                return value
        except ValueError:
            print(f"{Fore.RED}Invalid input. Please enter a valid {input_type.__name__}.{Fore.RESET}")

# Example usage
age = get_valid_input(f"Enter your {Fore.BLUE}age: {Fore.RESET}", int, 13, 80)
os.system("cls")
reset()

weight = get_valid_input(f"Enter your {Fore.BLUE}weight{Fore.RESET} in pounds: {Fore.RESET}", float, 30, 300)
os.system("cls")
reset()
height_feet = get_valid_input(f"Enter your {Fore.BLUE}height{Fore.RESET} ({Fore.MAGENTA}feet part{Fore.RESET}): ", int, 3, 7)
os.system("cls")
reset()
height_inches = get_valid_input(f"Enter your {Fore.BLUE}height{Fore.RESET} ({Fore.MAGENTA}inches part{Fore.RESET}): ", int, 0, 11)
os.system("cls")
reset()
while True:
    gender = input(f"Enter your {Fore.BLUE}gender{Fore.RESET} (male/female): {Fore.RESET}").lower()
    if gender in ['male', 'female']:
        break
    else:
        print(f"{Fore.RED}Invalid input. Please specify 'male' or 'female'.{Fore.RESET}")
os.system("cls")
reset()
bmr = calculate_bmr(weight, height_feet, height_inches, age, gender)
print(f"{Fore.YELLOW}Your BMR is: {Fore.MAGENTA}{bmr}{Fore.RESET}")

target_weight = get_valid_input(f"Enter your {Fore.BLUE}target weight{Fore.RESET} in pounds: {Fore.RESET}", float, 30, 300)
os.system("cls")
reset()

generate_report(weight, target_weight, height_feet, height_inches, gender, bmr)
print(f"{Fore.YELLOW}Report generated and saved to 'calorie_report.txt'.{Fore.RESET}")

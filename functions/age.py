from datetime import datetime
from dateutil.relativedelta import relativedelta

# Sofia's age in nanoseconds
def calculate_age_in_nanoseconds(dob: str) -> int: #dob is in YYYY-MM-DD

    # Convert the input date string to a datetime
    birth_date = datetime.strptime(dob, "%Y-%m-%d")
    
    current_time = datetime.now()
    
    age_timedelta = current_time - birth_date
    
    # to nanoseconds
    age_in_nanoseconds = age_timedelta.total_seconds() * 1e9
    
    return int(age_in_nanoseconds)


# Sofia's age in years, months, weeks, days, hours
def calculate_age(dob: str) -> str: #dob is in YYYY-MM-DD. Returns: str: The age in 'X years, Y months, Z weeks, W days, H hours' format.

    # Convert the input date string to a datetime object
    birth_date = datetime.strptime(dob, "%Y-%m-%d %H:%M:%S") if " " in dob else datetime.strptime(dob, "%Y-%m-%d")
    
    # Get the current date and time
    current_date = datetime.now()
    
    # Calculate the difference between the current date and the birth date
    age = relativedelta(current_date, birth_date)
    
    # Calculate total number of days between current date and birth date
    total_days = (current_date - birth_date).days
    
    # Calculate the number of weeks (7 days = 1 week)
    total_weeks = total_days // 7
    remaining_days = total_days % 7  # Remaining days after calculating full weeks
    
    # If remaining days are more than 3, consider them as 1 more month
    if remaining_days >= 21:  # If there are 3 weeks or more, treat it as 1 month
        age.months += 1
        remaining_days -= 21  # Subtract 3 weeks (21 days)
    
    # Calculate the difference in hours
    hours = current_date.hour - birth_date.hour
    if hours < 0:
        hours += 24
        remaining_days -= 1  # Adjust the remaining days if hours go negative
    
    # Format the result as a string
    age_str = f"{age.years} yrs, {age.months} mths, {total_weeks % 4} wks, {remaining_days} days, {hours} hrs"
    
    return age_str
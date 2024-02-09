from datetime import date, datetime, timedelta


def get_birthdays_per_week(users):
    if not users:
        return {}
    # We determine the current date and the week after it
    today = date.today()
    next_week = today + timedelta(days=7)

    # We create dictionaries of days of the week (without weekends) and birthdays
    weekday = {0: 'Monday', 1: 'Tuesday', 2: 'Wednesday', 3: 'Thursday', 4: 'Friday'}
    birthdays_dict = {day: [] for day in weekday.values()}

    # We sort birthdays according to requirements and add birthday people to the dictionary
    for user in users:
        name = user['name'].split()[0]
        birthday = user['birthday'].replace(year=today.year)

        if birthday < today:
            birthday = birthday.replace(year=today.year + 1)
        if today <= birthday <= next_week:
            day_of_week = birthday.strftime("%A")
            if day_of_week not in weekday.values():
                day_of_week = "Monday"
            birthdays_dict[day_of_week].append(name)

    birthdays_dict = {day: names for day, names in birthdays_dict.items() if names}
    return birthdays_dict


if __name__ == "__main__":
    users = [
        {"name": "Jan Koum", "birthday": datetime(1976, 2, 13).date()},
    ]

    result = get_birthdays_per_week(users)
    print(result)
    # We derive the result
    for day_name, names in result.items():
        print(f"{day_name}: {', '.join(names)}")

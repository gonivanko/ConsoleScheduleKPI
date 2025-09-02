from Config import Config
from TablePrinter import TablePrinter
from CampusAPI import CampusAPI
from ChosenSubjects import ChosenSubjects

from datetime import datetime
from babel.dates import format_datetime


def greeting(current_time):

    now = datetime.now()

    current_week = current_time['currentWeek']

    print('Привіт')
    print(f'Сьогодні {format_datetime(now, "EEEE, d MMMM y, Час: HH:mm", locale="uk")}')
    print(f"Поточний тиждень навчання: {current_week}")

def get_day_week(current_time):
    current_week = current_time['currentWeek']
    current_day = current_time['currentDay']

    next_day = current_day % 7 + 1
    next_week = current_week
    if next_day == 1:
        next_week = current_week % 2 + 1

    return current_week, current_day, next_week, next_day

def menu(schedule, current_time, tp: TablePrinter):

    current_week, current_day, next_week, next_day = get_day_week(current_time)

    running = True

    while running: 

        print("="*50)
        print("Меню:")
        print("0 | Перегляд розкладу за поточний тиждень")
        print("1 | Перегляд розкладу за наступний тиждень")
        print("2 | Перегляд розкладу за обидва тижні")
        print("3 | Перегляд розкладу за сьогоднішній день")
        print("4 | Перегляд розкладу за завтрішній день")
        print("="*50)

        choice = input("Обери варіант, будь ласка (0, 1, 2, 3, 4): ")

        match (choice):
            case "1":
                tp.print_week(schedule, (current_week) % 2 + 1)
            case "2":
                tp.print_week(schedule, 1)
                tp.print_week(schedule, 2)
            case "3":
                tp.print_day(schedule, current_week, current_day)
            case "4":
                tp.print_day(schedule, next_week, next_day)
            case "q":
                running = False
            case _:
                tp.print_week(schedule, current_week)
    return


def main():
    current_time = CampusAPI.current_time()
    
    greeting(current_time)

    config = Config.load()

    schedule = None
    try:
        schedule = CampusAPI.group_schedule(config['groupId'])
    except Exception as e:
        print(f"Помилка. Розклад порожній або недоступний.")
        return

    subjects = ChosenSubjects.load_from(config['subjects_file_path'])


    tp = TablePrinter(config, subjects)

    menu(schedule, current_time, tp)


if __name__ == "__main__":
    main()


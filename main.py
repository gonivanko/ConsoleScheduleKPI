from Config import Config
from TablePrinter import TablePrinter
from CampusAPI import CampusAPI
from ChosenSubjects import ChosenSubjects


def main():

    config = Config.load()

    schedule = None
    try:
        schedule = CampusAPI.group_schedule(config['groupId'])
    except Exception as e:
        print(f"Помилка. Розклад порожній або недоступний.")
        return

    subjects = ChosenSubjects.load_from(config['subjects_file_path'])

    tp = TablePrinter(config)
    tp.print_week(schedule, 0, subjects)
    tp.print_week(schedule, 1, subjects)

    input("\nНатисни Enter, щоб закрити програму...")


if __name__ == "__main__":
    main()


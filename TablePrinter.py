import shutil
import textwrap

from tabulate import tabulate

class TablePrinter:

    def __init__(this, config, chosen_subjects):
        this.config = config
        this.chosen_subjects = chosen_subjects

        term_width = shutil.get_terminal_size().columns

        this.col_width = (term_width - 29) // 2 - 2
    
    def _get_pair_number(this, pair_time: str) -> int:
        pair_times = this.config['PAIR_TIMES']
        return pair_times.get(pair_time, -1)
    
    def _get_day_name(this, day):
        return this.config['day_names'].get(day['day'])

    def _wrap_text(this, text, width):
        return "\n".join(textwrap.wrap(str(text), width=width)) if text else ""
    
    def _get_day_pairs(this, day):
        pairs = []
        for pair in day["pairs"]:
            if pair['name'] in this.chosen_subjects.values:
                pairs.append(pair)
        return pairs
    
    def _get_table(this, day):
        table = []
        pairs = this._get_day_pairs(day)
        for pair in pairs:
            # if pair['name'] in this.chosen_subjects.values:
            table.append([
                this._get_pair_number(pair['time']),
                this._wrap_text(pair['time'], 8),
                this._wrap_text(pair['type'], 4),
                this._wrap_text(pair['name'], this.col_width),
                this._wrap_text(pair['teacherName'], this.col_width),
                this._wrap_text(pair['dates'], 14)
            ])
        return table
    
    def _print_day(this, day):
        if day["pairs"]:
            print(this._get_day_name(day))
            table = this._get_table(day)
            print(tabulate(table, headers=this.config['table_headers'], tablefmt="grid"))
            print()
        else:
            print("Немає пар")

    def print_day(this, schedule_data, week_number: int, day_number: int):

        print("\nТиждень", week_number)

        week_name = this.config['week_api_names'][week_number - 1]

        this._print_day(schedule_data[week_name][day_number-1])

    def print_week(this, schedule_data, week_number: int):

        print("\nТиждень", week_number)

        week_name = this.config['week_api_names'][week_number - 1]

        for day in schedule_data[week_name]:
            this._print_day(day)
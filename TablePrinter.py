import shutil
import textwrap

from tabulate import tabulate

class TablePrinter:

    def __init__(this, config):
        this.config = config
    
    def _get_pair_number(this, pair_time: str) -> int:
        pair_times = this.config['PAIR_TIMES']
        return pair_times.get(pair_time, -1)

    def _wrap_text(this, text, width):
        return "\n".join(textwrap.wrap(str(text), width=width)) if text else ""

    def print_week(this, schedule_data, week_number: int, chosen_subjects):
        print("\nТиждень", week_number + 1)

        week_name = this.config['week_api_names'][week_number]
        
        term_width = shutil.get_terminal_size().columns

        col_width = (term_width - 13) // 2 - 2

        for day in schedule_data[week_name]:
            if day["pairs"]:
                print(f"\n{this.config['day_names'].get(day['day'])}")
                table = []
                for pair in day["pairs"]:
                    if pair['name'] in chosen_subjects.values:
                        table.append([
                            this._get_pair_number(pair['time']),
                            this._wrap_text(pair['time'], 8),
                            this._wrap_text(pair['type'], 4),
                            this._wrap_text(pair['name'], col_width),
                            this._wrap_text(pair['teacherName'], col_width),
                        ])
                print(tabulate(table, headers=this.config['table_headers'], tablefmt="grid"))
            # else:
            #     print("Немає пар")
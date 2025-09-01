import json
import os
from CampusAPI import CampusAPI

class Config:

    CONFIG_PATH = "config/config.json"

    DEFAULT_CONFIG = {
        "PAIR_TIMES": {
            "08:30:00": 1,
            "10:25:00": 2,
            "12:20:00": 3,
            "14:15:00": 4,
            "16:10:00": 5,
            "18:30:00": 6,
            "20:20:00": 7
        },
        "day_names": {
            "Пн": "Понеділок",
            "Вв": "Вівторок",
            "Ср": "Середа",
            "Чт": "Четвер",
            "Пт": "П'ятниця",
            "Сб": "Субота"
        },
        "week_api_names": ["scheduleFirstWeek", "scheduleSecondWeek"],
        "table_headers": ["#", "Час", "Тип", "Предмет", "Викладач"],
        "subjects_file_path": "config/subjects.csv",
        "groupId": ""
    }

    @classmethod
    def _get_group_id(this):
        group_name = input("Введи назву групи (наприклад, ІП-23): ")
        group_id = CampusAPI.find_group_id(group_name)

        if group_id:
            this.DEFAULT_CONFIG["groupId"] = group_id
        else:
            raise Exception(f'Групу {group_name} не знайдено')
        
    @classmethod    
    def _save(this, path: str = CONFIG_PATH):
        os.makedirs(os.path.dirname(path) or ".", exist_ok=True)

        with open(path, "w", encoding="utf-8") as f:
            json.dump(this.DEFAULT_CONFIG, f, ensure_ascii=False, indent=4)

        print(f"Створено новий файл конфігурації: {path}")

    @classmethod
    def create(this, path: str = CONFIG_PATH):
        running = not os.path.exists(path)
        while (running):
            try:
                this._get_group_id()
                running = False
            except Exception as e:
                print(f"{e}. Спробуйте, будь ласка, ще раз")
        this._save()
    
    @classmethod
    def load(this, path: str = CONFIG_PATH):
        if not os.path.exists(path):
            this.create()
        """Завантажує конфігурацію, або створює файл з дефолтними значеннями."""
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)

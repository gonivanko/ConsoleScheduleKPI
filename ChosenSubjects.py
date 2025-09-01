import os
import pandas as pd


class ChosenSubjects:

    csv_column_name = "subjects"
    mykpi_column_name = "Н/Д (О/К)"

    @classmethod
    def _get_from_html(this, table_html: str) -> pd.core.series.Series:

        table = pd.read_html(table_html)[0].dropna()    

        subjects = table[this.mykpi_column_name]
        subjects = subjects.str.replace(r"\s*\(.*?\)", "", regex=True)
        subjects.name = this.csv_column_name

        return subjects
    
    @classmethod
    def _save(this, subjects: pd.core.series.Series, directory:str, filename:str):
        os.makedirs(directory, exist_ok=True)
        subjects.to_csv(os.path.join(directory, filename), index=False)

    @classmethod
    def load_from(this, file_path):

        filename = os.path.basename(file_path)
        directory_path = os.path.dirname(file_path)

        running = (not os.path.exists(file_path))

        while running:
            table_html = input("Введіть html таблиці із сторінки https://my.kpi.ua/room/educhoose/index?inp: ")
            print(table_html)
            subjects = pd.Series()
            try:
                subjects = this._get_from_html(table_html)
                this._save(subjects, directory_path, filename)
                print(type(subjects))
                running = False
            except Exception as e:
                print(f'Помилка: {e}. Спробуйте, будь ласка, ще раз')

        return pd.read_csv(file_path)[this.csv_column_name]
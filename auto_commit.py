import datetime
import os

FILE_PATH = "daily_commit.txt"

# Записываем текущую дату в файл
with open(FILE_PATH, "a") as file:
    file.write(f"Коммит от {datetime.datetime.now()}\n")

# Делаем git-коммит
os.system("git add .")
os.system('git commit -m "Автоматический коммит"')
os.system("git push")

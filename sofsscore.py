import kagglehub
import os
import shutil

# مجلد التخزين النهائي
DATA_DIR = os.path.join(os.getcwd(), "data")
os.makedirs(DATA_DIR, exist_ok=True)

# تحميل مجموعة بيانات اللاعبين
players_path = kagglehub.dataset_download("maso0dahmed/football-players-data")
players_target = os.path.join(DATA_DIR, "football-players-data")
shutil.move(players_path, players_target)
print("✅ Players dataset saved to:", players_target)

# تحميل مجموعة بيانات الدوريات
leagues_path = kagglehub.dataset_download("kamrangayibov/football-data-european-top-5-leagues")
leagues_target = os.path.join(DATA_DIR, "european-top-5-leagues")
shutil.move(leagues_path, leagues_target)
print("✅ Leagues dataset saved to:", leagues_target)

# تحميل مجموعة بيانات الأحداث
events_path = kagglehub.dataset_download("secareanualin/football-events")
events_target = os.path.join(DATA_DIR, "football-events")
shutil.move(events_path, events_target)
print("✅ Events dataset saved to:", events_target)

'''
Purpose: Downloads and organizes football datasets.
How it works:
Imports required libraries.
Sets up the data directory.
Downloads three datasets from Kaggle using kagglehub.
Moves the downloaded datasets to the specified data directory.
Prints confirmation messages after each dataset is saved.
'''
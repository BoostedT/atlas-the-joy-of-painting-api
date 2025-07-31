import csv
import ast
import psycopg2
from datetime import datetime

# DATABASE CONNECTION
conn = psycopg2.connect(
    dbname="joy_of_painting",
    user="postgres",
    password="pass213",
    host="localhost"
)
cursor = conn.cursor()

def parse_date(title_line):
    if '(' not in title_line:
        return title_line.strip(), None
    title, date_str = title_line.rsplit('(', 1)
    title = title.strip(' ")')
    try:
        air_date = datetime.strptime(date_str.strip(' )\n'), '%B %d, %Y').date()
    except:
        air_date = None
    return title, air_date

episode_dates = {}
with open("datasets/episodes.csv", encoding="utf-8") as f:
    for line in f:
        title, air_date = parse_date(line)
        episode_dates[title.lower()] = air_date

colors_set = set()
episode_color_map = {}
episode_info_map = {}

with open("datasets/colors.csv", encoding="utf-8") as f:
    reader = csv.DictReader(f)
    for row in reader:
        title = row["painting_title"].strip()
        episode_key = title.lower()
        season = int(row["season"])
        episode = int(row["episode"])
        img = row["img_src"]
        video = row["youtube_src"]

        episode_info_map[episode_key] = {
            "title": title,
            "season": season,
            "episode": episode,
            "image_url": img,
            "video_url": video,
        }

        color_names = ast.literal_eval(row["colors"])
        hex_codes = ast.literal_eval(row["color_hex"])
        for name, hex_code in zip(color_names, hex_codes):
            clean_name = name.strip().lower()
            colors_set.add((clean_name, hex_code))
            episode_color_map.setdefault(episode_key, []).append(clean_name)

subject_set = set()
episode_subject_map = {}

with open("datasets/subject.csv", encoding="utf-8") as f:
    reader = csv.DictReader(f)
    for row in reader:
        title = row["TITLE"].strip().strip('"')
        episode_key = title.lower()
        for subject, value in row.items():
            if subject in ["EPISODE", "TITLE"]:
                continue
            if value == '1':
                clean_subject = subject.strip().lower()
                subject_set.add(clean_subject)
                episode_subject_map.setdefault(episode_key, []).append(clean_subject)

color_id_map = {}
for name, hex_code in colors_set:
    cursor.execute("""
        INSERT INTO colors (name, hex_code)
        VALUES (%s, %s)
        ON CONFLICT (name) DO NOTHING
        RETURNING id
    """, (name, hex_code))
    result = cursor.fetchone()
    if result:
        color_id_map[name] = result[0]
    else:
        cursor.execute("SELECT id FROM colors WHERE name = %s", (name,))
        color_id_map[name] = cursor.fetchone()[0]

subject_id_map = {}
for name in subject_set:
    cursor.execute("""
        INSERT INTO subjects (name)
        VALUES (%s)
        ON CONFLICT (name) DO NOTHING
        RETURNING id
    """, (name,))
    result = cursor.fetchone()
    if result:
        subject_id_map[name] = result[0]
    else:
        cursor.execute("SELECT id FROM subjects WHERE name = %s", (name,))
        subject_id_map[name] = cursor.fetchone()[0]

episode_id_map = {}
for key, data in episode_info_map.items():
    air_date = episode_dates.get(key)
    cursor.execute("""
        INSERT INTO episodes (title, season, episode, air_date, image_url, video_url)
        VALUES (%s, %s, %s, %s, %s, %s)
        RETURNING id
    """, (data["title"], data["season"], data["episode"], air_date, data["image_url"], data["video_url"]))
    episode_id_map[key] = cursor.fetchone()[0]

for key, color_list in episode_color_map.items():
    eid = episode_id_map.get(key)
    for cname in color_list:
        cid = color_id_map.get(cname)
        if eid and cid:
            cursor.execute("""
                INSERT INTO episode_colors (episode_id, color_id)
                VALUES (%s, %s)
                ON CONFLICT DO NOTHING
            """, (eid, cid))

for key, subject_list in episode_subject_map.items():
    eid = episode_id_map.get(key)
    for sname in subject_list:
        sid = subject_id_map.get(sname)
        if eid and sid:
            cursor.execute("""
                INSERT INTO episode_subjects (episode_id, subject_id)
                VALUES (%s, %s)
                ON CONFLICT DO NOTHING
            """, (eid, sid))

conn.commit()
cursor.close()
conn.close()
print("ETL completed. Data loaded into PostgreSQL.")

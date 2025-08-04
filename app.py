from flask import Flask, request, jsonify
import psycopg2
from psycopg2.extras import RealDictCursor

app = Flask(__name__)

# Connect to DB
conn = psycopg2.connect(
    dbname="joy_of_painting", user="postgres", password="pass213", host="localhost"
)


@app.route("/episodes", methods=["GET"])
def get_episodes():
    params = request.args
    colors = params.getlist("color")
    subjects = params.getlist("subject")
    months = params.getlist("month")
    title = params.get("title")
    match_all = params.get("match", "any") == "all"

    base_query = """
        SELECT DISTINCT e.id, e.title, e.season, e.episode, e.air_date
        FROM episodes e
        LEFT JOIN episode_colors ec ON e.id = ec.episode_id
        LEFT JOIN colors c ON ec.color_id = c.id
        LEFT JOIN episode_subjects es ON e.id = es.episode_id
        LEFT JOIN subjects s ON es.subject_id = s.id
    """

    values = []
    all_conditions = []

    if months:
        placeholders = ','.join(['%s'] * len(months))
        all_conditions.append(f"EXTRACT(MONTH FROM e.air_date) IN ({placeholders})")
        values.extend(list(map(int, months)))

    optional_conditions = []

    if colors:
        optional_conditions.append("LOWER(c.name) = ANY(%s)")
        values.append([color.lower() for color in colors])

    if subjects:
        optional_conditions.append("LOWER(s.name) = ANY(%s)")
        values.append([subject.lower() for subject in subjects])

    if title:
        optional_conditions.append("LOWER(e.title) = %s")
        values.append(title.lower())

    if optional_conditions:
        logic = " AND " if match_all else " OR "
        all_conditions.append("(" + logic.join(optional_conditions) + ")")
    
    all_conditions.append("e.air_date IS NOT NULL")

    if all_conditions:
        base_query += " WHERE " + " AND ".join(all_conditions)

    with conn.cursor(cursor_factory=RealDictCursor) as cur:
        cur.execute(base_query, values)
        episodes = cur.fetchall()

    return jsonify(episodes)

if __name__ == "__main__":
    app.run(debug=True)

from flask import Flask, request, jsonify
import psycopg2
from psycopg2.extras import RealDictCursor

app = Flask(__name__)

# Connect to DB
conn = psycopg2.connect(
    dbname="joy_of_painting",
    user="postgres",
    password="pass213",
    host="localhost"
)

@app.route('/episodes', methods=['GET'])
def get_episodes():
    params = request.args
    colors = params.getlist('color')
    subjects = params.getlist('subject')
    months = params.getlist('month')
    match_all = params.get('match', 'any') == 'all'

    base_query = """
        SELECT DISTINCT e.id, e.title, e.season, e.episode, e.air_date
        FROM episodes e
        LEFT JOIN episode_colors ec ON e.id = ec.episode_id
        LEFT JOIN colors c ON ec.color_id = c.id
        LEFT JOIN episode_subjects es ON e.id = es.episode_id
        LEFT JOIN subjects s ON es.subject_id = s.id
    """

    conditions = []
    values = []

    if months:
        conditions.append("EXTRACT(MONTH FROM e.air_date) = ANY(%s)")
        values.append(list(map(int, months)))

    if colors:
        conditions.append("LOWER(c.name) = ANY(%s)")
        values.append([color.lower() for color in colors])

    if subjects:
        conditions.append("LOWER(s.name) = ANY(%s)")
        values.append([subject.lower() for subject in subjects])

    if conditions:
        connector = " AND " if match_all else " OR "
        base_query += " WHERE " + connector.join(conditions)

    with conn.cursor(cursor_factory=RealDictCursor) as cur:
        cur.execute(base_query, values)
        episodes = cur.fetchall()

    return jsonify(episodes)

if __name__ == '__main__':
    app.run(debug=True)

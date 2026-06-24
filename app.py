from flask import Flask, render_template
import psycopg2
import psycopg2.extras

app = Flask(__name__)

DB_CONN = "dbname=smart_parking user=parking_admin password=12345 host=localhost"

def get_db_connection():
    return psycopg2.connect(DB_CONN)

@app.route('/')
def dashboard():
    conn = get_db_connection()
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    
    # Current status per slot (latest session per slot)
    cur.execute("""
        SELECT car_id, slot_number, entry_time, exit_time, fee,
               CASE WHEN exit_time IS NULL THEN 'occupied' ELSE 'vacant' END AS status
        FROM parking_sessions
        WHERE (slot_number, entry_time) IN (
            SELECT slot_number, MAX(entry_time)
            FROM parking_sessions
            GROUP BY slot_number
        )
        ORDER BY slot_number;
    """)
    current_status = cur.fetchall()
    
    # Dashboard statistics

    cur.execute("""
        SELECT COUNT(*)
        FROM parking_sessions
        WHERE exit_time IS NULL
    """)
    occupied_slots = cur.fetchone()[0]

    total_slots = 2

    available_slots = total_slots - occupied_slots

    cur.execute("""
        SELECT COALESCE(SUM(fee), 0)
        FROM parking_sessions
    """)
    total_revenue = cur.fetchone()[0]

    # Recent history (last 20 sessions)
    cur.execute("""
        SELECT car_id, slot_number, entry_time, exit_time, fee
        FROM parking_sessions
        ORDER BY entry_time DESC LIMIT 20;
    """)
    recent_sessions = cur.fetchall()
    
    cur.close()
    conn.close()
    
    return render_template(
        'dashboard.html',
        current_status=current_status,
        recent_sessions=recent_sessions,
        occupied_slots=occupied_slots,
        available_slots=available_slots,
        total_revenue=total_revenue
    )



if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
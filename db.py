from sqlite3 import connect
from werkzeug.security import generate_password_hash

DB_NAME = "database.db"

def execute_query(query, many, *params):
    conn = connect(DB_NAME)
    params = list(map(str, params))
    cur = conn.execute(query, params)
    res = cur.fetchall() if many else cur.fetchone()
    conn.commit()
    conn.close()
    print("res", res)
    return res

def execute_update(query, *params):
    conn = connect(DB_NAME)
    conn.execute("PRAGMA foreign_keys = ON;")
    params = list(map(str, params))
    cur = conn.execute(query, params)
    rowid = cur.lastrowid
    conn.commit()
    conn.close()
    return rowid

def insert_otp(token, otp):
    query = "insert into otp_requests values(?, ?)"
    execute_update(query, token, otp)

def validate_otp(token, received_otp):
    original_otp = execute_query("select otp from otp_requests where token = ?", False, token)
    if not original_otp:
        return False
    original_otp = original_otp[0]
    execute_update("delete from otp_requests where token = ?", token)
    return original_otp == received_otp

def add_user(name, email, password, is_student):
    pass_hash = generate_password_hash(password)
    query = "insert into users (email, name, password_hash, is_student) values (?, ?, ?, ?)"
    return execute_update(query, email, name, pass_hash, 1 if is_student else 0)

def select_faculty():
    query = "select id, name from users where is_student = 0"
    return execute_query(query, True)

def insert_complaint(sid, fid, title, body):
    query = "insert into complains (sid, fid, title, body) values (?, ?, ?, ?)"
    return execute_update(query, sid, fid, title, body)

def select_student_complaints(sid):
    query = "select complains.id, users.name, title, body, status from complains join users on complains.fid = users.id and sid = ?"
    return execute_query(query, True, sid)

def select_faculty_complaints(fid):
    query = "select complains.id, users.name, title, body, status from complains join users on complains.sid = users.id and fid = ?"
    return execute_query(query, True, fid)

def update_status(cid, status):
    query = "update complains set status = ? where id = ?"
    return execute_update(query, status, cid)

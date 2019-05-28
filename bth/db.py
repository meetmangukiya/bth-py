import datetime
import os
import sqlite3


class DB:
    def __init__(self):
        self._dirpath = os.path.expanduser(os.path.join('~', '.bth'))
        os.makedirs(self._dirpath, exist_ok=True)
        self._path = os.path.join(self._dirpath, 'bth.db')
        self.create_tables()

    def connection(self):
        conn = sqlite3.connect(self._path, detect_types=sqlite3.PARSE_DECLTYPES)
        return conn

    def create_tables(self):
        with self.connection() as conn:
            curs = conn.cursor()
            stmts = [
                ('CREATE TABLE IF NOT EXISTS projects('
                 '   name    TEXT,'
                 '   id      INTEGER PRIMARY KEY AUTOINCREMENT)'),
                ('CREATE TABLE IF NOT EXISTS sessions('
                 '   start   DATETIME,'
                 '   end     DATETIME,'
                 '   pid     INTEGER,'
                 '   sid     INTEGER PRIMARY KEY AUTOINCREMENT,'
                 '   FOREIGN KEY(pid) REFERENCES projects(id))'),
                ('CREATE TABLE IF NOT EXISTS currently_active('
                 '   pid      INTEGER,'
                 '   sid      INTEGER,'
                 '   FOREIGN KEY(sid) REFERENCES sessions(sid),'
                 '   FOREIGN KEY(pid) REFERENCES projects(id))')
            ]
            for stmt in stmts:
                curs.execute(stmt)
            conn.commit()

    def add_project(self, name):
        with self.connection() as conn:
            curs = conn.cursor()
            curs.execute('INSERT INTO projects(name) VALUES(?)', (name, ))
            conn.commit()

    def add_session(self, start, pid, end=None):
        with self.connection() as conn:
            curs = conn.cursor()
            curs.execute('INSERT INTO sessions(start, pid, end) VALUES(?, ?, ?)', (start, pid,
                end))
            conn.commit()
            return curs.execute('SELECT sid FROM sessions WHERE start=? AND pid=?',
                    (start, pid)).fetchone()[0]

    def end_session(self, sid):
        with self.connection() as conn:
            curs = conn.cursor()
            curs.execute('UPDATE sessions SET end=? WHERE sid=?',
                    (datetime.datetime.now(), sid))

    def get_session(self, sid=None, pid=None):
        with self.connection() as conn:
            curs = conn.cursor()
            single = False
            if sid:
                single = True
                curs.execute('SELECT start, end, pid, sid FROM sessions WHERE sid=?',
                             (sid, ))
            elif pid:
                curs.execute('SELECT start, end, pid, sid FROM sessions WHERE pid=? ORDER BY start',
                             (pid, ))
            res = []
            for start, end, pid, sid in curs:
                if isinstance(start, str):
                    start = datetime.datetime.fromisoformat(start)
                if isinstance(end, str):
                    end = datetime.datetime.fromisoformat(end)
                res.append((start, end, pid, sid))
            if single:
                return res[0]
            else:
                return res

    def get_projects(self):
        with self.connection() as conn:
            curs = conn.cursor()
            curs.execute('SELECT name, id FROM projects')
            return curs.fetchall()

    def get_currently_active(self):
        with self.connection() as conn:
            curs = conn.cursor()
            return curs.execute('SELECT pid, sid FROM currently_active').fetchone()

    def get_project(self, idd):
        with self.connection() as conn:
            curs = conn.cursor()
            return curs.execute('SELECT name, id FROM projects WHERE id=?',
                    (idd, )).fetchone()

    def set_currently_active(self, pid, sid):
        with self.connection() as conn:
            curs = conn.cursor()
            curs.execute('INSERT INTO currently_active(pid, sid) VALUES(?,?)', (pid, sid))
            conn.commit()

    def start(self, idd):
        with self.connection() as conn:
            curs = conn.cursor()
            if self.get_currently_active():
                return False
            sid = self.add_session(datetime.datetime.now(), idd)
            self.set_currently_active(idd, sid)
            return True

    def stop(self):
        (pid, sid) = self.get_currently_active() or (None, None)
        if pid:
            with self.connection() as conn:
                curs = conn.cursor()
                curs.execute('DELETE FROM currently_active')
                conn.commit()
            self.end_session(sid)
        return pid, sid

db = DB()

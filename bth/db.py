import datetime
import os
import sqlite3

import sqlalchemy
from sqlalchemy import and_, create_engine, Boolean, Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()

class Project(Base):
    __tablename__ = 'projects'

    name = Column(String)
    id = Column(Integer, autoincrement=True, primary_key=True)


class Session(Base):
    __tablename__ = 'sessions'

    start = Column(DateTime, nullable=False)
    end = Column(DateTime)
    pid = Column(Integer, ForeignKey(Project.id))
    sid = Column(Integer, autoincrement=True, primary_key=True)
    paid = Column(Boolean, nullable=False, default=False)


class CurrentlyActive(Base):
    __tablename__ = 'currently_active'

    pid = Column(Integer, ForeignKey(Project.id))
    sid = Column(Integer, ForeignKey(Session.sid), primary_key=True)



class DB:
    def __init__(self):
        self._dirpath = os.path.expanduser(os.path.join('~', '.bth'))
        os.makedirs(self._dirpath, exist_ok=True)
        self._path = os.path.join(self._dirpath, 'bth.db')
        self._engine = create_engine(f'sqlite:///{self._path}')
        Base.metadata.create_all(self._engine)
        self._Session = sessionmaker(bind=self._engine)
        self._session = self._Session()

    def add_project(self, name):
        project = Project(name=name)
        self._session.add(project)
        self._session.commit()

    def add_session(self, start, pid, end=None):
        session = Session(start=start, pid=pid)
        self._session.add(session)
        self._session.commit()
        session = self._session.query(Session).filter(and_(Session.start == start,
            Session.pid == pid)).first()
        return session.sid

    def end_session(self, sid):
        session = self._session.query(Session).filter(Session.sid == sid).first()
        session.end = datetime.datetime.now()
        self._session.commit()

    def get_session(self, sid=None, pid=None):
        single = False

        if sid:
            single = True
            query = self._session.query(Session).filter(Session.sid == sid)
        if pid:
            query = self._session.query(Session).filter(Session.pid == pid).order_by(Session.pid)

        res = []

        for session in query:
            res.append((session.start, session.end, session.pid, session.sid,
                session.paid))

        if single:
            return res[0]
        else:
            return res

    def get_projects(self):
        return [(project.name, project.id) for project in self._session.query(Project)]

    def get_currently_active(self):
        active = self._session.query(CurrentlyActive).first()
        if active:
            return active.pid, active.sid

    def get_project(self, idd):
        project = self._session.query(Project).filter(Project.id == idd).first()
        return project.name, project.id

    def set_currently_active(self, pid, sid):
        active = CurrentlyActive(pid=pid, sid=sid)
        self._session.add(active)
        self._session.commit()

    def set_session_paid_status(self, paid, sid=None, pid=None):
        if sid:
            sessions = self._session.query(Session).filter(Session.sid ==
                    sid)
        if pid:
            sessions = self._session.query(Session).filter(Session.pid == pid)
        for sess in sessions:
            sess.paid = paid
            self._session.add(sess)
        self._session.commit()

    def start(self, idd):
        if self.get_currently_active():
            return False
        sid = self.add_session(datetime.datetime.now(), idd)
        self.set_currently_active(idd, sid)
        return True

    def stop(self):
        (pid, sid) = self.get_currently_active() or (None, None)
        if pid:
            self._session.query(CurrentlyActive).delete()
            self._session.commit()

            self.end_session(sid)
        return pid, sid

    def close(self):
        self._session.close()

db = DB()

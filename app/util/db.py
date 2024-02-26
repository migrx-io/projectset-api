import sqlite3
from app.util.sql import (
    CREATE_TASKS,
    CREATE_PROJECTSET,
    CREATE_PROJECTSET_TEMPLATE,
    CREATE_TASKS_IDX,
    CREATE_PROJECTSET_IDX,
    CREATE_PROJECTSET_TEMPLATE_IDX,
)

from pathlib import Path
# import logging as log


def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d


class DB:

    def __init__(self):
        self.db = None
        self._connect()
        self._init_db()

    def _connect(self):
        # self.db = sqlite3.connect("file::memory:?cache=shared", check_same_thread=False)
        self.db = sqlite3.connect(f"{Path.cwd()}/config/app.db",
                                  check_same_thread=False)
        self.db.row_factory = dict_factory

    def _init_db(self):

        with self.db as con:
            cur = con.cursor()
            cur.execute(CREATE_TASKS)
            cur.execute(CREATE_PROJECTSET)
            cur.execute(CREATE_PROJECTSET_TEMPLATE)

            cur.execute(CREATE_TASKS_IDX)
            cur.execute(CREATE_PROJECTSET_IDX)
            cur.execute(CREATE_PROJECTSET_TEMPLATE_IDX)

    def get_conn(self):
        return self.db

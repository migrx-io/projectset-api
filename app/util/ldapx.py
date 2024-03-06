import logging as log
import ldap
import os
import yaml
import json
import threading
import time
# from app import db
from app.util.db import DB


def sync_ldap(args):
    threading.Thread(target=_sync_ldap, args=(args, ), daemon=True).start()


def _sync_ldap(args):

    db = args[0]

    while True:

        log.info("start sync ldap..")

        try:
            ld = Ldap()

            users = ld.load_users()

            with db.get_conn() as con:

                for u in users:

                    log.debug("load user : %s", u)

                    con.execute("""
                                DELETE FROM users WHERE id = '{}'
                                """.format(u["id"]))

                    con.execute("""
                                INSERT OR IGNORE INTO users(id, username, email, groups)
                                VALUES ('{}', '{}', '{}', '{}')
                                """.format(u["id"], u["username"], u["email"],
                                           json.dumps(u["groups"])))

        except Exception as e:
            log.error("_sync_ldap: %s", e)

        log.debug("sleep...")
        time.sleep(int(os.environ.get("PWORKERS_SLEEP", "15")))


def ldap_auth(username, password):

    db = DB()

    # get projectset and tasks
    with db.get_conn() as con:

        sql = """SELECT id, username, groups
                 FROM users
                 WHERE username = '{}'""".format(username)

        log.debug("sql: %s", sql)

        ps = con.execute(sql)

        for p in ps:

            log.debug("p: %s", p)

            try:

                ld = Ldap()
                ld.connect(p["id"], password)

                return True, {"groups": json.loads(p["groups"])}

            except Exception as e:
                log.error(e)

                return False, "Invalid credentials"

        return False, "Invalid credentials"


class Ldap:

    def __init__(self):

        # read config
        with open(os.environ.get("APP_CONF", "app.yaml"),
                  'r',
                  encoding="utf-8") as file:

            data = yaml.safe_load(file)

            log.debug("get_envs: data: %s", data)

            envs = data.get("auth", {}).get("ldap", {})

            log.debug("get_envs: %s", envs)

            # read config and
            self.server = envs

        self.con = None

    def connect(self, user, passwd):

        # if user is None set -
        if user is None:
            user = "-"

        log.debug("ldap params: %s", self.server)

        ldap.set_option(ldap.OPT_X_TLS_REQUIRE_CERT, ldap.OPT_X_TLS_NEVER)

        self.con = ldap.initialize(self.server["url"])

        self.con.set_option(ldap.OPT_REFERRALS, 0)
        self.con.simple_bind_s(user, passwd)

        log.debug("connection: %s", self.con)

    def get_user_mappings(self):

        m = self.server.get("userSearch", {})
        return m.get("user_map")

    def get_group_mappings(self):

        m = self.server.get("groupSearch", {})
        return m.get("group_map")

    def load_groups(self):

        groups = self.con.search_s(
            self.server["groupSearch"]["baseDN"], ldap.SCOPE_SUBTREE,
            self.server.get("groupSearch", {}).get("filter"),
            ['memberUid', 'cn', "member"])

        user_group = {}

        for g in groups:
            log.debug("load_groups: g: %s", g)

            g = g[1]

            # check group is dict
            if not isinstance(g, dict):
                continue

            users = g.get("member", [])
            for u in users:

                u = u.decode("utf-8")
                gr = g["cn"][0].decode("utf-8")
                if user_group.get(u) is None:
                    user_group[u] = {gr}
                else:
                    user_group[u].add(gr)

        return user_group

    def load_users(self):

        self.connect(self.server["bindDN"], self.server["bindPW"])

        groups = self.load_groups()
        log.debug("loaded groups: %s", groups)

        map_gr = self.get_group_mappings()

        objs = self.con.search_s(
            self.server["userSearch"]["baseDN"], ldap.SCOPE_SUBTREE,
            self.server.get("userSearch", {}).get("filter"))

        rows = []
        for o in objs:
            row = {"id": o[0]}
            log.debug("objs: o: %s", o)

            # check group is dict
            if not isinstance(o[1], dict):
                continue

            for k, v in self.get_user_mappings().items():

                log.debug("get_user_mappings: k: %s v: %s", k, v)

                val = o[1].get(v)

                if val is not None:
                    row[k] = val[0].decode("utf-8")

            # log.debug(map_gr)
            # log.debug(groups)

            row["groups"] = [map_gr.get(x) for x in groups.get(o[0], [])]

            if row.get("username") is not None and row.get(
                    "email") is not None:
                rows.append(row)

        return rows

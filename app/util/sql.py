# SCHEMA

CREATE_TASKS = """CREATE TABLE IF NOT EXISTS
                                            tasks(
                                                  uuid text,
                                                  op text,
                                                  status text,
                                                  error text,
                                                  date_begin timestamp,
                                                  date_end timestamp)
               ;"""

CREATE_PROJECTSET = """CREATE TABLE IF NOT EXISTS
                                                  projectset(
                                                        uuid text,
                                                        repo text,
                                                        env text,
                                                        name text,
                                                        template text,
                                                        labels text,
                                                        annotations text,
                                                        data text)
               ;"""

CREATE_PROJECTSET_TEMPLATE = """CREATE TABLE IF NOT EXISTS
                                                  projectset_template(
                                                        uuid text,
                                                        repo text,
                                                        env text,
                                                        name text,
                                                        labels text,
                                                        annotations text,
                                                        data text)
               ;"""

# SCHEMA

CREATE_TASKS = """CREATE TABLE IF NOT EXISTS
                                            tasks(
                                                  uuid text,
                                                  op text,
                                                  status text,
                                                  error text,
                                                  date_begin timestamp,
                                                  date_end timestamp);
                """

CREATE_TASKS_IDX = """
    CREATE UNIQUE INDEX IF NOT EXISTS tasks_idx ON tasks(uuid); 
               """

CREATE_PROJECTSET = """CREATE TABLE IF NOT EXISTS
                                                  projectset(
                                                        uuid text,
                                                        repo text,
                                                        env text,
                                                        name text,
                                                        template text,
                                                        labels text,
                                                        annotations text,
                                                        data text);
                    """

CREATE_PROJECTSET_IDX = """                    
    CREATE UNIQUE INDEX IF NOT EXISTS projectset_idx ON projectset(uuid); 
               """

CREATE_PROJECTSET_TEMPLATE = """CREATE TABLE IF NOT EXISTS
                                                  projectset_template(
                                                        uuid text,
                                                        repo text,
                                                        env text,
                                                        name text,
                                                        labels text,
                                                        annotations text,
                                                        data text);
                              """



CREATE_PROJECTSET_TEMPLATE_IDX = """  
    CREATE UNIQUE INDEX IF NOT EXISTS projectset_template_idx ON projectset_template(uuid); 

"""

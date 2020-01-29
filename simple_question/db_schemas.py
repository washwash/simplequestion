import sqlite3


__all__ = ['Action', 'User']


class DB:
    class manager:
        def __init__(self):
            self.conn = sqlite3.connect('sq.db')
            self.cursor = self.conn.cursor()

        def __enter__(self):
            return self

        def __exit__(self, type, value, traceback):
            self.conn.close()

        def execute(self, sql):
            res = self.cursor.execute(sql)
            self.conn.commit()
            return res

    def execute(self, sql):
        with self.manager() as m:
            res = m.execute(sql).fetchall()
        return res

    def insert(self, sql):
        with self.manager() as m:
            res = m.execute(sql).lastrowid
        return res


class Executor:

    def __init__(self, db=None):
        self._db = db or DB()


class Action(Executor):
    
    def __init__(self, *args):
        super().__init__(*args)
        self._db.execute('''
            CREATE TABLE IF NOT EXISTS "action" (
                "id" INTEGER PRIMARY KEY AUTOINCREMENT,
                "what" TEXT,
                "user" INTEGER,
                "at" REAL,
                FOREIGN KEY(user) REFERENCES user(id),
                CONSTRAINT Check_ActionType CHECK (what in ('from', 'to'))
            );
        ''')

    def insert(self, what, user, at):
        if not isinstance(at, (int, )):
            raise ValueError(
                f'"at" should be a timestamp. {type(at)} recieved'
            )
        return self._db.insert(f'''
            INSERT INTO "action" ("what", "user", "at")
            VALUES ("{what}",  "{user}", "{at}");
        '''
        )


class User(Executor):

    def __init__(self, *args):
        super().__init__(*args)
        self._db.execute('''
            CREATE TABLE IF NOT EXISTS "user" (
                "id" INTEGER PRIMARY KEY AUTOINCREMENT,
                "name" TEXT CHECK("name" != ''),
                UNIQUE("name")
            );
        ''')

    def insert(self, name):
        record =  self._db.execute(f'''
            SELECT id
            FROM user
            WHERE "name"="{name}";
        ''')
        return (record and record[0][0]) or self._db.insert(f'''
            INSERT INTO "user" ("name")
            VALUES ("{name}");
        '''
        )


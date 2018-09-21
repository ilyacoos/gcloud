#import sqlite3

DATABASE_FILE = "statistic.db"
ERROR = 1
RECORDSET = 0
STATEMENT = -1

class Database:
    def connect(self, dbFile = DATABASE_FILE):
        self._con = sqlite3.connect(dbFile)

    def commit(self):
        self._con.commit()

    def close(self, commitOnClose = False):
        if commitOnClose: self.DB.commit()
        self._con.close()

    def query(self, SQL, commitOnExec = False):
        _ret = 0
        _msg = "Completed"
        _heads = 0
        _data = 0

        try:
            _cur = self._con.execute(SQL)
            if type(_cur.description) == tuple:
                _heads = tuple([desc[0] for desc in _cur.description])
                _data = tuple([desc for desc in _cur])
                _ret = RECORDSET
            else:
                _ret = STATEMENT

            if commitOnExec:
                self._con.commit()
        except Exception as e:
            _ret = ERROR
            _msg = e.message
        
        return (_ret, _msg, _heads, _data)

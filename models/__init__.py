from db import Db
    
class Model:
    def __init__(self):
        """Sets the db engine and session."""
        self.engine = Db.engine
        self.session = Db.session

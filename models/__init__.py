import traceback
from db import Db


class Model(object):

    def __init__(self):
        """Sets the db engine and session."""
        self.engine = Db.engine
        self.session = Db.session

        try:
            self.metadata.create_all(self.engine)
        except:
            print "Error: Could not connect to database."
            print traceback.print_exc()

    def save(self):
        try:
            self.session.add(self)
            self.session.commit()
            self.session.close()
        except:
            self.session.rollback()
            print traceback.print_exc()

    def initialize_table(self):
        # temporary, until there's an easier setup interface
        try:
            self.metadata.create_all(self.engine)
        except:
            print "Error: Could not connect to database."
            print traceback.print_exc()

        self.session.commit()
        self.session.close()

import traceback
from db import Db


class Model(object):
    engine = Db.engine
    session = Db.session

    def __init__(self):
        """Sets the db engine and session."""

        try:
            self.metadata.create_all(Model.engine)
        except:
            print "Error: Could not connect to database."
            print traceback.print_exc()

    def save(self):
        try:
            Model.session.add(self)
            Model.session.commit()
            Model.session.close()
        except:
            Model.session.rollback()
            Model.session.close()
            print traceback.print_exc()

    def initialize_table(self):
        # temporary, until there's an easier setup interface
        try:
            self.metadata.create_all(Model.engine)
        except:
            print "Error: Could not connect to database."
            print traceback.print_exc()

        Model.session.commit()
        Model.session.close()

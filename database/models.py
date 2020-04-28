# models.py contains all of the declarative models for our database.
#
# docs => https://docs.sqlalchemy.org/en/13/orm/tutorial.html


# isort: 3rd party imports
import sqlalchemy
import sqlalchemy.ext.declarative as sqlalchemy_declarative

# docs => https://docs.sqlalchemy.org/en/13/orm/tutorial.html#declare-a-mapping
Base = sqlalchemy_declarative.declarative_base()


class User(Base):
    __tablename__ = "users"
    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
    name = sqlalchemy.Column(sqlalchemy.String)

    def __repr__(self):
        return f"<User(name='{self.name}')>"

    def json(self):
        return {
            "id": self.id,
            "name": self.name,
        }

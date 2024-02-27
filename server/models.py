from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import validates
from sqlalchemy_serializer import SerializerMixin

db = SQLAlchemy()


class Station(db.Model):
    __tablename__ = "stations"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False, unique=True)
    city = db.Column(db.String(80))

    @validates("name")
    def validate_name(self, key, value):
        if len(value) >= 3:
            return value
        else:
            raise ValueError("Station name must be at least 3 characters")

    platforms = db.relationship("Platform", back_populate="station")

    def __repr__(self):
        return f"<Station {self.name}>"


class Platform(db.Model):
    __tablename__ = "platforms"

    id = db.Column(db.Integer, primary_key=True)
    platform_num = db.Column(db.Integer)
    station_id = db.Column(db.Integer, db.ForeignKey("stations.id"))

    station = db.relationship("Station", back_populate="platforms")
    assignments = db.relationship("Assignments", back_populate="platform")

    @validates("platform_num")
    def validate_platform_num(self, key, value):
        if 1 <= value <= 20:
            return value
        else:
            raise ValueError("Platform number must be between 1 and 20")

    def __repr__(self):
        return f"<Platform {self.name}>"


class Train(db.Model):
    __tablename__ = "trains"

    id = db.Column(db.Integer, primary_key=True)
    train_num = db.Column(db.String)
    service_type = db.Column(db.String)
    origin = db.Column(db.String, nullable=False)
    destination = db.Column(db.String, nullable=False)

    assingments = db.relationship("Assignment", back_populate='Train')

    @validates("origin", "destination")
    def validate_locatons(self, key, value):
        if 3 <= len(value) <= 24:
            return value
        else:
            raise ValueError("Station name must be between 3 and 24 characters long")

    @validates("service_type")
    def validate_service_type(self, key, value):
        valid_service = ["express", "local"]
        if value in valid_service:
            return value
        else:
            raise ValueError("Service type must be either express or local")

    def __repr__(self):
        return f"<Train {self.name}>"


class Assignment(db.Model):
    __tablename__ = "assignments"

    id = db.Column(db.Integer, primary_key=True)
    arrival_time = db.Column(db.DateTime)
    departure_time = db.Column(db.DateTime)
    train_id = db.Column(db.Integer, db.ForeignKey("trains.id"))
    platform_id = db.Column(db.Integer, db.ForeignKey("platforms.id"))

    platform = db.relationship("Platform", back_populates="assignments")
    train = db.relationship("Train", back_populates="assingments")

    @validates("arrival_time", "departure_time")
    def validates_time(self, key, value):
        if value is None:
            raise ValueError("Times must be present")
        else:
            return value

    def __repr__(self):
        return f"<Assignment Train No: {self.train.train_num} Platform: {self.platform.platform_num}>"
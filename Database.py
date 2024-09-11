from sqlalchemy import Column, Integer, String, DateTime, Double, Sequence

from sqlalchemy.orm import declarative_base

Base = declarative_base()


class MeteoData(Base):
    __tablename__ = 'MeteoData'

    id = Column(Integer, Sequence("meteodata_id_sequence"), primary_key=True)
    taken_time = Column(DateTime)

    temperature = Column(Integer)

    wind_direction = Column(String(10))  # N / E / S / W and combinations
    wind_speed = Column(Double)  # m/s

    air_pressure = Column(Double)  # mmHg

    precipitation_type = Column(String(100))
    precipitation_amount = Column(Integer)  # millimeters

    def __repr__(self) -> str:
        return (
            f"<MeteoData(ID={self.id}; TakenAt={self.taken_time}; "
            f"Temperature={self.temperature}; "
            f"Wind={self.wind_direction} at {self.wind_speed} m/s; "
            f"AirPressure={self.air_pressure}mmHg; "
            f"Precipitation={self.precipitation_type}, {self.precipitation_amount}mm)>"
        )


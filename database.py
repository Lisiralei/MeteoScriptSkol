from datetime import datetime

from sqlalchemy import Integer, String, DateTime, Double, Sequence

from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column

from utils import get_WMO_weather_type, get_wind_direction_from_angle

Base = declarative_base()


class MeteoData(Base):
    __tablename__ = 'MeteoData'

    id: Mapped[int] = mapped_column(primary_key=True)
    taken_time: Mapped[datetime] = mapped_column(DateTime)

    temperature: Mapped[int] = mapped_column(Integer)

    wind_direction: Mapped[float] = mapped_column(Double)  # Wind direction in degrees
    wind_speed: Mapped[float] = mapped_column(Double)  # m/s

    air_pressure: Mapped[float] = mapped_column(Double)  # mmHg

    precipitation_type: Mapped[int] = mapped_column(Integer)
    precipitation_amount: Mapped[int] = mapped_column(Integer)  # millimeters

    def human_readable_precipitation(self) -> str:
        return get_WMO_weather_type(self.precipitation_type)

    def text_from_wind_direction(self) -> str:
        return get_wind_direction_from_angle(self.wind_direction)

    def __repr__(self) -> str:
        return (
            f"<MeteoData(ID={self.id!r}; TakenAt={self.taken_time!r}; "
            f"Temperature={self.temperature!r}; "
            f"Wind={self.text_from_wind_direction()} at {self.wind_speed!r} m/s; "
            f"AirPressure={self.air_pressure!r}mmHg; "
            f"Precipitation={self.human_readable_precipitation()}, {self.precipitation_amount!r}mm)>"
        )


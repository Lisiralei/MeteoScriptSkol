import asyncio
from datetime import datetime

import sqlalchemy as alch
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import async_sessionmaker, AsyncEngine, AsyncSession
from sqlalchemy.ext.asyncio import create_async_engine


import requests

from database import Base, MeteoData
from utils import hectopascal_to_mercury_mm, get_WMO_weather_type


async def init_db() -> (AsyncEngine, AsyncSession):
    engine_obj = create_async_engine(
        f"sqlite+aiosqlite:///meteo_data.db",
        pool_pre_ping=True
    )
    async with engine_obj.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    Session = async_sessionmaker(engine_obj, class_=AsyncSession)

    session_obj = Session()

    return engine_obj, session_obj


data_provider_url = "https://api.open-meteo.com/v1/forecast"

request_parameters = {
    "latitude": 55.698,  # Skoltech latitude and longitude
    "longitude": 37.359,
    "current": [
        "temperature_2m", "precipitation",
        "weather_code", "surface_pressure",
        "wind_speed_10m", "wind_direction_10m"
    ],

    "&timezone": "Europe%2FMoscow"
}


async def request_function() -> MeteoData or None:
    # await response
    response = requests.get(
        data_provider_url,
        params=request_parameters
    )

    if response.status_code == 200:

        data_collected = MeteoData(
            taken_time=datetime.now(),
            temperature=response.json()['current']['temperature_2m'],
            wind_direction=response.json()['current']['wind_direction_10m'],
            wind_speed=response.json()['current']['wind_speed_10m'],
            air_pressure=hectopascal_to_mercury_mm(response.json()['current']['surface_pressure']),
            precipitation_type=response.json()['current']['weather_code'],
            precipitation_amount=response.json()['current']['precipitation'],
        )
        return data_collected

    return


async def data_collection_routine(session: AsyncSession, run_delay: int) -> None:
    data_collected = await request_function()
    if data_collected:
        async with session.begin():
            session.add(data_collected)
            await session.commit()

    await asyncio.sleep(run_delay)


async def meteo_data_collector(run_delay: int, times_to_run: int = 0) -> None:
    engine, session = await init_db()

    times_to_run = int(times_to_run)
    run_delay = int(run_delay)
    if times_to_run:
        for i in range(times_to_run):
            await data_collection_routine(session, run_delay)

    else:  # Assume infinite run amount
        while True:
            await data_collection_routine(session, run_delay)




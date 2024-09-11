import asyncio
from datetime import datetime

import sqlalchemy as alch
from sqlalchemy.orm import sessionmaker

from Database import MeteoData

engine = alch.engine.create_engine("sqlite://Lisiralei:all@localhost/meteo_data")
Session = sessionmaker(bind=engine)

session = Session()


async def request_function() -> MeteoData:
    # await response
    response = {  # TODO Implement outgoing request
        'temp': 1,
        'windsp': 2,
        'winddir': 'NW',
        'airprs': 760,
        'preciptype': 'hail',
        'precipamount': 1000
    }

    data_collected = MeteoData(
        taken_time=datetime.now(),
        temperature=response['temp'],
        wind_direction=response['winddir'],
        wind_speed=response['windsp'],
        air_pressure=response['airprs'],
        precipitation_type=response['preciptype'],
        precipitation_amount=response['precipamount'],
    )
    return data_collected


async def data_collection_routine(run_delay: int) -> None:
    data_collected = asyncio.run(request_function())
    session.add(data_collected)
    session.commit()
    await asyncio.sleep(run_delay)


def meteo_data_collector(run_delay: int, times_to_run: int = 0) -> None:
    if times_to_run:
        for i in range(times_to_run):
            asyncio.run(data_collection_routine(run_delay))

    else:  # Assume infinite run amount
        while True:
            asyncio.run(data_collection_routine(run_delay))




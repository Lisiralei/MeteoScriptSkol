from datetime import datetime
from pathlib import Path

import pandas

from sqlalchemy import select
from sqlalchemy.ext.asyncio import async_sessionmaker, AsyncSession
from sqlalchemy.ext.asyncio import create_async_engine

from database import MeteoData, Base


async def write_data_to_xls(amount_to_write: int = 10) -> None:
    engine = create_async_engine(
        f"sqlite+aiosqlite:///meteo_data.db",
        pool_pre_ping=True
    )

    Session = async_sessionmaker(engine, class_=AsyncSession)

    session = Session()

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    await session.begin()
    data_item_select = select(MeteoData).order_by(MeteoData.id.desc()).limit(amount_to_write)
    data_items = await session.execute(data_item_select)
    await session.close()

    list_items = list()
    for meteo_item in data_items.scalars().all():
        list_items.append(
            {
                'Id': f'{meteo_item.id!r}',
                'Date Taken': f'{meteo_item.taken_time.strftime('%d.%m.%Y')}',
                'Time Taken': f'{meteo_item.taken_time.strftime('%H:%M:%S.%f')}',
                'Temperature, C': f'{meteo_item.temperature!r}',
                'Wind Direction': f'{meteo_item.text_from_wind_direction()}',
                'Wind Speed, m/s': f'{meteo_item.wind_speed!r}',
                'AirPressure, mmHg': f'{meteo_item.air_pressure!r}',
                'Precipitation Type': f'{meteo_item.human_readable_precipitation()}',
                'Precipitation Amount, mm': f'{meteo_item.precipitation_amount!r}mm'
            }
        )

    excel_file_directory = "ExcelFiles"
    Path(excel_file_directory).mkdir(exist_ok=True)

    data_frame = pandas.DataFrame(list_items)
    filename = f"File_{datetime.now():%Y-%m-%d_%H-%M-%S}"
    full_file_name = f"./{excel_file_directory}/{filename}.xlsx"
    writer = pandas.ExcelWriter(full_file_name)

    data_frame.to_excel(writer, index=False)
    writer.close()









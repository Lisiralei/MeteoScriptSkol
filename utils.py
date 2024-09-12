WMO_weather_code_table = {  # a construct to interpret weather codes from the open_meteo API
    0: "Clear sky",
    **dict.fromkeys([1, 2, 3], "Mainly clear, partly cloudy, and overcast"),
    **dict.fromkeys([45, 48], "Fog and depositing rime fog"),
    **dict.fromkeys([51, 53, 55], "Drizzle: Light, moderate, and dense intensity"),
    **dict.fromkeys([56, 57], "Freezing Drizzle: Light and dense intensity"),
    **dict.fromkeys([61, 63, 65], "Rain: Slight, moderate and heavy intensity"),
    **dict.fromkeys([66, 67], "Freezing Rain: Light and heavy intensity"),
    **dict.fromkeys([71, 73, 75], "Snow fall: Slight, moderate, and heavy intensity"),
    77:	"Snow grains",
    **dict.fromkeys([80, 81, 82], "Rain showers: Slight, moderate, and violent"),
    **dict.fromkeys([85, 86], "Snow showers slight and heavy"),
    95: "Thunderstorm: Slight or moderate",
    **dict.fromkeys([96, 99], "Thunderstorm with slight and heavy hail")
}


def hectopascal_to_mercury_mm(hpa_value: float) -> float:  # Convert from hectopascal (hPa) pressure units to mercury mm (mmHg)
    return round(hpa_value * 0.75006, 1)  # Conversion estimate


def get_WMO_weather_type(weather_code: int) -> str:  # return a human_readable type of weather from WMO codes
    return WMO_weather_code_table[weather_code]


def get_wind_direction_from_angle(wind_angle: int) -> str:  # return a text form of wind direction from angle in degrees
    if wind_angle > 337.5:
        return 'Northerly'
    if wind_angle > 292.5:
        return 'North Westerly'
    if wind_angle > 247.5:
        return 'Westerly'
    if wind_angle > 202.5:
        return 'South Westerly'
    if wind_angle > 157.5:
        return 'Southerly'
    if wind_angle > 122.5:
        return 'South Easterly'
    if wind_angle > 67.5:
        return 'Easterly'
    if wind_angle > 22.5:
        return 'North Easterly'
    return 'Northerly'








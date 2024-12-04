from datetime import datetime, timedelta
from fastapi import APIRouter, Depends, Query
from app.models import Steam, Photoresistor, Temperature, Humidity, DewPoint, PIR, SoilHumidity, WaterLevel, Ultrasonic, Button, Buzzer, Fan, Relay, LED, Servo, LCD
from .auth import get_current_user_from_request
from .sensors import get_sensor_history_all
from itertools import groupby
from fastapi import HTTPException
from app.models import get_db
from sqlalchemy.orm import Session

charts_router = APIRouter()

def convert_to_milliseconds(dt: datetime) -> int:
    """Convert datetime to milliseconds since epoch"""
    return int(dt.timestamp() * 1000)

def merge_binned_data(values_data, percentages_data):
    """Merge two lists of binned data based on timestamp"""
    merged = {}
    
    # Create a dictionary with timestamp as key
    for item in values_data:
        merged[item["timestamp"]] = {"value": item["avg_value"]}
    
    # Merge percentage data
    for item in percentages_data:
        if item["timestamp"] in merged:
            merged[item["timestamp"]]["percentage"] = item["avg_value"]
    
    # Convert back to list and sort by timestamp
    return [
        {"timestamp": convert_to_milliseconds(ts), **data}
        for ts, data in sorted(merged.items())
    ]

def bin_sensor_data(items, getter_func, interval: str = "hour"):
    """Bin sensor data by time interval and calculate average values"""
    
    def get_interval_key(timestamp: datetime, interval: str) -> datetime:
        """Get the start of the interval for binning"""
        if interval == "minute":
            return timestamp.replace(second=0, microsecond=0)
        elif interval == "hour":
            return timestamp.replace(minute=0, second=0, microsecond=0)
        elif interval == "day":
            return timestamp.replace(hour=0, minute=0, second=0, microsecond=0)
        return timestamp

    # Sort items by timestamp if not already sorted
    sorted_items = sorted(items, key=lambda x: x.timestamp)
    
    # Group by interval and calculate averages
    binned_data = []
    for timestamp, group in groupby(sorted_items, key=lambda x: get_interval_key(x.timestamp, interval)):
        group_items = list(group)
        avg_value = sum(getter_func(item) for item in group_items) / len(group_items)
        binned_data.append({
            "timestamp": timestamp,
            "avg_value": avg_value
        })
    
    return binned_data

@charts_router.get("/sensors/light/chart")
async def get_light_chart_data(start_time: str | None = Query(None), 
                                 end_time: str | None = Query(None), 
                                 interval: str = Query("hour"), 
                                 db: Session = Depends(get_db),
                                 _=Depends(get_current_user_from_request)):
    if interval not in ["minute", "hour", "day"]:
        raise HTTPException(status_code=400, detail="Invalid interval")
    
    items = get_sensor_history_all(db, Photoresistor, start_time, end_time)
    binned_values = bin_sensor_data(items, lambda x: x.value, interval)
    binned_percentages = bin_sensor_data(items, lambda x: x.percentage, interval)

    # Merge the binned data
    merged_data = merge_binned_data(binned_values, binned_percentages)

    # Convert start_time and end_time to milliseconds for metadata
    start_ms = convert_to_milliseconds(datetime.fromisoformat(start_time.replace('Z', '+00:00'))) if start_time else None
    end_ms = convert_to_milliseconds(datetime.fromisoformat(end_time.replace('Z', '+00:00'))) if end_time else convert_to_milliseconds(datetime.utcnow())
    
    return {
        "data": merged_data,
        "metadata": {
            "start_time": start_ms,
            "end_time": end_ms,
            "interval": interval
        }
    }

@charts_router.get("/sensors/water/chart")
async def get_water_chart_data(start_time: str | None = Query(None),
                                 end_time: str | None = Query(None), 
                                 interval: str = Query("hour"), 
                                 db: Session = Depends(get_db),
                                 _=Depends(get_current_user_from_request)):
    if interval not in ["minute", "hour", "day"]:
        raise HTTPException(status_code=400, detail="Invalid interval")
    
    items = get_sensor_history_all(db, WaterLevel, start_time, end_time)
    binned_values = bin_sensor_data(items, lambda x: x.value, interval)
    binned_percentages = bin_sensor_data(items, lambda x: x.percentage, interval)

    # Merge the binned data
    merged_data = merge_binned_data(binned_values, binned_percentages)

    # Convert start_time and end_time to milliseconds for metadata
    start_ms = convert_to_milliseconds(datetime.fromisoformat(start_time.replace('Z', '+00:00'))) if start_time else None
    end_ms = convert_to_milliseconds(datetime.fromisoformat(end_time.replace('Z', '+00:00'))) if end_time else convert_to_milliseconds(datetime.utcnow())
    
    return {
        "data": merged_data,
        "metadata": {
            "start_time": start_ms,
            "end_time": end_ms,
            "interval": interval
        }
    }

@charts_router.get("/sensors/steam/chart")
async def get_steam_chart_data(start_time: str | None = Query(None), 
                                 end_time: str | None = Query(None), 
                                 interval: str = Query("hour"), 
                                 db: Session = Depends(get_db),
                                 _=Depends(get_current_user_from_request)):
    if interval not in ["minute", "hour", "day"]:
        raise HTTPException(status_code=400, detail="Invalid interval")

    items = get_sensor_history_all(db, Steam, start_time, end_time)
    binned_values = bin_sensor_data(items, lambda x: x.value, interval)
    binned_percentages = bin_sensor_data(items, lambda x: x.percentage, interval)

    # Merge the binned data
    merged_data = merge_binned_data(binned_values, binned_percentages)

    # Convert start_time and end_time to milliseconds for metadata
    start_ms = convert_to_milliseconds(datetime.fromisoformat(start_time.replace('Z', '+00:00'))) if start_time else None
    end_ms = convert_to_milliseconds(datetime.fromisoformat(end_time.replace('Z', '+00:00'))) if end_time else convert_to_milliseconds(datetime.utcnow())
    
    return {
        "data": merged_data,
        "metadata": {
            "start_time": start_ms,
            "end_time": end_ms,
            "interval": interval
        }
    }

@charts_router.get("/sensors/ultrasonic/chart")
async def get_ultrasonic_chart_data(start_time: str | None = Query(None), 
                                      end_time: str | None = Query(None), 
                                      interval: str = Query("hour"), 
                                      db: Session = Depends(get_db),
                                      _=Depends(get_current_user_from_request)):
    if interval not in ["minute", "hour", "day"]:
        raise HTTPException(status_code=400, detail="Invalid interval")
    
    items = get_sensor_history_all(db, Ultrasonic, start_time, end_time)
    binned_values = bin_sensor_data(items, lambda x: x.value, interval)

    # Convert start_time and end_time to milliseconds for metadata
    start_ms = convert_to_milliseconds(datetime.fromisoformat(start_time.replace('Z', '+00:00'))) if start_time else None
    end_ms = convert_to_milliseconds(datetime.fromisoformat(end_time.replace('Z', '+00:00'))) if end_time else convert_to_milliseconds(datetime.utcnow())
    
    return {
        "data": list(map(
            lambda x: {
                "timestamp": convert_to_milliseconds(x["timestamp"]), 
                "value": x["avg_value"], 
                "unit": "cm"
            }, 
            binned_values
        )), 
        "metadata": {
            "start_time": start_ms,
            "end_time": end_ms,
            "interval": interval
        }
    }

@charts_router.get("/sensors/dht11/temperature/chart")
async def get_dht11_temperature_chart_data(start_time: str | None = Query(None), 
                                           end_time: str | None = Query(None), 
                                           interval: str = Query("hour"), 
                                           unit: str = Query("celsius"), 
                                           db: Session = Depends(get_db),
                                           _=Depends(get_current_user_from_request)):
    if interval not in ["minute", "hour", "day"]:
        raise HTTPException(status_code=400, detail="Invalid interval")
    if unit not in ["celsius", "fahrenheit", "kelvin"]:
        raise HTTPException(status_code=400, detail="Invalid unit")
    
    items = get_sensor_history_all(db, Temperature, start_time, end_time)
    binned_values = bin_sensor_data(items, lambda x: getattr(x, unit), interval)

    # Convert start_time and end_time to milliseconds for metadata
    start_ms = convert_to_milliseconds(datetime.fromisoformat(start_time.replace('Z', '+00:00'))) if start_time else None
    end_ms = convert_to_milliseconds(datetime.fromisoformat(end_time.replace('Z', '+00:00'))) if end_time else convert_to_milliseconds(datetime.utcnow())
    
    return {
        "data": list(map(
            lambda x: {
                "timestamp": convert_to_milliseconds(x["timestamp"]), 
                "value": x["avg_value"], 
                "unit": unit
            }, 
            binned_values
        )),
        "metadata": {
            "start_time": start_ms,
            "end_time": end_ms,
            "interval": interval,
            "unit": unit
        }
    }

@charts_router.get("/sensors/dht11/humidity/chart")
async def get_dht11_humidity_chart_data(start_time: str | None = Query(None), 
                                          end_time: str | None = Query(None), 
                                          interval: str = Query("hour"), 
                                          db: Session = Depends(get_db),
                                          _=Depends(get_current_user_from_request)):
    if interval not in ["minute", "hour", "day"]:
        raise HTTPException(status_code=400, detail="Invalid interval")
    
    items = get_sensor_history_all(db, Humidity, start_time, end_time)
    binned_values = bin_sensor_data(items, lambda x: x.value, interval)

    # Convert start_time and end_time to milliseconds for metadata
    start_ms = convert_to_milliseconds(datetime.fromisoformat(start_time.replace('Z', '+00:00'))) if start_time else None
    end_ms = convert_to_milliseconds(datetime.fromisoformat(end_time.replace('Z', '+00:00'))) if end_time else convert_to_milliseconds(datetime.utcnow())
    
    return {
        "data": list(map(
            lambda x: {
                "timestamp": convert_to_milliseconds(x["timestamp"]), 
                "value": x["avg_value"], 
                "unit": "%"
            }, 
            binned_values
        )),
        "metadata": {
            "start_time": start_ms,
            "end_time": end_ms,
            "interval": interval
        }
    }

@charts_router.get("/sensors/dht11/dewpoint/chart")
async def get_dht11_dewpoint_chart_data(start_time: str | None = Query(None), 
                                          end_time: str | None = Query(None), 
                                          interval: str = Query("hour"), 
                                          db: Session = Depends(get_db),
                                          _=Depends(get_current_user_from_request)):
    if interval not in ["minute", "hour", "day"]:
        raise HTTPException(status_code=400, detail="Invalid interval")
    
    items = get_sensor_history_all(db, DewPoint, start_time, end_time)
    binned_values = bin_sensor_data(items, lambda x: x.celsius, interval)

    # Convert start_time and end_time to milliseconds for metadata
    start_ms = convert_to_milliseconds(datetime.fromisoformat(start_time.replace('Z', '+00:00'))) if start_time else None
    end_ms = convert_to_milliseconds(datetime.fromisoformat(end_time.replace('Z', '+00:00'))) if end_time else convert_to_milliseconds(datetime.utcnow())
    
    return {
        "data": list(map(
            lambda x: {
                "timestamp": convert_to_milliseconds(x["timestamp"]), 
                "value": x["avg_value"], 
                "unit": "celsius"
            }, 
            binned_values
        )),
        "metadata": {
            "start_time": start_ms,
            "end_time": end_ms,
            "interval": interval
        }
    }

@charts_router.get("/sensors/soil/chart")
async def get_soil_chart_data(start_time: str | None = Query(None), 
                                end_time: str | None = Query(None), 
                                interval: str = Query("hour"), 
                                db: Session = Depends(get_db),  
                                _=Depends(get_current_user_from_request)):
    if interval not in ["minute", "hour", "day"]:
        raise HTTPException(status_code=400, detail="Invalid interval")
    
    items = get_sensor_history_all(db, SoilHumidity, start_time, end_time)
    binned_values = bin_sensor_data(items, lambda x: x.value, interval)
    binned_percentages = bin_sensor_data(items, lambda x: x.percentage, interval)

    # Convert start_time and end_time to milliseconds for metadata
    start_ms = convert_to_milliseconds(datetime.fromisoformat(start_time.replace('Z', '+00:00'))) if start_time else None
    end_ms = convert_to_milliseconds(datetime.fromisoformat(end_time.replace('Z', '+00:00'))) if end_time else convert_to_milliseconds(datetime.utcnow())
    
    merged_data = merge_binned_data(binned_values, binned_percentages)
    
    return {
        "data": merged_data,
        "metadata": {
            "start_time": start_ms,
            "end_time": end_ms,
            "interval": interval
        }
    }

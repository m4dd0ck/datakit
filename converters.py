"""Unit conversion utilities."""

from typing import Literal


# Temperature
def celsius_to_fahrenheit(c: float) -> float:
    """Convert Celsius to Fahrenheit."""
    return (c * 9 / 5) + 32


def fahrenheit_to_celsius(f: float) -> float:
    """Convert Fahrenheit to Celsius."""
    return (f - 32) * 5 / 9


def celsius_to_kelvin(c: float) -> float:
    """Convert Celsius to Kelvin."""
    return c + 273.15


def kelvin_to_celsius(k: float) -> float:
    """Convert Kelvin to Celsius."""
    return k - 273.15


# Distance
def miles_to_km(miles: float) -> float:
    """Convert miles to kilometers."""
    return miles * 1.60934


def km_to_miles(km: float) -> float:
    """Convert kilometers to miles."""
    return km / 1.60934


def feet_to_meters(feet: float) -> float:
    """Convert feet to meters."""
    return feet * 0.3048


def meters_to_feet(meters: float) -> float:
    """Convert meters to feet."""
    return meters / 0.3048


def inches_to_cm(inches: float) -> float:
    """Convert inches to centimeters."""
    return inches * 2.54


def cm_to_inches(cm: float) -> float:
    """Convert centimeters to inches."""
    return cm / 2.54


# Weight
def lbs_to_kg(lbs: float) -> float:
    """Convert pounds to kilograms."""
    return lbs * 0.453592


def kg_to_lbs(kg: float) -> float:
    """Convert kilograms to pounds."""
    return kg / 0.453592


def oz_to_grams(oz: float) -> float:
    """Convert ounces to grams."""
    return oz * 28.3495


def grams_to_oz(grams: float) -> float:
    """Convert grams to ounces."""
    return grams / 28.3495


# Volume
def gallons_to_liters(gallons: float) -> float:
    """Convert US gallons to liters."""
    return gallons * 3.78541


def liters_to_gallons(liters: float) -> float:
    """Convert liters to US gallons."""
    return liters / 3.78541


def cups_to_ml(cups: float) -> float:
    """Convert US cups to milliliters."""
    return cups * 236.588


def ml_to_cups(ml: float) -> float:
    """Convert milliliters to US cups."""
    return ml / 236.588


# Data
def bytes_to_human(num_bytes: int) -> str:
    """Convert bytes to human-readable string."""
    for unit in ["B", "KB", "MB", "GB", "TB", "PB"]:
        if abs(num_bytes) < 1024:
            return f"{num_bytes:.1f} {unit}"
        num_bytes /= 1024
    return f"{num_bytes:.1f} EB"


def human_to_bytes(size_str: str) -> int:
    """Convert human-readable size string to bytes.

    Example: "5 MB" -> 5242880
    """
    units = {"B": 1, "KB": 1024, "MB": 1024**2, "GB": 1024**3, "TB": 1024**4}

    size_str = size_str.strip().upper()
    for unit, multiplier in units.items():
        if size_str.endswith(unit):
            number = float(size_str[: -len(unit)].strip())
            return int(number * multiplier)

    return int(float(size_str))


# Time
def hours_to_seconds(hours: float) -> float:
    """Convert hours to seconds."""
    return hours * 3600


def seconds_to_hours(seconds: float) -> float:
    """Convert seconds to hours."""
    return seconds / 3600


def minutes_to_seconds(minutes: float) -> float:
    """Convert minutes to seconds."""
    return minutes * 60


def seconds_to_minutes(seconds: float) -> float:
    """Convert seconds to minutes."""
    return seconds / 60

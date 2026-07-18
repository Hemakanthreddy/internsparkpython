# Weather Explorer

A command-line Python tool that fetches live weather data for any city using
the free **Open-Meteo API** (no API key required), parses the JSON response,
and lets you search for a city and filter results when the name is ambiguous.

---

## Features

- Fetches real-time weather data using the `requests` module
- Parses JSON responses from two chained API calls (geocoding + forecast)
- Search by city name
- Filter ambiguous matches by country code (`--country`) or state/region (`--admin1`)
- Choose metric or imperial units (`--units`)
- Clean, formatted terminal output

---

## Requirements

- Python 3.8+
- `requests` library

Install the dependency:

```bash
pip install requests
```

---

## How It Works

The script makes two API calls, both through `requests`:

1. **Geocoding API** — `https://geocoding-api.open-meteo.com/v1/search`
   Converts a city name into one or more matching locations (name, country,
   region, latitude, longitude). If more than one place matches (e.g.
   "Springfield" exists in several US states), the results become a
   searchable/filterable list.

2. **Forecast API** — `https://api.open-meteo.com/v1/forecast`
   Takes the chosen location's coordinates and returns current weather:
   temperature, wind speed, wind direction, and a weather condition code.

Both responses are parsed with `.json()` and rendered into a clean,
human-readable summary.

---

## Usage

```bash
# Basic lookup
python weather_explorer.py Hyderabad

# Ambiguous city name -> lists matches, prompts you to pick one
python weather_explorer.py Springfield

# Filter by country code
python weather_explorer.py Springfield --country US

# Filter by state/region
python weather_explorer.py Springfield --admin1 Illinois

# Imperial units (°F, mph)
python weather_explorer.py London --units imperial
```

---

## images output

<img width="1517" height="850" alt="Screenshot 2026-07-18 203258" src="https://github.com/user-attachments/assets/64ae3cea-5421-4a16-9786-c9a97449b538" />

<img width="1536" height="831" alt="Screenshot 2026-07-18 203603" src="https://github.com/user-attachments/assets/b77facb9-6528-422d-ac2b-3cc64be306fb" />



## Project Structure

```
weather_explorer.py   # main script
README.md             # this file
```

---

## Notes

- Open-Meteo is completely free and requires no sign-up or API key.
- If a request fails, check your internet connection — some restricted
  networks (office/college wifi) block outbound API calls.
- Weather codes follow the WMO standard and are mapped to readable
  descriptions inside the script (`WEATHER_CODES` dictionary).

---

## Author

Hemakanth Reddy [LinkedIn](https://linkedin.com/in/hemakanth-reddy)

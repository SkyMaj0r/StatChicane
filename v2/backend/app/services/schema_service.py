"""
app/services/schema_service.py

Provides the F1DB schema string used as LLM context.

The schema is hardcoded as a constant rather than
introspected at runtime — this gives the LLM a stable,
human-readable description of every table and its key
relationships, which produces better SQL than raw
INFORMATION_SCHEMA output.
"""

import logging

logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# F1DB Schema — single source of truth for LLM context
# ---------------------------------------------------------------------------

F1DB_SCHEMA = """
DATABASE: F1DB — All-time Formula 1 Statistics

TABLES:

drivers (driver_id PK, forename, surname, nationality,
  date_of_birth, url)

constructors (constructor_id PK, constructor_ref, name,
  nationality, url)

circuits (circuit_id PK, circuit_ref, name, location,
  country, lat, lng, alt, url)

races (race_id PK, year, round, circuit_id FK, name,
  date, time, url, fp1_date, fp2_date, fp3_date,
  quali_date, sprint_date)

results (result_id PK, race_id FK, driver_id FK,
  constructor_id FK, number, grid, position,
  position_text, position_order, points, laps,
  time, milliseconds, fastest_lap, rank,
  fastest_lap_time, fastest_lap_speed, status_id FK)

qualifying (qualify_id PK, race_id FK, driver_id FK,
  constructor_id FK, number, position, q1, q2, q3)

lap_times (race_id FK, driver_id FK, lap, position,
  time, milliseconds)

pit_stops (race_id FK, driver_id FK, stop, lap,
  time, duration, milliseconds)

driver_standings (driver_standings_id PK, race_id FK,
  driver_id FK, points, position, position_text, wins)

constructor_standings (constructor_standings_id PK,
  race_id FK, constructor_id FK, points, position,
  position_text, wins)

constructor_results (constructor_results_id PK,
  race_id FK, constructor_id FK, points, status)

status (status_id PK, status)

seasons (year PK, url)

sprint_results (sprint_result_id PK, race_id FK,
  driver_id FK, constructor_id FK, number, grid,
  position, position_text, position_order, points,
  laps, time, milliseconds, fastest_lap,
  fastest_lap_time, status_id FK)

KEY RELATIONSHIPS:
- results joins drivers, constructors, races, status
- qualifying joins drivers, constructors, races
- lap_times joins races and drivers
- pit_stops joins races and drivers
- driver_standings joins races and drivers
- constructor_standings joins races and constructors

COMMON QUERY PATTERNS:
- Driver full name: CONCAT(d.forename, ' ', d.surname)
- Season results: JOIN races r ON r.race_id = res.race_id
  WHERE r.year = <year>
- Championship winner: SELECT driver with MAX points
  in driver_standings at final race of season
- Win count: COUNT(*) WHERE position = 1
- Podium count: COUNT(*) WHERE position <= 3
"""


def get_schema() -> str:
    """
    Returns the F1DB schema string for LLM context.

    The schema is a constant — no DB round-trip needed.
    If a dynamic schema is required in future, this
    function is the single place to add caching logic.
    """
    return F1DB_SCHEMA

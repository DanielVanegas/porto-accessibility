from src.build_query_graphql import build_query
from datetime import datetime
import requests

## Travel time query to OTP
def get_time(lat, lon, dest_lat, dest_lon, mode, base_url, datetime_iso):
    query = build_query(mode)

    variables = {
        "fromLat": lat,
        "fromLon": lon,
        "toLat": dest_lat,
        "toLon": dest_lon,
        "dateTime": datetime_iso
    }

    try:
        r = requests.post(
            base_url,
            json={"query": query, "variables": variables},
            timeout=30
        )
        r.raise_for_status()
        data = r.json()

        if "errors" in data:
            print("GRAPHQL ERRORS:", data["errors"])
            return None
        
    except requests.exceptions.RequestException as e:
        print("CONNECTION ERROR:", e)
        return None

    # Case 1: OTP does not return a data
    if "data" not in data or "planConnection" not in data["data"]:
        print("NO PLAN:", data)
        return None

    edges = data["data"]["planConnection"].get("edges", [])

    # Case 2: no feasible routes
    if not edges:
        print("NO ITINERARIES")
        return None

    # Use the first returned itinerary
    # OTP reports duration in seconds; converted to minutes.
    node = edges[0]["node"]

    # accumulate distance and time per mode
    mode_stats = {}
    total_distance = 0
    total_duration = 0

    for leg in node["legs"]:
        mode = leg["mode"]
        distance = leg["distance"]

        stats = mode_stats.setdefault(mode, {
            "distance_m": 0,
            "duration_min": 0
        })

        start_time = leg.get("start", {}).get("scheduledTime")
        end_time = leg.get("end", {}).get("scheduledTime")

        # always accumulate distance
        stats["distance_m"] += distance
        total_distance += distance

        if not start_time or not end_time:
            continue

        start_leg = datetime.fromisoformat(start_time.replace("Z", "+00:00"))
        end_leg = datetime.fromisoformat(end_time.replace("Z", "+00:00"))

        duration_leg = (end_leg - start_leg).total_seconds() / 60

        stats["duration_min"] += duration_leg
        total_duration += duration_leg

    return {
        "total": {
            "distance_m": round(total_distance, 2),
            "duration_min": round(total_duration, 2)
        },
        "by_mode": {
            m: {
                "distance_m": round(v["distance_m"], 2),
                "duration_min": round(v["duration_min"], 2)
            }
            for m, v in mode_stats.items()
        }
    }


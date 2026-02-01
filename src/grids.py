import math
import geopandas as gpd
from shapely.geometry import Polygon


def generate_hex_grid(area_proj, HEX_SIZE, METRIC_CRS):
    # Study area bounding box
    minx, miny, maxx, maxy = area_proj.total_bounds

    # Hexagon geometric parameters
    dx = HEX_SIZE * 3**0.5
    dy = HEX_SIZE * 1.5

    # Hexagon generation
    hexes = []

    y = miny
    row = 0
    while y < maxy + dy:
        x = minx + (dx / 2 if row % 2 else 0)
        while x < maxx + dx:
            hexagon = Polygon([
                (
                    x + HEX_SIZE * math.cos(math.radians(angle)),
                    y + HEX_SIZE * math.sin(math.radians(angle))
                )
                for angle in range(0, 360, 60)
            ])
            hexes.append(hexagon)
            x += dx
        y += dy
        row += 1

    grid_hex = gpd.GeoDataFrame(geometry=hexes, crs=METRIC_CRS)

    return grid_hex

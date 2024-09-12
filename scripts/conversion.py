import geopandas
from os.path import splitext
for x in ["import/25min.geojson", "import/40min.geojson"]:
    name, ext = splitext(x)
    gdf = geopandas.read_file(x).to_file(f'export/{name}.kml', driver='KML')
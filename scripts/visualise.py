from simplekml import Kml, Style
import geopandas as gpd
import pandas as pd
from create_color import color_dic

def main():
    crime_data = pd.read_csv("/workspaces/London-rental-map/build/crime_data.csv")

    # Summarise crime counts between Aug. 2021 - July 2024 in each LSOA region  
    LSOA_series = crime_data.value_counts("LSOA code", dropna = True)
    LSOA_counts = pd.DataFrame(LSOA_series).reset_index()
    LSOA_counts.columns = ['LSOA code', 'crime_counts']

    # Merge two datasets
    districts = gpd.read_file("/workspaces/London-rental-map/import/Lower_Layer_Super_Output_Areas_Dec_2011_Boundaries_Full_Extent_BFE_EW_V3_2022_1537314916368806697.geojson")
    merged_df = districts.merge(LSOA_counts, how = "inner", left_on='LSOA11CD', right_on='LSOA code')

    # Generate area of each region. To ensure precision need to convert crs format to 27700
    proj = merged_df.to_crs(epsg=27700)
    proj["crime_rate"] = proj["crime_counts"] / proj.area
    final_df = proj.to_crs(epsg=4326)

    # Normalise crime rate
    largest_100_df = final_df.nlargest(100, "crime_rate")
    largest_100_df['bins'] = pd.cut(largest_100_df['crime_rate'], 10, labels = range(10))
    largest_100_df = largest_100_df.reset_index()


    kml = Kml()
    style_list = []
    color_dict = color_dic()

    for i in range(10):
        style = Style()
        style.polystyle.color = color_dict[i]
        style.polystyle.outline = 0
        style_list.append(style)

    kml.document.name = "Test"
    for i in range(100):
        if largest_100_df['geometry'][i].geom_type == "Polygon":
            pol = kml.newpolygon(name=str(largest_100_df["LSOA11NM"][i]),
                        outerboundaryis=list(largest_100_df["geometry"][i].exterior.coords))    
            pol.style = style_list[largest_100_df['bins'][i]]
    kml.save("/workspaces/London-rental-map/export/crime_rate.kml")

if __name__ == "__main__":
    main()


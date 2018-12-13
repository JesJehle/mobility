import pandas as pd
import geopandas as gpd


path_eccidents = "../data/accidents/Shapefile/Unfallorte2017_LinRef.shp"

eccidents_2017 = gpd.read_file(path_eccidents)

eccidents_2017.head(1)
eccidents_2017.columns

# TTC_BusDelay
This project aims to analyze the relationship between bus delays and geographic 
location within the Greater Toronto Area (GTA), utilizing bus delay data from the 
Toronto Open Data portal. The goal is to identify areas within the GTA that need 
improvements TTC services. To achieve this, the project leverages geospatial
analysis tools in ArcGIS Pro to visualize and analyze the processed dataset.

# Location_convert.py
To account for incomplete data from partial address given by Data portal, 
geopy is utilized.
## Geopy
Use ArcGis geocodes to get complete address. Uses WGS84 gcs.
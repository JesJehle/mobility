# SuMo - A Monitoring System for Sustainable Mobility

The SuMo project is a collaboration between the University of Freiburg, KIT Karlsruhe, University of Landau and the University of Strasbourg. The project objective is to develop an indicator system which enables to measure the sustainability of mobility systems in the upper Rhine region. Furthermore, the indicator set shall be integrated into an application that can be used by the municipalities to evaluate their mobility systems and support their planning process.

## Structuring of work-packages

* Data review and acquisition.
  * Find required data sources. :+1:
  * Evaluate and review the data according to a set of defined criteria. :question:
  * Acquire, clean and integrate the data into the application. :+1:
* Develop the Indicator System.
  * Define a set of indicators according to a literature review. :question:
  * Review methods to calculate the indicators used in literature. :question:
  * Evaluate different methods with data on an example municipality and choose the best fitting while justifying the selection. :question:


### criteria for data sources
* Availability over the entire project region.
* Easy accessible.
* Dynamic database which is up to date and reflects real-world changes.
* Data quality
* High spatial resolution to allow small-scale analysis.


## literature review of indicator methods


### Walkability index method review

#### leslie 2007 --------------------------------------------------------------------------------

* data: Tax valuation and cadastral (parcel) data, street
centreline data, land use, zoning data, shopping centre location data and census data.

Is computed of:
* __dwelling density__:
  * is then created by dividing the dwelling count by the sum of the residential land area.

* __Street Connectivity__:
  * Intersections are identified from the street centerline data and connectivity is based upon the number of unique street connections at each intersection (or the potential for different route choices available at each intersection)

* __Land use__:
  *  residential, commercial, industrial, recreation and other.
  * The land use categories are further aggregated in an entropy equation.
  * The entropy equation results in a score of 0–1, with 0 representing homogeneity (all land uses are of a single type), and 1 representing heterogeneity (the developed area is evenly distributed among all
land use categories)

* __Net retail area__:
  * It is the gross retail area and the parcel area that are used in this measure as a simple ratio: NRA ¼ - GRA/P, where GRA ¼ gross retail area; and, P ¼ total retail parcel area.
  * , this measure captures the degree to which retail is located near the roadway edge, as is the case in a pedestrian-oriented community, or set behind a sea of parking.

The __walkability index__ is calculated using the above data sets. The 1–10 score for each measure (dwelling density, intersection density, land use and net retail area) is summed for each CCD resulting in a possible score of 4–40.


### Walk Score Methodology ----------------------------------------------------------------------

* Data sources: Business listing data from Google and Localeze, Road network data and park data from Open Street Map, School data from Education.com

Street Smart Walk Score includes:
* Walking routes and distances to amenities
* Road connectivity metrics such as intersection density and block length
* Scores for individual amenity categories

Street Smart Walk Score calculates a score by mapping out the walking distance to
amenities in 9 different amenity categories. In amenity categories where depth of
choice is important, we count multiple amenities in a given category. Categories
are also weighted according to their importance. The distance to a
location, counts, and weights determine a base score of an address, which is then
normalized to a score from 0 to 100. After this, an address may receive a penalty
for having poor pedestrian friendliness metrics, such as having long blocks or low
intersection density.

Following amenities categories, base weights and counts are used:

category [weight][count]
* grocery [3][1], have shown to be drivers of walking and therefore hold the highest weights.
* restaurants - bars [3][10]
* shopping [2][5], retail business such as clothing, shoes, gift shops, specialty food stores, children’s stores
* coffee [2][2]
* banks [1][1]
* parks [1][1]
* schools [1][1]
* books [1][1]
* entertainment [1][1]

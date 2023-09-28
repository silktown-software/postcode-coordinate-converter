# Code Point Open Postcode Conversion Script

This script will download the codepoint open CSV data and convert the Easting and Northing coordinates to Latitudes and Longitudes.

## Pre-requisites

* Python 3.11
* Pip 23.0.1

## Background

The Codepoint Open data has the location data for every postcode. The Coordinate system used is OSGB36 (EPSG 27700) coordinates.
These are Eastings/Northings coordinates and services such as Google Maps and Mapbox use Latitude and Longitude which are WGS84.

## Setup

The tool requires installing [Pandas](https://pandas.pydata.org/) and [PyProj](https://pyproj4.github.io/pyproj/stable/examples.html):  

* Pandas is required to read the CSV quickly. Using the default CSV Reader in Python took many hours to run on my Desktop as the files have 1000s of entries each. 
* PyProj does the projection calculations for the conversion.

To setup do the following in the root of the repository:

`python -m venv venv`

`source venv/bin/activate`

`pip install -r requirements.txt`

## Running

While in the virtual environment is active:

`python convert_coordinates`

Note: This will probably take a few minutes to process. There are a lot of files, each with 10000s of entries.

## TODO

* Process each file on a separate thread using multiprocessing

## References

 * https://stackoverflow.com/questions/57901730/convert-uk-grid-coordinates-x-y-to-latitude-and-longitude
 * https://www.nationalarchives.gov.uk/doc/open-government-licence/version/3/
 * https://www.ordnancesurvey.co.uk/products/code-point-open#technical



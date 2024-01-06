# Code Point Open Postcode Conversion Script

**DISCLAIMER**: This is provided with absolutely no warranty.

This script will download the codepoint open CSV data and convert the Easting and Northing coordinates to Latitudes and Longitudes.

## Pre-requisites

* Python 3.11
* Pip 23.0.1

## Background

The Codepoint Open data has the location data for every postcode. The Coordinate system used is OSGB36 (EPSG 27700) coordinates.
These are Eastings/Northings coordinates and services such as Google Maps and Mapbox use Latitude and Longitude which are WGS84.
There are plenty of services that offer a Geo-lookup via an Address and/or Postcode to Lat Lng lookup, however these usually
hit rate/api usage limits and/or charges. 

## Setup

The tool requires installing [Pandas](https://pandas.pydata.org/) and [PyProj](https://pyproj4.github.io/pyproj/stable/examples.html):  

* Pandas is required to read the CSV quickly. Using the default CSV Reader in Python took many hours to run on my Desktop as the files have 1000s of entries each. 
Using Pandas to load the CSVs this time was reduced to only a few minutes.
* PyProj does the projection calculations for the conversion.

To setup do the following in the root directory of the repository:

`python -m venv venv`

`source venv/bin/activate`

`pip install -r requirements.txt`

## Running

While in the virtual environment is active:

`python convert_coordinates`

This will produce two directories inside the root of the repository.

* `input` - this holds the code point open postcode archive (zip file) and the files of the extracted archive.
* `output` - this directory will be where the updated coordinates are present. Each CSV file is named by the *area code*.

Each file has three columns. The first being the **postcode**, the second being the **latitude**, the third being the **longitude**.

Note: This will probably take a good few minutes to process. There are a lot of files, each with 10000s of entries.

## Accuracy

A spot check the output of the conversion tool with known postcodes using [Google Maps Sample](https://developers.google.com/maps/documentation/javascript/examples/geocoding-reverse) i.e the author's home postcode and other known postcodes to the author. 
The output hasn't been exhaustively checked.

## TODO

* It may speed things up to process each file on a separate thread using multiprocessing.

## References

 * https://stackoverflow.com/questions/57901730/convert-uk-grid-coordinates-x-y-to-latitude-and-longitude
 * https://www.nationalarchives.gov.uk/doc/open-government-licence/version/3/
 * https://www.ordnancesurvey.co.uk/products/code-point-open#technical



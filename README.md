# verloop_weather
A copy of assignment solution

## Created a wrapper API

## The REST service is implemented using FastAPI
##### Official Docs : https://fastapi.tiangolo.com/
### Also need to install uvicorn - which runs a local server to serve api at route localhost:8000

##### Alternate options could use other webservice options also such as django or a light-weight one like flask to implement these routes

### Installation

### Assuming a stable python3 version is installed.

### Install fastapi and uvicorn

``` bash
$ pip install fastapi
```


``` bash
$ pip install uvicorn
```

### To Run : 

``` bash
$ cd to_required_directory_where_the_main_py_file_is

$ uvicorn main:app --reload

```


### Routes

### '/' - root route -> METHOD : GET
#### http://localhost:8000/
```json
{
  "message" "Hello!\nYou have made a request to root route at {some-time-formatted}"
}
```


### '/getCurrentWeather' - to get current weather through weatherapi(rapidapi) <br> -> METHOD : POST ( with payload/request body)
#### http://localhost:8000/getCurrentWeather
<p>
  request body : <br>
  {'city':'new york','output_format':'json'}
  
</p>

```json
{
   "Weather":"10.0 C",
   "Latitude":"40.71",
   "Longitude":"-74.01",
   "City":"New York United States of America"
}
```


### output_format : has been made optional ( if not passed in request - it gives json response by default )
### using a pydantic model - for type saftey and proper management of request body
##### (NOTE) get_weather_data() [main.py]
  - is a helper function which makes a request to original resource of weatherapi
  - with an api key to get the current weather and formats the output as per requested by user

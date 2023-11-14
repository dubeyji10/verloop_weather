from fastapi import FastAPI
import time
import requests
## to make request to weatherapi resource
from pydantic import BaseModel
## for request body
## add logging later for better debugging of request faults

apiKey = 'add-a-valid-api-key-here'

class CityRequested(BaseModel):
    # json={'city':'agra','output_format':'json'}

    city: str
    output_format: str | None=None
    # Use None to make it just optional.
    ## if output format not passed will return json response by default





# Import FastAPI.
# Create an app instance.
# Write a path operation decorator (like @app.get("/")).
# Write a path operation function (like def root(): ... above).
# Run the development server (like uvicorn main:app --reload).


def get_weather_data(cityName,apiKeyPassed,format_requested):
    
    url = "https://weatherapi-com.p.rapidapi.com/current.json"
    querystring = {"q":cityName}
    headers = {
    "X-RapidAPI-Key": apiKeyPassed,
    "X-RapidAPI-Host": "weatherapi-com.p.rapidapi.com"
    }
    response = requests.get(url, headers=headers, params=querystring)
    # print(response.json())
    if response.status_code==200 or response.status_code==202:
        print('request made successfully')
        #print('returned json response')
        #return {'message':response.json()}
        resJson = response.json()
        ## build response as per format
        if format_requested=='xml':
            print('-requested xml format-')
            # return "<xml> pending </xml>"
            return '''
                <?xml version="1.0" encoding="UTF-8"?>
                <root>
                    <Temperature>{}</Temperature>
                    <City>{}</City>
                    <Latitude>{}</Latitude>
                    <Longitude>{}</Longitude>
                </root>
            '''.format(resJson['current']['temp_c'],resJson['location']['name'],resJson['location']['lat'],resJson['location']['lon'])

        else:
            print('-json requested by default-')
            outputJson = {}
            ## all as string in assignment sample??
            outputJson['Weather'] = "{} C".format(resJson['current']['temp_c'])
            outputJson['Latitude'] = "{}".format(resJson['location']['lat'])
            outputJson['Longitude'] =  "{}".format(resJson['location']['lon'])
            outputJson['City'] = "{} {}".format(resJson['location']['name'] , resJson['location']['country'])
            return outputJson
        
    else:
        print('-some error ocurred-')
        resJson = response.json()
        #         print(response.status_code)
        #         print(response.text)
        #         return {'message':response.json()}
        if format_requested=='xml':
            return '''
                <?xml version="1.0" encoding="UTF-8"?>
                <root>
                    <Message>{}</Message>
                    <Error>{}</Error>
                    <StatusCode>{}</StatusCode>
                </root>
            '''.format(resJson['error']['message'],resJson['error']['code'],response.status_code)
            
        else:
            #             return {"message":"error occurred","error":response.status_code,"error_message":response.json()}
            return {
                    "message":resJson['error']['message'],
                    "error":resJson['error']['code'],
                    "status_code":response.status_code
                   }            

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello!\nYou have made a request to root route at {}".format(time.ctime())}


## define post routes for wrapper api
# https://fastapi.tiangolo.com/tutorial/body/



@app.post("/getCurrentWeather")
async def getCurrentWeather(city: CityRequested):
    try:
        # print('you have made a post request to getCurrentWeather \nwith a request body at {}'.format(time.ctime()))
        # print(city)
        ## dict of city request body
        cityRes = city.dict()
        cityNameRequested = cityRes['city']
        responseFormat = cityRes['output_format']
        # cityRes.update({'request recieved at':'{}'.format(time.ctime())})
        # return cityRes
        output = get_weather_data(cityName=cityNameRequested,apiKeyPassed=apiKey,format_requested=responseFormat)
        return output

    except Exception as e:
        print('-some error ocurred-')
        print('-'*100)
        print(e)
        print('-'*100)
        return {'message':'error'}


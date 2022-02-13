import os
import json
import requests
import time
from logs import logger

# Local data updater
data_send_path = os.path.join(os.path.dirname(__file__), "data_send.json")
with open(data_send_path) as file:
    data_send_json = file.read()
    data_send = json.loads(data_send_json)

def try_request(api_url:str, params:dict, send_data:bool=False):
    """Send data to API in Post

    Args:
        params (dictionary): paramns for send to the api endpoint
    """
    
    headers = {'Content-Type': 'application/x-www-form-urlencoded'}

    # Validate params
    if params in data_send:
        logger.info(f"\tSkipped, data already sent to the API.")
        return None

    # Try to send data to api
    try_api_counter = 0
    while True:

        if try_api_counter == 3:
            logger.info(f"\tError in api call, max retries exceeded.")
            return None

        try:
            if send_data:
                # Try to send api data
                res = requests.post(api_url, headers=headers, params=params)

                # Catch 422 response
                if res.status_code == 422:
                    logger.info(f"\tApi call, no save.")
                    break

                res.raise_for_status()
        except:
            try_api_counter += 1
            logger.info(f"\tError in api call, retryng. ({try_api_counter}).. ")
            time.sleep(5)
            continue
        else:
            logger.info(f"\tApi call, done.")

            # Save params in json
            data_send.append(params)

            # Write json param file
            with open(data_send_path, "w") as file:
                data_send_json = json.dumps(data_send)
                file.write(data_send_json)

            break
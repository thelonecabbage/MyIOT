import urequests
from secrets import PARSE_APP_ID, PARSE_REST_API_KEY, PARSE_URL

def device_update_server(id='', settings={},telemetry={'grill':0, 'probes':[0, 0]}):
    url = PARSE_URL
    headers =  {
        'content-type': 'application/json',
        "X-Parse-Application-Id": PARSE_APP_ID,
        "X-Parse-REST-API-Key": PARSE_REST_API_KEY,}  
    print(url)
    print({
        'objectId': id,
        'settings': settings,
        'telemetry': telemetry
    })
    try:
        response = urequests.post(url, json={
            'objectId': id,
            'settings': settings,
            'telemetry': telemetry
        }, headers=headers)
        if response.status_code < 300:
        # print(response.status_code)
        # print(response.json())
            return response.json()
    except:
        pass
    return None

import http.client
import json

def nutritionnix_calorie_api(food_name):
    param = {"query": food_name}
    conn = http.client.HTTPSConnection("trackapi.nutritionix.com")
    headers = {
        'x-app-id': 'aaa7d5cb',
        'x-app-key': '90e31137806ff25301c021cb0d7d21ec',
        'Content-Type': 'application/json',
        'x-remote-user-id': '0'
    }
    conn.request("POST", "/v2/natural/nutrients", json.dumps(param), headers)
    res = conn.getresponse()
    result = res.read()
    data = json.loads(result)
    if res.status==200:
        return True, data["foods"][0]["nf_calories"]
    else:
        return False, 0
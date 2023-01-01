import requests
import urllib3
import json

import pandas as pd

from overall import overall


def main():
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

    auth_url = "https://www.strava.com/oauth/token"

    club_id = 1040081
    club_members_url = f"https://www.strava.com/api/v3/clubs/{club_id}/members"
    club_activities_url = f"https://www.strava.com/api/v3/clubs/{club_id}/activities"

    with open('secrets.json') as json_data:
        secrets = json.loads(json_data.read())
        json_data.close()

    payload = {
        'client_id': "80717",
        'client_secret': secrets['client_secret'],
        'refresh_token': secrets['refresh_token'],
        'grant_type': "refresh_token",        'f': 'json'
    }

    res = requests.post(auth_url, data=payload, verify=False)
    access_token = res.json()['access_token']

    header = {'Authorization': 'Bearer ' + access_token}
    param = {'per_page': 200, 'page': 1}

    # Activities
    club_activities = requests.get(club_activities_url, headers=header, params=param).json()
    break_name = 'Charity Run 1'

    old_runs = pd.read_csv('activities.csv', header=0)
    
    buffer = []
    for run in club_activities:
        run_details = [run['athlete']['firstname'],
                       run['athlete']['lastname'],
                       run['name'],
                       run['distance'],
                       run['moving_time'],
                       run['elapsed_time'],
                       run['total_elevation_gain']]

        if (old_runs == run_details).all(1).any():
            pass
        else:
            print(f"adding {run_details[2]}")
            print(run_details)
            buffer.append(run_details)

        if run["name"] == break_name:
            break

    if buffer:
        new_runs = pd.DataFrame(buffer, index=None)
        new_runs.to_csv('activities.csv', mode='a', header=False, index=False)
    else:
        print("No new runs")


if __name__ == "__main__":
    while True:
        print('running')
        main()
        overall()

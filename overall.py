import pandas as pd


def overall():
    activities = pd.read_csv("activities.csv")

    stats = {}

    for index, run in activities.iterrows():
        user = f"{run['Firstname']} {(run['Lastname']).strip('.')}"
        distance = run['Distance']
        moving_time = run['Moving Time']
        total_elevation_gain = run['Total Elevation Gain']

        if user not in stats:
            stats[user] = [1, distance/1000, total_elevation_gain, moving_time]
        else:
            stats[user][0] += 1
            stats[user][1] = round(stats[user][1] + distance/1000, 2)
            stats[user][2] = round(stats[user][2] + total_elevation_gain, 2)
            stats[user][3] = round(stats[user][3] + moving_time, 2)

    stats_pd = pd.DataFrame.from_dict(stats, orient='index', columns=['Run Count',
                                                                      'Distance(km)',
                                                                      'Elevation Gain (m)',
                                                                      'Moving Time(s)'])

    stats_pd = stats_pd.sort_values(by=['Distance(km)'], ascending=False)
    stats_pd.to_csv("cumc_stats.csv")

    print("Current Standings:")
    print(stats_pd.to_string())

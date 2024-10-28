import datetime
import requests

def iss_passes():
    response = requests.get(
        "https://api.n2yo.com/rest/v1/satellite/visualpasses/25544/56/0/0/5/50",
        params={'apiKey': "33Q884-HFUV8K-SCS3LG-55CU"}
    )
    
    text = response.json()
    total_n_passes = text['info']['passescount']
    passes = []
    for i in range(total_n_passes):
        iss_pass = text['passes'][i]
        passes.append((datetime.datetime.fromtimestamp(iss_pass['startUTC']), 
                      datetime.datetime.fromtimestamp(iss_pass['endUTC'])))
        
    output_passes = [(ta.strftime("%Y-%m-%d %H:%M:%S"), tb.strftime("%Y-%m-%d %H:%M:%S")) for ta, tb in passes]
        
    return output_passes


def time_range(start_time, end_time, number_of_intervals=1, gap_between_intervals_s=0):
    start_time_s = datetime.datetime.strptime(start_time, "%Y-%m-%d %H:%M:%S")
    end_time_s = datetime.datetime.strptime(end_time, "%Y-%m-%d %H:%M:%S")

    if (end_time_s < start_time_s):
        raise ValueError("input end_time is before start_time")
    
    d = (end_time_s - start_time_s).total_seconds() / number_of_intervals + gap_between_intervals_s * (1 / number_of_intervals - 1)
    sec_range = [(start_time_s + datetime.timedelta(seconds=i * d + i * gap_between_intervals_s),
                  start_time_s + datetime.timedelta(seconds=(i + 1) * d + i * gap_between_intervals_s))
                 for i in range(number_of_intervals)]
    return [(ta.strftime("%Y-%m-%d %H:%M:%S"), tb.strftime("%Y-%m-%d %H:%M:%S")) for ta, tb in sec_range]


def compute_overlap_time(range1, range2):
    overlap_time = []
    for start1, end1 in range1:
        for start2, end2 in range2:
            low = max(start1, start2)
            high = min(end1, end2)
            if (high > low):
                overlap_time.append((low, high))
                
    return overlap_time

if __name__ == '__main__':
    from unittest.mock import patch
    with patch.object(requests,'get') as mock_get:
        output_passes = iss_passes()
        print(mock_get.mock_calls)
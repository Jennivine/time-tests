from times import compute_overlap_time, time_range
import pytest
import yaml

def test_backwards_interval():
    expected_message = "input end_time is before start_time"
    with pytest.raises(ValueError, match=expected_message):
        time_range("2010-01-12 12:00:00", "2010-01-12 10:00:00")
        
with open("fixture.yaml", "r") as f:
    data = yaml.safe_load(f)

test_data = []
for case in data:
    case_name = list(case.keys())[0]
    case_value = case[case_name]
    
    time_input_1 = case_value['time_range_1']
    time_1 = time_range(time_input_1['start'], time_input_1['end'], time_input_1['n_intervals'], time_input_1['interval_gap'])
    
    time_input_2 = case_value['time_range_2']
    time_2 = time_range(time_input_2['start'], time_input_2['end'], time_input_2['n_intervals'], time_input_2['interval_gap'])

    expected = [eval(x) for x in case_value['expected']]
    test_data.append((time_1, time_2, expected))
        
@pytest.mark.parametrize("time_1,time_2,expected", [
                                                    (
                                                        time_range("2010-01-12 10:00:00", "2010-01-12 12:00:00"),
                                                        time_range("2010-01-12 10:30:00", "2010-01-12 10:45:00", 2, 60),
                                                        [('2010-01-12 10:30:00', '2010-01-12 10:37:00'), 
                                                         ('2010-01-12 10:38:00', '2010-01-12 10:45:00')]
                                                    ),
                                                    (
                                                        time_range("2010-01-12 10:00:00", "2010-01-12 10:15:00"),
                                                        time_range("2010-01-12 10:20:00", "2010-01-12 10:35:00"),
                                                        []
                                                    ),
                                                    (
                                                        time_range("2010-01-12 10:00:00", "2010-01-12 10:20:00", 3, 60),
                                                        time_range("2010-01-12 10:05:00", "2010-01-12 10:25:00", 2, 60),
                                                        [('2010-01-12 10:05:00', '2010-01-12 10:06:00'), 
                                                        ('2010-01-12 10:07:00', '2010-01-12 10:13:00'),
                                                        ('2010-01-12 10:14:00', '2010-01-12 10:14:30'),
                                                        ('2010-01-12 10:15:30', '2010-01-12 10:20:00')]
                                                    ),
                                                    (
                                                        time_range("2010-01-12 10:00:00", "2010-01-12 10:20:00"),
                                                        time_range("2010-01-12 10:20:00", "2010-01-12 10:25:00"),
                                                        []
                                                    )
                                                    ]
                        )
def test_positive_eval(time_1, time_2, expected):
    assert(compute_overlap_time(time_1, time_2) == expected)

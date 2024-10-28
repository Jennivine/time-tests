from times import compute_overlap_time, time_range
from pytest import raises

def test_backwards_interval():
    with raises(ValueError):
        time_range("2010-01-12 12:00:00", "2010-01-12 10:00:00")

def test_given_input():
    large = time_range("2010-01-12 10:00:00", "2010-01-12 12:00:00")
    short = time_range("2010-01-12 10:30:00", "2010-01-12 10:45:00", 2, 60)
    result = compute_overlap_time(large, short)
    
    expected = [('2010-01-12 10:30:00', '2010-01-12 10:37:00'), 
                ('2010-01-12 10:38:00', '2010-01-12 10:45:00')]
    
    assert(result == expected)
    
def test_no_overlap():
    time_1 = time_range("2010-01-12 10:00:00", "2010-01-12 10:15:00")
    time_2 = time_range("2010-01-12 10:20:00", "2010-01-12 10:35:00")
    
    result = compute_overlap_time(time_1, time_2)
    expected = []
    
    assert(result == expected)
    
def test_multiple_intervals():
    time_1 = time_range("2010-01-12 10:00:00", "2010-01-12 10:20:00", 3, 60)
    time_2 = time_range("2010-01-12 10:05:00", "2010-01-12 10:25:00", 2, 60)
    
    result = compute_overlap_time(time_1, time_2)
    
    expected = [('2010-01-12 10:05:00', '2010-01-12 10:06:00'), 
                ('2010-01-12 10:07:00', '2010-01-12 10:13:00'),
                ('2010-01-12 10:14:00', '2010-01-12 10:14:30'),
                ('2010-01-12 10:15:30', '2010-01-12 10:20:00')]
    
    assert(result == expected)
    
def test_end_as_the_other_starts():
    time_1 = time_range("2010-01-12 10:00:00", "2010-01-12 10:20:00")
    time_2 = time_range("2010-01-12 10:20:00", "2010-01-12 10:25:00")
    
    result = compute_overlap_time(time_1, time_2)
    expected = []
    
    assert(result == expected)
    
    
    
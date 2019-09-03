def has_time_window_overlap(ws1, we1, ws2, we2) -> bool:
    '''
    Compute if two timewindow overlap
    :param ws1: time window 1 start time
    :param we1: time window 1 end time
    :param ws2: time window 2 start time
    :param we2: time window 2 end time
    :return: True if the two time window has overlap, False otherwise
    '''
    latest_start = max(ws1, ws2)
    earliest_end = min(we1, we2)
    delta = earliest_end - latest_start
    if delta > 0:
        return True
    else:
        return False

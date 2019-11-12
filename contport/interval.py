from datetime import datetime, timedelta
import time    
    
ONE_HOUR_IN_MS = 1 * 60 * 60 * 1000

def get_boundary_timestamps(past_hours):
    end_timestamp = int(time.time() * 1000)
    start_timestamp = end_timestamp - int(past_hours) * ONE_HOUR_IN_MS
    return (start_timestamp, end_timestamp)

if __name__ == "__main__":
    print(get_boundary_timestamps("24"))
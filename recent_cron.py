import datetime
import re
from datetime import timedelta

def read_cron_log(file_path):
    with open(file_path, 'r') as file:
        return file.readlines()

def parse_cron_log(lines, time_frame):
    now = datetime.datetime.now()
    recent_entries = []

    cron_regex = re.compile(r'(\w+\s+\d+\s+\d+:\d+:\d+)\s+\w+\s+CRON')

    for line in lines:
        match = cron_regex.search(line)
        if match:
            log_time_str = match.group(1)
            log_time = datetime.datetime.strptime(log_time_str, '%b %d %H:%M:%S')

            # Update year for log time (since the log doesn't include the year)
            log_time = log_time.replace(year=now.year)

            # Check if the log entry is within the specified time frame
            if now - log_time <= time_frame:
                recent_entries.append(line)

    return recent_entries

def main():
    log_file_path = '/var/log/cron'
    time_frame = timedelta(hours=24)

    try:
        log_lines = read_cron_log(log_file_path)
        recent_cron_jobs = parse_cron_log(log_lines, time_frame)

        if recent_cron_jobs:
            print("Recent cron jobs:")
            for entry in recent_cron_jobs:
                print(entry.strip())
        else:
            print("No recent cron jobs found.")

    except FileNotFoundError:
        print(f"Error: The file {log_file_path} was not found.")
    except PermissionError:
        print(f"Error: Permission denied when trying to read {log_file_path}.")

if __name__ == "__main__":
    main()
import dateutil.parser as parser
from datetime import datetime
from io import StringIO
import pytz
import pandas as pd
import sys


def format_time_interval_string(time_interval):
    seconds = time_interval.total_seconds()
    hours = seconds // 3600
    seconds = seconds - (hours * 3600)
    minutes = seconds // 60
    seconds = seconds - (minutes * 60)
    # converting to floating point seconds
    seconds = seconds * 100 / 60  # TODO: account for decimal being a different base
    string = "%d:%02d:%2.3f" % (hours, minutes, seconds)
    return string.replace(".", "")


with open(sys.argv[1], "rb") as myfile:
    input_str = myfile.read()

df_str = StringIO(input_str.decode("utf-8", "replace"))
df = pd.read_csv(df_str, encoding="utf8")

# The Timestamp column should be formatted in ISO-8601 format.
# The Timestamp column should be assumed to be in US/Pacific time;
# please convert it to US/Eastern.
old_timezone = pytz.timezone("US/Pacific")
new_timezone = pytz.timezone("US/Eastern")
df["Timestamp"] = df["Timestamp"].map(
    lambda x: old_timezone.localize(parser.parse(x))
    .astimezone(new_timezone)
    .isoformat()
)

# All ZIP codes should be formatted as 5 digits. If there are less
# than 5 digits, assume 0 as the prefix.
df["ZIP"] = df["ZIP"].map(lambda x: str(x).zfill(5))

# All name columns should be converted to uppercase. There will
# be non-English names.
df["FullName"] = df["FullName"].map(lambda x: x.upper())

# Convert `FooDuration` and `BarDuration` columns to TimeDeltas in
# preparation for the next two normalizing functions.
df["FooDuration"] = pd.to_timedelta(df["FooDuration"])
df["BarDuration"] = pd.to_timedelta(df["BarDuration"])

# The column "TotalDuration" is filled with garbage data. For each
# row, please replace the value of TotalDuration with the sum of
# FooDuration and BarDuration.
df["TotalDuration"] = df["FooDuration"] + df["BarDuration"]
df["TotalDuration"] = df["TotalDuration"].map(lambda x: format_time_interval_string(x))

# The columns `FooDuration` and `BarDuration` are in HH:MM:SS.MS format
# (where MS is milliseconds); please convert them to a floating point
# seconds format.
df["FooDuration"] = df["FooDuration"].map(lambda x: format_time_interval_string(x))
df["BarDuration"] = df["BarDuration"].map(lambda x: format_time_interval_string(x))

df.to_csv(sys.stdout, index=False)

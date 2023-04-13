import json
from datetime import datetime

def write_tweets_to_json(data, d0, path="output/listener_data", format_string="{prefix}.{now.year}{now.month:02d}{now.day:02d}-{now.hour:02d}.{suffix}.json"):
    """
    Writes the given JSON data to a file with a formatted name.

    Parameters:
    - data (str): The JSON data to be written to the file.
    - d0 (datetime): The datetime object to be used to construct the file name.
    - format_string (str): A string containing placeholders for the file name components.
      Default: "{prefix}.{now.year}{now.month:02d}{now.day:02d}-{now.hour:02d}.{suffix}.json"

    Returns:
    - True if the data was written to the file successfully, False otherwise.
    """
    now = datetime.now()
    file_name = format_string.format(prefix="TweetsRawData", suffix="FiltroIstat" + d0.strftime("%Y%m%d-%H"))
    with open(f"{path}/{file_name}", 'a') as tf:
        #tf.write('\n')
        json.dump(json.loads(data), tf)
    return True
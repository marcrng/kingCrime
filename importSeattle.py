import config
import pandas as pd
from sodapy import Socrata
from sqlalchemy import create_engine

# Connect to Socrata data using app_token
client = Socrata("data.seattle.gov",
                 config.app_token)

# Retrieve data from API
results = client.get("tazs-3rd5", limit=9999999999)

# Convert to pandas DataFrame
results_df = pd.DataFrame.from_records(results)

# Connect to SQL database
engine = create_engine(
    "mysql+pymysql://{user}:{pw}@{host}/{db}".format(
        host=config.sql_host,
        db='kc_crime',
        user=config.sql_user,
        pw=config.sql_pass)
)

results_df.to_sql('seattle_cases', engine, index=False)

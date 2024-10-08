BACKGROUND_CODE_EX = """
import pandas as pd
  
df = pd.read_csv('data.csv')
"""

CURR_CODE_EX = """
print(df['RelationshipStatus'])
"""

FERTILITY_DATA_EX = {
    "dataset_description": "A total of 275 women participated in the study for this dataset. Each participant was asked to answer three religiosity items using a 9-point scale. Further, each participant was asked to indicate the typical length of her menstrual cycle, the start date of her last menstrual period, and the start date of her previous menstrual period. In addition, each woman indicated how sure she was about these two start dates, using a 9-point scale. Finally, each woman was asked to indicate her current romantic relationship status with the following four response options: (1) not dating/romantically involved with anyone, (2) dating or involved with only one partner, (3) engaged or living with my partner, and (4) married.",
    "fields": [
        {
            "column": "WorkerID",
            "properties": {
                "dtype": "number",
                "std": 79.52986860293433,
                "min": 1,
                "max": 275,
                "samples": [31, 140, 196],
                "num_unique_values": 275,
                "description": "The unique identifier of a participant.",
            },
        },
        {
            "column": "Rel1",
            "properties": {
                "dtype": "number",
                "std": 3.284246850080361,
                "min": 1,
                "max": 9,
                "samples": [4, 1, 9],
                "num_unique_values": 9,
                "description": "'How much do you believe in God?' 1 \u2013 9",
            },
        },
        {
            "column": "Rel2",
            "properties": {
                "dtype": "number",
                "std": 3.087872913331648,
                "min": 1.0,
                "max": 9.0,
                "samples": [4.0, 2.0, 6.0],
                "num_unique_values": 9,
                "description": "'I see myself as a religiously oriented person.' 1 \u2013 9",
            },
        },
        {
            "column": "Rel3",
            "properties": {
                "dtype": "number",
                "std": 3.333610823065186,
                "min": 1.0,
                "max": 9.0,
                "samples": [3.0, 1.0, 7.0],
                "num_unique_values": 9,
                "description": "'I believe that God or a Higher Power is responsible for my existence.' 1 \u2013 9",
            },
        },
        {
            "column": "Sure1",
            "properties": {
                "dtype": "number",
                "std": 1.5732501786909676,
                "min": 1,
                "max": 9,
                "samples": [4, 7, 9],
                "num_unique_values": 8,
                "description": "In reference to `StartDateofLastPeriod`,  'How sure are you about that date?' 1 \u2013 9.",
            },
        },
        {
            "column": "Sure2",
            "properties": {
                "dtype": "number",
                "std": 2.221975065515302,
                "min": 1,
                "max": 9,
                "samples": [6, 3, 7],
                "num_unique_values": 9,
                "description": "In reference to `StartDateofPeriodBeforeLast`,  'How sure are you about that date?' 1 \u2013 9.",
            },
        },
        {
            "column": "Relationship",
            "properties": {
                "dtype": "number",
                "std": 1.167327837424664,
                "min": 1,
                "max": 4,
                "samples": [1, 2, 3],
                "num_unique_values": 4,
                "description": "Answer to 'What is your current romantic relationship status?' (1) not dating/romantically involved with anyone, (2) dating or involved with only one partner, (3) engaged or living with my partner, (4) married",
            },
        },
        {
            "column": "ReportedCycleLength",
            "properties": {
                "dtype": "number",
                "std": 2.6714983210492633,
                "min": 21.0,
                "max": 38.0,
                "samples": [21.0, 22.0, 26.0],
                "num_unique_values": 17,
                "description": "Answer to 'How many days long are your menstrual cycles? (for most women, the range is between 25-35 days) Keep in mind this is the number of days from the start of one menstrual period to the start of the next menstrual period and NOT the length of your menstrual bleeding.'",
            },
        },
        {
            "column": "DateTesting",
            "properties": {
                "dtype": "date",
                "min": "03/12/12",
                "max": "04/27/12",
                "samples": ["04/06/12", "04/26/12", "03/12/12"],
                "num_unique_values": 13,
                "description": "Date of participant filling in the questionnaire",
            },
        },
        {
            "column": "StartDateofLastPeriod",
            "properties": {
                "dtype": "date",
                "min": "02/06/12",
                "max": "04/26/12",
                "samples": ["02/16/12", "03/01/12", "04/25/12"],
                "num_unique_values": 61,
                "description": "Answer to 'Please give your best estimate of the date on which you started your last period (please be as precise as possible). This date was probably within the last few weeks. Sometimes thinking of where you were when you started your last period helps. For instance, was it on a weekend?, were you at work, was it during a football game?, etc. Please write the date in mm/dd/yyyy format (e.g., 8/18/2012).'",
            },
        },
        {
            "column": "StartDateofPeriodBeforeLast",
            "properties": {
                "dtype": "date",
                "min": "01/03/12",
                "max": "03/29/12",
                "samples": ["01/15/12", "02/04/12", "03/24/12"],
                "num_unique_values": 61,
                "description": "Answer to 'Please give your best estimate of the date on which you started the period before your last period (please be as precise as possible). Please write the date in mm/dd/yyyy format (e.g., 7/18/2012).'",
            },
        },
    ],
    "num_rows": 275,
    "field_names": [
        "WorkerID",
        "Rel1",
        "Rel2",
        "Rel3",
        "Sure1",
        "Sure2",
        "Relationship",
        "ReportedCycleLength",
        "DateTesting",
        "StartDateofLastPeriod",
        "StartDateofPeriodBeforeLast",
    ],
}

ERROR_MSG = """Executed code failed, please reflect the cause of bug and then debug. Truncated to show only last 2000 characters
-------------------
KeyError                                  Traceback (most recent call last)
File ~/miniforge3/envs/AnalysisAgent/lib/python3.9/site-packages/pandas/core/indexes/base.py:3802, in Index.get_loc(self, key, method, tolerance)
   3801 try:
-> 3802     return self._engine.get_loc(casted_key)
   3803 except KeyError as err:

File ~/miniforge3/envs/AnalysisAgent/lib/python3.9/site-packages/pandas/_libs/index.pyx:138, in pandas._libs.index.IndexEngine.get_loc()

File ~/miniforge3/envs/AnalysisAgent/lib/python3.9/site-packages/pandas/_libs/index.pyx:165, in pandas._libs.index.IndexEngine.get_loc()

File pandas/_libs/hashtable_class_helper.pxi:5745, in pandas._libs.hashtable.PyObjectHashTable.get_item()

File pandas/_libs/hashtable_class_helper.pxi:5753, in pandas._libs.hashtable.PyObjectHashTable.get_item()

KeyError: 'RelationshipStatus'

The above exception was the direct cause of the following exception:

KeyError                                  Traceback (most recent call last)
Cell In[2], line 1
----> 1 __output__ = df['RelationshipStatus']
      4 with open("./saved_obj.pkl", "wb") as f:
      5     pickle.dump(__output__, f)

File ~/miniforge3/envs/AnalysisAgent/lib/python3.9/site-packages/pandas/core/frame.py:3807, in DataFrame.__getitem__(self, key)
   3805 if self.columns.nlevels > 1:
   3806     return self._getitem_multilevel(key)
-> 3807 indexer = self.columns.get_loc(key)
   3808 if is_integer(indexer):
   3809     indexer = [indexer]

File ~/miniforge3/envs/AnalysisAgent/lib/python3.9/site-packages/pandas/core/indexes/base.py:3804, in Index.get_loc(self, key, method, tolerance)
   3802     return self._engine.get_loc(casted_key)
   3803 except KeyError as err:
-> 3804     raise KeyError(key) from err
   3805 except TypeError:
   3806     # If we have a listlike key, _check_indexing_error will raise
   3807     #  InvalidIndexError. Otherwise we fall through and re-raise
   3808     #  the TypeError.
   3809     self._check_indexing_error(key)

KeyError: 'RelationshipStatus'
"""

REFLECTION = """The error is a KeyError: 'RelationshipStatus'. This error occurred because the code is trying to print the 'RelationshipStatus' column of the dataframe df, but there is no 'RelationshipStatus' column in the dataframe. The dataframe schema provided shows that the dataframe has the following columns: "WorkerID", "Rel1", "Rel2", "Rel3", "Sure1", "Sure2", "Relationship", "ReportedCycleLength", "DateTesting", "StartDateofLastPeriod", "StartDateofPeriodBeforeLast". The 'RelationshipStatus' column is not present in the dataframe."""
THOUGHT = """The best way to fix it is to replace 'RelationshipStatus' with a column that actually exists in the dataframe which should be 'Relationship'."""
RESULT = """```python
print(df['Relationship'])
```"""

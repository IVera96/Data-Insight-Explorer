import pandas as pd

def create_statistics(dataframe: pd.DataFrame) -> dict:
    """
    Create and return a dictionary containing various statistics.
    
    Returns:
        dict: A dictionary with keys 'total_users', 'active_users', and 'inactive_users'.
    """
    df=dataframe.copy()
    info_df = df.describe()

    return info_df.to_dict()
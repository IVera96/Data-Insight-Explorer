import pandas as pd
def clean_dataframe(df: pd.DataFrame) -> pd.DataFrame:
    """
    Cleans the input DataFrame 

    Parameters:
    df (pd.DataFrame): The DataFrame to be cleaned.

    Returns:
    pd.DataFrame: The cleaned DataFrame.
    """
 
    
    df_cleaned = df.drop_duplicates()

    
    df_cleaned.columns = df_cleaned.columns.str.replace(r'[^a-zA-Z0-9_]', '', regex=True)


    for col in df_cleaned.columns:
        if df_cleaned[col].dtype == 'object':
            # Strip whitespace from string columns
            df_cleaned[col] = df_cleaned[col].str.strip()
            df_cleaned[col] = df_cleaned[col].str.lower()
        elif df_cleaned[col].dtype == 'int64' or df_cleaned[col].dtype == 'float64':
            # Convert numeric columns to appropriate types
            df_cleaned[col] = pd.to_numeric(df_cleaned[col], errors='coerce')
        else:
            # For other types, we can just ensure they are not null
            df_cleaned[col] = df_cleaned[col].fillna(method='ffill').fillna(method='bfill')
    
    
    for col in df_cleaned.select_dtypes(include=['float64', 'int64']).columns:
        median_value = df_cleaned[col].median()
        df_cleaned[col] = df_cleaned[col].fillna(median_value)
    # For categorical columns, fill NaN with the mode of the column
    for col in df_cleaned.select_dtypes(include=['object']).columns:
        mode_value = df_cleaned[col].mode()[0] if not df_cleaned[col].mode().empty else df_cleaned[col].iloc[0]
        df_cleaned[col] = df_cleaned[col].fillna(mode_value)
    
    
    df_cleaned = df_cleaned.dropna()

    
    df_cleaned = df_cleaned.reset_index(drop=True)


    return df_cleaned
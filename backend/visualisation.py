import matplotlib.pyplot as plt
import seaborn as sns
from io import BytesIO
import base64

def create_visualisation(df):
    """
    Create visualizations for the given DataFrame.
    
    Args:
        df (pd.DataFrame): The DataFrame to visualize.
    
    Returns:
        dict: A dictionary containing visualizations.
    """

    visualizations = {}

    numeric_cols = df.select_dtypes(include=['number']).columns
    if numeric_cols.empty:
        return {"message": "No numeric columns to visualize."}
    
    for col in numeric_cols:
        plt.figure(figsize=(5, 3))
        sns.histplot(df[col], kde=True)
        plt.title(f'Histogram of {col}')
        plt.xlabel(col)
        plt.ylabel('Frequency')

        # Save the plot to a BytesIO object and encode it to base64
        buf = BytesIO()
        plt.savefig(buf, format='png')
        buf.seek(0)
        image_base64 = base64.b64encode(buf.read()).decode('utf-8')
        visualizations[col] = f"data:image/png;base64,{image_base64}"
        plt.close()
    # if no numeric columns are found, return a message
    if not visualizations:
        return {"message": "No visualizations created."}
    
    return visualizations
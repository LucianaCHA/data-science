def read_csv_to_dataframe(file_path):
    import pandas as pd
    
    try:
        # Read the CSV file into a DataFrame
        df = pd.read_csv(file_path)
        return df
    except Exception as e:
        print(f"An error occurred while reading the CSV file: {e}")
        return None
    
    
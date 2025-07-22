import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from app.utils import postgres_utils


def plot_boxplot_with_outliers(table, column, step=10, show_outlier_count=True):
    """
    Plots a boxplot of the specified column from a SQL table with IQR-based outlier bounds.

    Parameters:
    - table (str): Name of the table.
    - column (str): Column to analyze.
    - step (int): Step size for x-axis ticks.
    - show_outlier_count (bool): Whether to print number of outliers.
    """
    # Fetch column data from the database
    query = f'SELECT "{column}" FROM "{table}";'
    df = postgres_utils.run_query(query)

    # Use the actual column name from the DataFrame
    actual_col = df.columns[0]

    # Compute IQR and bounds
    Q1 = df[actual_col].quantile(0.25)
    Q3 = df[actual_col].quantile(0.75)
    IQR = Q3 - Q1
    lower_bound = Q1 - 1.5 * IQR
    upper_bound = Q3 + 1.5 * IQR

    # Identify outliers
    outliers = df[(df[actual_col] < lower_bound) | (df[actual_col] > upper_bound)]

    if show_outlier_count:
        print(f"Number of outliers in '{column}': {len(outliers)}")

    # Plot boxplot
    plt.figure(figsize=(10, 2))
    sns.boxplot(x=df[actual_col])
    plt.title(f"Boxplot of {column}")
    max_val = df[actual_col].max()
    plt.xticks(np.arange(0, int(max_val) + step, step))
    plt.tight_layout()
    plt.show()

    return outliers, lower_bound, upper_bound
    # """
    # Plots a boxplot of the specified column with IQR-based outlier bounds.

    # Parameters:
    # - df (pd.DataFrame): DataFrame containing the data.
    # - column (str): Column to analyze.
    # - step (int): Step size for x-axis ticks.
    # - show_outlier_count (bool): Whether to print number of outliers.
    # """
    # Q1 = df[column].quantile(0.25)
    # Q3 = df[column].quantile(0.75)
    # IQR = Q3 - Q1
    # lower_bound = Q1 - 1.5 * IQR
    # upper_bound = Q3 + 1.5 * IQR

    # outliers = df[(df[column] < lower_bound) | (df[column] > upper_bound)]

    # if show_outlier_count:
    #     print(f"Number of outliers in '{column}': {len(outliers)}")

    # # Plot
    # plt.figure(figsize=(10, 2))
    # sns.boxplot(x=df[column])
    # plt.title(f"Boxplot of {column}")
    # # plt.axvline(lower_bound, color="red", linestyle="--", label="Lower bound")
    # # plt.axvline(upper_bound, color="red", linestyle="--", label="Upper bound")
    # plt.xticks(np.arange(0, int(df[column].max()) + step, step))
    # # plt.legend()
    # plt.tight_layout()
    # plt.show()

    # return outliers, lower_bound, upper_bound

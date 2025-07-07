import pandas as pd
import utils.notebook_utils as notebook_utils


def sum_non_null(df: pd.DataFrame, column: str) -> float:
    return df[column].sum(skipna=True)


def sum_zero_or_negative(df: pd.DataFrame, column: str) -> float:
    return (df[column] <= 0).sum()


def get_dataframe_info(df: pd.DataFrame) -> None:
    notebook_utils.print_colored("DataFrame Info:", "blue")
    df.info()
    

def is_outlier(df: pd.DataFrame, column: str, limit: int = 1.5) -> pd.Series:
    lower_bound, upper_bound = get_iqr_bounds(df, column, limit=limit)
    return (df[column] < lower_bound) | (df[column] > upper_bound)


def get_iqr_bounds(
        df: pd.DataFrame, column: str, limit: int) -> tuple[float, float]:
    q1 = df[column].quantile(0.25)
    q3 = df[column].quantile(0.75)
    iqr = q3 - q1
    lower_bound = q1 - limit * iqr
    upper_bound = q3 + limit * iqr
    return lower_bound, upper_bound

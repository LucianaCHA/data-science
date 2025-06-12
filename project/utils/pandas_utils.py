import pandas as pd
import utils.notebook_utils as notebook_utils


def sum_non_null(df: pd.DataFrame, column: str) -> float:
    return df[column].sum(skipna=True)


def sum_zero_or_negative(df: pd.DataFrame, column: str) -> float:
    return (df[column] <= 0).sum()


def get_dataframe_info(df: pd.DataFrame) -> None:
    notebook_utils.print_colored('DataFrame Info:', 'blue')
    df.info()
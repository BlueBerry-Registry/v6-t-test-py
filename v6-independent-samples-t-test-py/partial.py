import pandas as pd
import pandas.api.types as ptypes
from typing import Any

from vantage6.algorithm.tools.util import info, error
from vantage6.algorithm.tools.decorators import data


@data(1)
def partial(df: pd.DataFrame, column_name: str) -> dict:
    """
    Compute the mean and the sample variance of a column for a single data station to
    share with the aggregator part of the algorithm

    Parameters
    ----------
    df : pd.DataFrame
        The data for the data station
    column_name : str
        The column to compute the mean and sample variance for. The column must be
        numeric.

    Returns
    -------
    dict
        The mean, the number of observations and the sample variance for the data
        station.
    """

    if not ptypes.is_numeric_dtype(df[column_name]):
        error("Column must be numeric.")

    ### Compute mean ----
    info("Computing mean")
    # Sum of the values
    col_sum = df[column_name].sum()
    # Count of observations
    count = len(df)
    # Mean
    avg = col_sum / count

    ### Compute sample variance (S) ----
    info("Computing sample variance")
    # Sum of Squared Deviations (SSD)
    ssd = ((df[column_name].astype(float) - avg) ** 2).sum()
    # Sample variance
    S = ssd / (count - 1)

    # Return results to the vantage6 server.
    return {"avg": float(avg), "count": float(count), "S": float(S)}

import pandas as pd
import pandas.api.types as ptypes

from vantage6.algorithm.tools.util import info, error, get_env_var
from vantage6.algorithm.tools.decorators import data
from vantage6.algorithm.tools.exceptions import InputError
from .globals import T_TEST_MINIMUM_NUMBER_OF_RECORDS


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

    info("Checking number of records in the DataFrame.")
    MINIMUM_NUMBER_OF_RECORDS = get_env_var(
        "T_TEST_MINIMUM_NUMBER_OF_RECORDS",
        T_TEST_MINIMUM_NUMBER_OF_RECORDS,
        as_type="int",
    )
    if len(df) <= MINIMUM_NUMBER_OF_RECORDS:
        raise InputError(
            "Number of records in 'df' must be greater than "
            f"{MINIMUM_NUMBER_OF_RECORDS}."
        )

    if not ptypes.is_numeric_dtype(df[column_name]):
        error("Column must be numeric.")

    ### Compute mean ----
    info("Computing mean")
    # Sum of the values
    column_sum = df[column_name].sum()
    # Count of observations
    count = len(df)
    # Mean
    average = column_sum / count

    ### Compute sample variance (S) ----
    info("Computing sample variance")
    # Sum of Squared Deviations (SSD)
    ssd = ((df[column_name].astype(float) - average) ** 2).sum()
    # Sample variance
    variance = ssd / (count - 1)

    # Return results to the vantage6 server.
    return {
        "average": float(average),
        "count": float(count),
        "variance": float(variance),
    }

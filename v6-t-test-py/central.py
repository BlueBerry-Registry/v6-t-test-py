import numpy as np
from scipy.stats import t

from vantage6.algorithm.tools.util import info
from vantage6.algorithm.tools.decorators import algorithm_client
from vantage6.algorithm.client import AlgorithmClient
from vantage6.algorithm.tools.exceptions import UserInputError


@algorithm_client
def central(
    client: AlgorithmClient,
    organizations_to_include: list[int],
    columns: list[str] | None = None,
) -> dict:
    """
    Send task to each node participating in the task to compute a local mean and sample
    variance, aggregate them to compute the t value for the independent sample t-test,
    and return the result.

    Parameters
    ----------
    client : AlgorithmClient
        The client object used to communicate with the server.
    organizations_to_include : list[int]
        The organizations to include in the task. These must be exactly 2.
    columns : list[str] | None
        The columns to compute the t test for. The columns must be
        numeric. If not provided, all numeric columns are included.
    """

    # Check that the number of organization included is exactly 2
    if len(organizations_to_include) != 2:
        raise UserInputError("Exactly 2 organizations should be provided")

    # Define input parameters for a subtask
    info("Defining input parameters")
    input_ = {
        "method": "partial",
        "kwargs": {
            "columns": columns,
        },
    }

    # create a subtask for all organizations in the collaboration.
    info("Creating subtask for all organizations in the collaboration")
    task = client.task.create(
        input_=input_,
        organizations=organizations_to_include,
        name="Subtask mean and sample variance",
        description="Compute mean and sample variance per data station.",
    )

    # wait for node to return results of the subtask.
    info("Waiting for results")
    results = client.wait_for_results(task_id=task.get("id"))
    info("Results obtained!")

    # Aggregate results to compute t value for the independent-samples t test
    t_test_results = {}
    for cols in zip(*[result.items() for result in results]):
        col = cols[0][0]
        col_result = [col_value[1] for col_value in cols]
        # Compute pooled variance
        Sp = (
            (col_result[0]["count"] - 1) * col_result[0]["variance"]
            + (col_result[1]["count"] - 1) * col_result[1]["variance"]
        ) / (col_result[0]["count"] + col_result[1]["count"] - 2)
        # t score
        t_score = (col_result[0]["average"] - col_result[1]["average"]) / (
            ((Sp / col_result[0]["count"]) + (Sp / col_result[1]["count"])) ** 0.5
        )
        # Degrees of freedom (DOF)
        dof = (col_result[0]["count"] + col_result[1]["count"]) - 2
        # p-value
        p_value = float(2 * (1 - t.cdf(np.abs(t_score), dof)))

        t_test_results[col] = {
            "t_score": t_score,
            "p_value": p_value,
        }

    # return the final results of the algorithm
    return t_test_results

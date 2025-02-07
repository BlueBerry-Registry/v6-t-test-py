from typing import Any

from vantage6.algorithm.tools.util import info
from vantage6.algorithm.tools.decorators import algorithm_client
from vantage6.algorithm.client import AlgorithmClient


@algorithm_client
def central(
    client: AlgorithmClient, column_name: str, organizations_to_include: list[int]
) -> Any:
    """
    Send task to each node participating in the task to compute a local mean and sample
    variance, aggregate them to compute the t value for the independent sample t-test,
    and return the result.

    Parameters
    ----------
    client : AlgorithmClient
        The client object used to communicate with the server.
    column_name : str
        The column to compute the mean and sample variance for. The column must be
        numeric.
    organizations_to_include : list[int]
        The organizations to include in the task.
    """

    # Define input parameters for a subtask
    info("Defining input parameters")
    input_ = {
        "method": "partial",
        "kwargs": {
            "column_name": column_name,
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
    # Compute pooled variance
    Sp = (
        (results[0]["count"] - 1) * results[0]["S"]
        + (results[1]["count"] - 1) * results[1]["S"]
    ) / (results[0]["count"] + results[1]["count"] - 2)

    # t value
    t = (results[0]["avg"] - results[1]["avg"]) / (
        ((Sp / results[0]["count"]) + (Sp / results[1]["count"])) ** 0.5
    )

    # return the final results of the algorithm
    return {"t": t}

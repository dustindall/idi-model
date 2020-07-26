from typing import Tuple

import pandas as pd
from dask import compute
from dask.delayed import delayed

from footings import define_parameter, use, build_model

from ..policy_models.dlr_deterministic import (
    dlr_deterministic_model,
    param_valuation_dt,
    param_assumption_set,
)
from ..functions.shared import dispatch_model_per_record

__all__ = ["check_extract", "create_output", "run_policy_model_per_record"]

#########################################################################################
# arguments
#########################################################################################

# valuation_dt and assumption_set are imported from policy_models

param_extract = define_parameter(
    name="extract",
    description="The disabled life extract to use. See idi_model/schema/disabled_life_schema.yaml for specification.",
    dtype=pd.DataFrame,
)

param_policy_model = define_parameter(
    name="policy_model",
    description="""The policy model to deploy. Options are :

        * `determinstic`
        * `stochastic`
    """,
    dtype=str,
    allowed=["deterministic", "stochastic"],
)

#########################################################################################
# functions
#########################################################################################


def check_extract(
    extract: pd.DataFrame,  # , valuation_dt: pd.Timestamp, schema: pd.DataFrame
):
    """Check extract against required schema.
    
    Parameters
    ----------
    extract : pd.DataFrame
        The extract to check.
    valuation_dt : pd.Timestamp
        The valuation date to be modeled.
    schema : 
        The required schema.
    
    Returns
    -------
    pd.DataFrame
        The extract.
    """
    return extract


def run_policy_model_per_record(
    extract: pd.DataFrame,
    valuation_dt: pd.Timestamp,
    assumption_set: str,
    policy_model: str,
) -> list:
    """Run each policy in extract through specified policy model.

    Parameters
    ----------
    extract : pd.DataFrame
        The extract to run.
    valuation_dt : pd.Timestamp
        The valuation date to be modeled.
    assumption_set : str
        The assumptions set to model.
    net_benefit_method : str
        The net benefit method to use.
    policy_model : callable
        The policy model to run for each policy in extract.

    Raises
    ------
    NotImplementedError
        When specifying policy_model = stochastic

    Returns
    -------
    list
        A list of all policies that have been ran through the policy model.
    """
    if policy_model == "deterministic":
        return dispatch_model_per_record(
            policy_model=dlr_deterministic_model,
            record_keys=["POLICY_ID", "CLAIM_ID"],
            extract=extract,
            valuation_dt=valuation_dt,
            assumption_set=assumption_set,
        )
    elif policy_model == "stochastic":
        raise NotImplementedError("Stochastic capabilities not implemented yet.")


def create_output(results: list) -> Tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    """
    Creates model output.

    Returns
    -------
    Tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]
        A tuple with three DataFrames : 
        
        * `[0]` = Time 0 reserve values
        * `[1]` = Projected reserve values
        * `[2]` = Any errors produced
    """
    successes = results[0]
    errors = results[1]
    time_0 = pd.concat([success.head(1) for success in successes]).reset_index(drop=True)
    projected = pd.concat(successes)
    time_0_cols = [
        "MODEL_VERSION",
        "LAST_COMMIT",
        "RUN_DATE_TIME",
        "POLICY_ID",
        "DLR",
    ]
    return time_0[time_0_cols], projected, errors


#########################################################################################
# steps
#########################################################################################

steps = [
    {
        "name": "check-extract",
        "function": check_extract,
        "args": {
            "extract": param_extract,
            # "valuation_dt": param_valuation_dt,
            # "schema": "123",
        },
    },
    {
        "name": "run-policy-model-per-record",
        "function": run_policy_model_per_record,
        "args": {
            "extract": use("check-extract"),
            "valuation_dt": param_valuation_dt,
            "assumption_set": param_assumption_set,
            "policy_model": param_policy_model,
        },
    },
    {
        "name": "create-output",
        "function": create_output,
        "args": {"results": use("run-policy-model-per-record")},
    },
]

#########################################################################################
# models
#########################################################################################

DESCRIPTION = """A population model to calculate disabled life reserves (DLRs) using the 2013 individual
disability insurance (IDI) valuation standard.

The model is configured to use different assumptions sets - stat, gaap, or best-estimate.

The key assumption underlying the model is -

* `Termination Rates` - the probability of an individual going off claim.

"""
disabled_lives_model = build_model(
    name="DisabledLivesModel", description=DESCRIPTION, steps=steps
)

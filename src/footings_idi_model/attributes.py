import pandas as pd
from footings import def_parameter, def_meta, def_sensitivity

from .__init__ import __version__ as MOD_VERSION
from .__init__ import __git_revision__ as GIT_REVISION

param_n_simulations = def_parameter(
    description="The number of simulations to run.", default=1000, dtype=int,
)

param_seed = def_parameter(
    description="The seed passed to numpy.random.seed.", default=42, dtype=int,
)

param_valuation_dt = def_parameter(
    description="The valuation date which reserves are based.", dtype=pd.Timestamp,
)

param_assumption_set = def_parameter(
    description="""The assumption set to use for running the model. Options are :

        * `stat`
        * `gaap`
        * `best-estimate`
    """,
    dtype=str,
    allowed=["stat", "gaap", "best-estimate"],
)

param_disabled_extract = def_parameter(
    description="The disabled life extract to use. See idi_model/schema/disabled_life_schema.yaml for specification.",
    dtype=pd.DataFrame,
)

param_active_base_extract = def_parameter(
    description="""The active life base extract to use. See idi_model/schema/extract-active-lives-base.yaml
    for specification.""",
    dtype=pd.DataFrame,
)

param_active_rider_extract = def_parameter(
    description="""The active life rider extract to use. See idi_model/schema/extract-active-lives-riders.yaml
    for specification.""",
    dtype=pd.DataFrame,
)

param_model_type = def_parameter(
    description="""The policy model to deploy. Options are :

        * `determinstic`
        * `stochastic`
    """,
    dtype=str,
    allowed=["deterministic", "stochastic"],
)

param_net_benefit_method = def_parameter(
    description="""The net benefit method. Options are :

        * `NLP` = Net level premium
        * `PT1` = 1 year preliminary term
        * `PT2` = 2 year preliminary term
    """,
    dtype=str,
    allowed=["NLP", "PT1", "PT2"],
)

param_withdraw_table = def_parameter(
    dtype=str,
    description="Table name for withdraw rates.",
    allowed=["01CSO", "17CSO", "58CSO", "80CSO"],
)

param_volume_tbl = def_parameter(
    dtype=pd.DataFrame,
    description="The volume table to use with refence to the distribution of policies by attributes.",
)

param_as_of_dt = def_parameter(
    dtype=pd.Timestamp, description="The as of date which birth date will be based.",
)

meta_model_version = def_meta(
    meta=MOD_VERSION, dtype=str, description="The model version generated by versioneer."
)

meta_last_commit = def_meta(
    meta=GIT_REVISION, dtype=str, description="The last git commit."
)

meta_run_date_time = def_meta(
    meta=pd.to_datetime("now"), dtype=pd.Timestamp, description="The run date and time."
)

modifier_ctr = def_sensitivity(default=1.0, dtype=float, description="Modifier for CTR.")

modifier_interest = def_sensitivity(
    default=1.0, dtype=float, description="Interest rate modifier."
)

modifier_incidence = def_sensitivity(
    default=1.0, description="The incidence rate modifier."
)

modifier_withdraw = def_sensitivity(default=1.0, description="The withdraw rate modifier")

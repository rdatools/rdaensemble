"""
UTILTIES
"""


import os, pwd, datetime
from typing import Any, Dict

from rdabase import cycle, plan_type


def ensemble_metadata(
    *,
    xx: str,
    ndistricts: int,
    size: int,
    technique: str,
) -> Dict[str, Any]:
    """Create the metadata for an ensemble."""

    ensemble: Dict[str, Any] = dict()

    ensemble["username"] = pwd.getpwuid(os.getuid()).pw_name

    timestamp = datetime.datetime.now()
    ensemble["date_created"] = timestamp.strftime("%x")
    ensemble["time_created"] = timestamp.strftime("%X")

    ensemble["repository"] = "rdatools/rdaensemble"

    ensemble["state"] = xx
    ensemble["cycle"] = cycle
    ensemble["plan_type"] = plan_type
    ensemble["units"] = "VTD"
    ensemble["ndistricts"] = ndistricts

    ensemble["technique"] = technique
    ensemble["size"] = size

    return ensemble


### END ###

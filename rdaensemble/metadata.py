"""
UTILTIES
"""


import os, pwd, datetime
from typing import Any, Dict

from rdabase import cycle, plan_type


def shared_metadata(
    *,
    xx: str,
) -> Dict[str, Any]:
    """Create the metadata for an ensemble."""

    shared: Dict[str, Any] = dict()

    shared["username"] = pwd.getpwuid(os.getuid()).pw_name

    timestamp = datetime.datetime.now()
    shared["date_created"] = timestamp.strftime("%x")
    shared["time_created"] = timestamp.strftime("%X")

    shared["repository"] = "rdatools/rdaensemble"

    shared["state"] = xx
    shared["cycle"] = cycle
    shared["plan_type"] = plan_type
    shared["units"] = "VTD"

    return shared


def ensemble_metadata(
    *,
    xx: str,
    ndistricts: int,
    size: int,
    method: str,
) -> Dict[str, Any]:
    """Create the metadata for an ensemble."""

    ensemble: Dict[str, Any] = shared_metadata(xx=xx)

    ensemble["ndistricts"] = ndistricts
    ensemble["method"] = method
    ensemble["size"] = size

    return ensemble


### END ###

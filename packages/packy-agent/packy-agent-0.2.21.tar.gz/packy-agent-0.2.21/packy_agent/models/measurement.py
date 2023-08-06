from datetime import datetime

from schematics import types

from packy_agent.utils.schematics import CustomModel


class BaseMeasurement(CustomModel):
    dt = types.DateTimeType(default=datetime.utcnow)


class HTTPModuleMeasurement(BaseMeasurement):
    ts = types.IntType(required=True)
    target = types.StringType(required=True)

    is_success = types.BooleanType(default=True)
    http_status_code = types.IntType()

    namelookup_ms = types.FloatType()
    total_ms = types.FloatType()

    certificate_expiration_dt = types.DateTimeType()

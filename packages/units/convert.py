DOC = """Quantities converted between units: length, mass, temperature and time.

Lengths m, km, cm, mm, mi, yd, ft, in; masses kg, g, mg, t, lb, oz; temperatures C, F, K; times s, min, h, day, week."""
CONFIG = {}

_SCALES = {
    "length": {"m": 1.0, "km": 1000.0, "cm": 0.01, "mm": 0.001, "mi": 1609.344, "yd": 0.9144, "ft": 0.3048,
               "in": 0.0254},
    "mass": {"kg": 1.0, "g": 0.001, "mg": 1e-6, "t": 1000.0, "lb": 0.45359237, "oz": 0.028349523125},
    "time": {"s": 1.0, "min": 60.0, "h": 3600.0, "day": 86400.0, "week": 604800.0},
}


def _kelvin(value, unit):
    return {"K": value, "C": value + 273.15, "F": (value - 32.0) * 5.0 / 9.0 + 273.15}[unit]


def convert_units(value, from_unit, to_unit):
    """value in from_unit, as to_unit: 12 "ft" "m" is 3.6576."""
    value = float(value)
    if from_unit in ("C", "F", "K") and to_unit in ("C", "F", "K"):
        k = _kelvin(value, from_unit)
        return {"K": k, "C": k - 273.15, "F": (k - 273.15) * 9.0 / 5.0 + 32.0}[to_unit]
    for scale in _SCALES.values():
        if from_unit in scale and to_unit in scale:
            return value * scale[from_unit] / scale[to_unit]
    raise ValueError("%s and %s are not units of one kind: lengths %s; masses %s; times %s; temperatures C F K" % (
        from_unit, to_unit, " ".join(_SCALES["length"]), " ".join(_SCALES["mass"]), " ".join(_SCALES["time"])))

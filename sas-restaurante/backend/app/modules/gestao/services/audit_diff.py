def build_diff(before: dict | None, after: dict | None):
    if not before or not after:
        return None

    diff = {}

    for key in after.keys():
        if key not in before:
            diff[key] = {"before": None, "after": after[key]}
        elif before[key] != after[key]:
            diff[key] = {
                "before": before[key],
                "after": after[key]
            }

    return diff or None

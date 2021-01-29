import json


def triggered_by_id(triggered, id, pattern_matching=False, type_key="type"):
    for elem in triggered:
        trigger_id, _ = elem["prop_id"].split(".")
        if trigger_id and pattern_matching:
            try:
                trigger_id = json.loads(trigger_id)[type_key]
            except json.JSONDecodeError:
                pass
        if trigger_id == id:
            return True
    return False


def get_trigger_id(triggered, key="type"):
    trigger_id = triggered[0]["prop_id"].split(".")[0]
    if trigger_id:
        if trigger_id.startswith("{") and trigger_id.endswith("}"):
            try:
                return json.loads(trigger_id)[key]
            except json.JSONDecodeError:
                pass
    return trigger_id


def get_trigger_index(triggered, key="index"):
    trigger_id = triggered[0]["prop_id"].split(".")[0]
    if trigger_id:
        return json.loads(trigger_id)[key]
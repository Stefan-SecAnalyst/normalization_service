
def normalize_record(record, rules):
    normalized = {}
    # Optionally define a field mapping to handle source name differences
    field_map = {
        "timestamp": ["timestamp"],
        "system": ["system", "system_name"],
        "level": ["level"],
        "code": ["code", "error_code"],
        "message": ["message", "msg"]
    }

    for out_field, rule in rules.items():
        print(f"Normalizing output field: {out_field} using rule: {rule}")
        # Try each possible input field for this output field
        input_value = None
        for possible_key in field_map.get(out_field, [out_field]):
            if possible_key in record:
                input_value = record[possible_key]
                break

        normalized_value = input_value  # default

        if input_value is not None:
            if rule.get("type") == "datetime":
                normalized_value = datetime_normalizer(input_value, rule)
            elif rule.get("transform") == "upper":
                normalized_value = uppercase_normalizer(input_value)
            elif rule.get("transform") == "lower":
                normalized_value = lowercase_normalizer(input_value)
            elif rule.get("type") == "integer":
                normalized_value = code_normalizer(input_value, rule)
            elif out_field == "message" and "mask_keywords" in rule:
                normalized_value = message_normalizer(rule, input_value)

            # Enforce allowed values if defined
            allowed = rule.get("allowed_values")
            if allowed and normalized_value not in allowed:
                normalized_value = None

        normalized[out_field] = normalized_value
        print("Normalized record:", normalized)
    return normalized


#DateTime normalization function
def datetime_normalizer(value, rule):
    # Implement datetime normalization logic here
    
    from datetime import datetime
    input_fmt = rule.get("input_format")
    output_fmt = rule.get("output_format", input_fmt)
    
    try:
        dt = datetime.strptime(value, input_fmt)
        normalized_value = dt.strftime(output_fmt)
    except Exception:
        normalized_value = value

    return normalized_value


def uppercase_normalizer(value):
    try:
        value = value.upper()
        return value
    except Exception:
        value = None
    return value

def lowercase_normalizer(value):
    value = value.lower()
    return value


def code_normalizer(value, rule):
    try:
        normalized_value = int(value)
    except Exception:
        normalized_value = None

    minv = rule.get("min_value")
    maxv = rule.get("max_value")

    if minv is not None and normalized_value is not None and normalized_value < minv:
        normalized_value = None
    if maxv is not None and normalized_value is not None and normalized_value > maxv:
        normalized_value = None

    
    return normalized_value


def message_normalizer(rule, value):
    masked_value = value
    for keyword in rule["mask_keywords"]:
        if keyword.lower() in str(value).lower():
            masked_value = "[MASKED]"
    return masked_value
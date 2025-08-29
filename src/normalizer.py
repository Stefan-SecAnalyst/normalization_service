
def normalizer (record, rules):
    normalized = {}  # Start an empty dict for output
    for field, value in record.items():
        if field in rules:
            rule = rules[field]
    
            if rule.get("type") == "datetime":
                normalized = datetime_normalizer(value, rule)


            elif rule.get("transform") == "uppercase":
                normalized_value = uppercase_normalizer(value)

            elif rule.get("transfrom") == "lowercase":
                normalized_value = lowercase_normalizer(value)

            else:
                normalized[field] = value
        #Enforce Allowed Values
        allowed = rule.get("allowed_values")

        if allowed and normalized[field] not in allowed:
            normalized[field] = None

        if rule.get("type") == "integer":
            code_normalizer(value, rule)

        if field = "message" and "mask_keywords" in rule:

            normalized_value = value
            normalized[field] = normalized_value
        else:
            normalized[field] = value
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
        value = int(value)
    except Exception:
        value = None

    minv = rule.get("min_value")
    maxv = rule.get("max_value")

    if minv is not None and normalized_value is not None and normalized_value < minv:
        normalized_value = None
    if maxv is not None and normalized_value is not None and normalized_value > maxv:
        normalized_value = None

    
    return value


def message_normalizer(rule, value):
    masked_value = value
    for keyword in rule["mask_keywords"]:
        if keyword.lower() in str(value).lower():
            masked_value = "[MASKED]"
    return masked_value
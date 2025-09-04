
def normalize_record (record, rules):
    normalized = {}  # Start an empty dict for output

    for field, value in record.items():
        if field in rules:
            rule = rules[field]
    
            if rule.get("type") == "datetime":
                normalized_value = datetime_normalizer(value, rule)


            elif rule.get("transform") == "uppercase":
                normalized_value = uppercase_normalizer(value)

            elif rule.get("transform") == "lowercase":
                normalized_value = lowercase_normalizer(value)

            elif rule.get("type") == "integer":
                normalized_value = code_normalizer(value, rule)

            elif field == "message" and "mask_keywords" in rule:
                normalized_value = message_normalizer(rule, value)

            else:
                normalized_value = value
        #Enforce Allowed Values
        allowed = rule.get("allowed_values")

        if allowed and normalized_value not in allowed:
            normalized_value = None


        normalized[field] = normalized_value
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
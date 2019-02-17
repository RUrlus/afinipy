def concat_imports(values, sep='.'):
    if isinstance(values, str):
        return values

    values = list(values)
    if len(values) >= 1:
        store = []
        for v in values:
            if isinstance(v, (list, tuple)):
                store.extend(v)
            else:
                store.append(v)
        imports = sep.join(store)
        if imports[0] == '.':
            return imports[1:]
        else:
            return imports
    else:
        return ''


def notin(validate, baseline):
    """Determine wich elements are not present in the baseline
    but are present in the `validate set`

    Parameters
    ----------
    validate : set, or list-like
        The set from which we want to find the elements
    baseline : set, or list-like
        The set that serves as a baseline set

    Returns
    -------
    set
        Set containing the element not in baseline
    """
    return set(validate) - set(baseline)


def ordered_notin(validate, baseline):
    """Determine wich elements are not present in the baseline
    but are present in the `validate set`

    Parameters
    ----------
    validate : list
        The list from which we want to find the elements
    baseline : list
        The list that serves as a baseline set

    Returns
    -------
    set
        Set containing the element not in baseline
    """
    return [v for v in validate if v not in baseline]

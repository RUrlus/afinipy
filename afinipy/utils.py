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


def concat_strings(values, sep='.'):
    """Combine list of string into string

    Parameters
    ----------
    values : list
        The list with which to combine
    sep : str
        The seperator between the parents

    Returns
    -------
    str
        String containing all the parents
    """
    return sep.join(values)

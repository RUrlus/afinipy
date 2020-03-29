"""Utility functions for afinipy."""


def concat_imports(values, sep='.'):
    """Combine import statements.

    Parameters
    ----------
    values : list-like
        The values to be concatenated
    sep : string
        The value between the statements

    Returns
    -------
    str
        The concatenated string

    """
    if len(values) >= 1:
        store = []
        for v in values:
            if isinstance(v, (list, tuple)):
                store.extend(v)
            else:
                store.append(v)
        return sep.join(store)
    else:
        return ''


def notin(validate, baseline):
    """Determine elements not in validate.

    Parameters
    ----------
    validate : set, or list-like
        The set from which we want to find the elements
    baseline : set, or list-like
        The set that serves as a baseline set

    Returns
    -------
    set
        List containing the elements not in baseline

    """
    return set(validate) - set(baseline)


def ordered_notin(validate, baseline):
    """Determine elements not in validate.

    Parameters
    ----------
    validate : list
        The list from which we want to find the elements
    baseline : list
        The list that serves as a baseline set

    Returns
    -------
    list
        List containing the elements not in baseline

    """
    return [v for v in validate if v not in baseline]

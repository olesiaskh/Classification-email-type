def orgtype(data):
    """Define sets of organization types.

    Parameters
    ----------
    data: dataframe
        Dataframe that includes 'label' and 'org' columns.

    Returns
    -------
    org_update: set
        The organizations the belong to set 'update'.
    org_personal: set
        The organizations the belong to set 'personal'.
    org_promo: set
        The organizations the belong to set 'promotions'.
    org_prof: set
        The organizations the belong to set 'professional'.
    org_com: set
        The organizations the belong to set 'commercial'.
    org_travel: set
        The organizations the belong to set 'travel'.
    org_spam: set
        The organizations the belong to set 'spam'.
    org_social: set
        The organizations the belong to set 'social'.

    Notes
    -------
    The type is based on target value that appears with a specific organization.
    If an organization is associated with multiple target values, the organization is
    assigned to the type that is least common in the dataset overall
    (neither 'update', nor 'personal').
    """
    label_sets = [set(data[data["label"] == i]["org"].unique()) for i in range(8)]

    org_update = label_sets[0] - set.union(*label_sets[2:])
    org_personal = label_sets[1] - set.union(label_sets[0], *label_sets[2:])
    org_promo = label_sets[2] - label_sets[4]
    org_prof = label_sets[3]
    org_com = label_sets[4]
    org_travel = label_sets[5] - label_sets[3]
    org_spam = label_sets[6] - label_sets[4]
    org_social = label_sets[7]

    return (
        org_update,
        org_personal,
        org_promo,
        org_prof,
        org_com,
        org_travel,
        org_spam,
        org_social,
    )


def org_encode(
    data,
    org_update,
    org_personal,
    org_promo,
    org_prof,
    org_com,
    org_travel,
    org_spam,
    org_social,
):
    """Assign organization type to each email.

    Parameters
    ----------
    data: dataframe
        Dataframe that includes 'org' column.
    org_update: set
        The organizations the belong to set 'update'.
    org_personal: set
        The organizations the belong to set 'personal'.
    org_promo: set
        The organizations the belong to set 'promotions'.
    org_prof: set
        The organizations the belong to set 'professional'.
    org_com: set
        The organizations the belong to set 'commercial'.
    org_travel: set
        The organizations the belong to set 'travel'.
    org_spam: set
        The organizations the belong to set 'spam'.
    org_social: set
        The organizations the belong to set 'social'.

    Returns
    -------
    dataframe
        Dataframe with 8 new columns: 'org_update', 'org_personal',
        'org_promo', 'org_prof', 'org_com', 'org_travel', 'org_spam',
        'org_social' (all boolean).
    """
    for org_type in [
        "org_update",
        "org_personal",
        "org_promo",
        "org_prof",
        "org_com",
        "org_travel",
        "org_spam",
        "org_social",
    ]:
        data[org_type] = data["org"].isin(eval(org_type)).astype(int)

    return data

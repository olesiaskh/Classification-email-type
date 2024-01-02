import pandas as pd


def tld_clean(data):
    """Separate organization and domain if they are still one value in 'tld'.

    Parameters
    ----------
    data: dataframe
        Dataframe that includes 'tld' and 'org' columns.

    Returns
    -------
    dataframe
        Dataframe with cleaned values in 'tld'.

    Notes
    -------
    The function replaces current organization name with name extracted from 'tld'.
    Double domain names (such as 'gov.fr') are kept as one value in 'tld'.
    """
    exceptions = ["org", "co", "gov", "ac", "net"]  # elements of double domain names
    for index, row in data.iterrows():
        element = row["tld"]
        if pd.notna(element):
            splitted = element.split(".")
            if len(splitted) == 2 and splitted[0] not in exceptions:
                data.loc[index, "tld"] = splitted[1]
                data.loc[index, "org"] = splitted[0]

            elif len(splitted) > 2:
                if splitted[-2] not in exceptions:
                    data.loc[index, "tld"] = splitted[-1]
                    data.loc[index, "org"] = ".".join(splitted[:-2])
                else:
                    data.loc[index, "tld"] = splitted[-2]
                    data.loc[index, "org"] = ".".join(splitted[:-3])

        else:
            data.loc[index, "tld"] = None

    return data


def mailtype_clean(data):
    """Fix differences in spelling of the same values.

    Parameters
    ----------
    data: dataframe
        Dataframe that includes the 'mail_type' column with values to fix.

    Returns
    -------
    dataframe
        Dataframe with values in 'mail_type' column lowered and
        stripped of trailing whitespaces.
    """
    data["mail_type"] = data["mail_type"].str.lower().str.strip()

    return data

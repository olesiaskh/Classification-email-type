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
    exceptions = ['org','co','gov','ac','net'] #elements of double domain names
    for index,row in data.iterrows():
        element = row['tld']
        if type(element) != float:
            splitted = element.split(".")
            if len(splitted) == 2:
                if splitted[0] not in exceptions:
                    data.loc[index,'tld'] = splitted[1]
                    data.loc[index,'org']=splitted[0]
      
            elif len(splitted) > 2:
                if splitted[-2] not in exceptions:
                    data.loc[index,'tld'] = splitted[-1]
                    merged_org = '.'.join(splitted[:-2])
                    data.loc[index,'org'] = merged_org
                else:
                     merged_tld = '.'.join(splitted[-2:-1])
                     data.loc[index,'tld'] = merged_tld
                     merged_org = '.'.join(splitted[:-3])
                     data.loc[index,'org'] = merged_org

        else:
            data.loc[index,'tld']=None
           
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
        Dataframe with spelling fixed in 'mail_type' column.
    """
    data['mail_type'] = data['mail_type'].replace(['Multipart/Alternative'],'multipart/alternative')
    data['mail_type'] = data['mail_type'].replace(['Multipart/Mixed'],'multipart/mixed')
    data['mail_type'] = data['mail_type'].replace(['Text/Html'],'text/html')
    data['mail_type'] = data['mail_type'].replace(['text/html '],'text/html')
    
    return data

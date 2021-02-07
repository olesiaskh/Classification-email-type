def tld_clean(data):
    """
    Separate organization name and domain name if they are still together in the 'tld' column
    Replace the current organization name with the extracted organization name
    Double domain names (such as 'gov.fr' are kept as one domain name)
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
    """
    Fix differences in spelling of the same values
    """
    data['mail_type'] = data['mail_type'].replace(['Multipart/Alternative'],'multipart/alternative')
    data['mail_type'] = data['mail_type'].replace(['Multipart/Mixed'],'multipart/mixed')
    data['mail_type'] = data['mail_type'].replace(['Text/Html'],'text/html')
    data['mail_type'] = data['mail_type'].replace(['text/html '],'text/html')
    
    return data

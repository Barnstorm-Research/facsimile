'''
 This is a stand in for the FERMI tool.
 Computes  zone dependent constants
 First value is the transmission rate in the zone
 second number is the recovery rate out of the zone
'''

def fermi(query,indexvalue):
    """
    Stand in for a call to the Fermi Framework
    Args:
       query: string containing the query to pass to Fermi
       indexvalue: parameters for the query
    Returns:
       answer: Answer to the query returned by Fermi. Empty if the query failed
    """
    if query=='infrecrates':
        return infrecrate(indexvalue)
    else:
        return []

def infrecrate(zone):
    """
    Stand in for Fermi query execution
    Args:
        zone: Region element
    Returns:
        parameters: Value of the three parameters
    """
    if zone == 'Metroton':
        return [1e-4,1e-2,1e-5]
    elif zone == 'Suburbium':
        return [1e-3,1e-2,1e-4]
    else:
        return [1e-4,1e-2,1e-5]

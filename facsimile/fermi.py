#
# This is the FERMI part.
# Computes  zone dependent constants
# First value is the transmission rate in the zone
# second number is the recovery rate out of the zone
#

def fermi(query,indexvalue):
    """

    :param query:
    :param indexvalue:
    :return:
    """
    if query=='infrecrates':
        return infrecrate(indexvalue)
    else:
        return []

def infrecrate(zone):
    """

    :param zone: Metroton, Suburbium or will return a default
    :return:
    """
    if zone == 'Metroton':
        return [1e-4,1e-2,1e-5]
    elif zone == 'Suburbium':
        return [1e-3,1e-2,1e-4]
    else:
        return [1e-4,1e-2,1e-5]

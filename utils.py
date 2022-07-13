def get_id_from_data(data: str, index):
    """
    get id from data
    :param data: data from callback
    :param index: index of information
    """
    try:
        assert ':' in data
        return data.split(':')[index]
    except IndexError:
        return 'button expired'
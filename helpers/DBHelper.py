import base64


def DictionaryFetchOne(query):
    desc = query.description

    columns = [col[0] for col in desc]
    row = query.fetchone()
    if row is not None:
        return dict(zip(columns, row))
    else:
        return {}


def DictionaryFetchAll(query):
    desc = query.description
    columns = [col[0] for col in desc]

    # columns = []
    # for col in desc:
    #     columns.append(col[0])

    return [
        dict(zip(columns, rows)) for rows in query.fetchall()
    ]


def EncodeData(data):
    byte_msg = data.encode('ascii')
    base64_val = base64.b64encode(byte_msg)
    base64_string = base64_val.decode('ascii')

    return base64_string


def DecodeData(data):
    byte_msg = data.encode('ascii')
    base64_val = base64.b64decode(byte_msg)
    base64_string = base64_val.decode('ascii')

    return base64_string
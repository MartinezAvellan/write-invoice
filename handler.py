from app.utils.utils import get_request_id, is_str_or_dict


def handler(event, context):
    print(event)
    print(context)
    request_id = get_request_id(event, context)
    message = is_str_or_dict(event)
    try:
        body = is_str_or_dict(message['Records'][0]['body'])
    except Exception as e:
        print(e)
        raise


if __name__ == '__main__':
    eeeee = {}
    handler(eeeee, None)

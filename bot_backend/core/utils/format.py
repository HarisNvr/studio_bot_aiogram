def get_word_form(count: int, forms_type: str) -> str:
    """
    Return formated text, according to Russian grammar rules.

    :param count: User's count.
    :param forms_type: Determines which forms list to choose.
    :return: Formated text.
    """

    if forms_type == 'send':
        forms = [
            'пользователь получил',
            'пользователя получили',
            'пользователей получили'
        ]
    elif forms_type == 'block':
        forms = [
            'пользователь заблокировал',
            'пользователя заблокировали',
            'пользователей заблокировали'
        ]
    else:
        raise KeyError('Supports only "send" and "block" forms_type keys')

    count = str(count)

    if count[-1] == '1' and count != '11':
        return forms[0]
    elif count[-1] in ['2', '3', '4'] and count not in ['12', '13', '14']:
        return forms[1]
    else:
        return forms[2]

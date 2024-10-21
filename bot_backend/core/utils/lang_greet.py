from random import randint


def get_lang_greet_text(user_first_name: str) -> str:
    """
    Generates a greeting for the user depending on the random value,
    most often gives a normal greeting.

    :param user_first_name: The name of the user in str format that
        initialized the function launch
    :return: Text greeting in a random language in <str> format.
    """

    lang_greet_dict = {
        54: '<b>Да пребудет с вами сила, '
            f'<u>{user_first_name}!</u> \U0001F47D'
            'Помочь вам могу я чем?</b>',
        900: '<b>?ьчомоп мав угом я меч, '
             f'<u>{user_first_name[::-1]}</u></b> \U0001F643',
        901: f'<b>नमस्ते <u>{user_first_name}</u>, '
             'मैं आपकी कैसे मदद कर सकता हूँ?</b> \U0001F642',
        902: f'<b>Greetings <u>{user_first_name}</u>, '
             'how can I help you?</b> \U0001F642',
        903: f'<b>¡Hola! <u>{user_first_name}</u>, '
             '¿le puedo ayudar en algo?</b> \U0001F642',
        904: f'<b>你好 <u>{user_first_name}</u>, '
             '我怎么帮你？</b> \U0001F642',
        906: f'<b>مرحبا <u>{user_first_name}</u>, كيف يمكنني مساعدتك؟'
             '</b> \U0001F642',
        907: f'<b>Merhaba <u>{user_first_name}</u>, '
             'nasıl yardımcı olabilirim?</b> \U0001F642',
        908: f'<b>Konnichiwa <u>{user_first_name}</u>, '
             'dou tasukeraremasuka?</b> \U0001F642',
        909: f'<b>Hallo <u>{user_first_name}</u>, '
             'wie kann ich Ihnen helfen?</b> \U0001F642',
        910: f'<b>Bonjour <u>{user_first_name}</u>, '
             'comment puis-je vous aider?</b> \U0001F642',
        911: f'<b>Ciao <u>{user_first_name}</u>, '
             'come posso aiutarti?</b> \U0001F642',
        912: f'<b>Szia <u>{user_first_name}</u>, '
             'hogyan segíthetek?</b> \U0001F642',
        913: f'<b>Olá <u>{user_first_name}</u>, '
             'como posso ajudar?</b> \U0001F642',
        914: f'<b>Hej <u>{user_first_name}</u>, '
             'hur kan jag hjälpa dig?</b> \U0001F642',
        915: f'<b>Saluton <u>{user_first_name}</u>, '
             'kiel mi povas helpi vin?</b> \U0001F642',
        916: f'<b>Rytsas, <u>{user_first_name}</u>, '
             'skorkydoso kostagon nyke dohaeragon ao?</b> \U0001F642',
        917: f'<b>Sveiki <u>{user_first_name}</u>, '
             'kaip galiu jums padėti?</b> \U0001F642',
        918: f'<b>Բարև <u>{user_first_name}</u>, '
             'ինչպես կարող եմ օգնել ձեզ?</b> \U0001F642',
        919: f'<b>Sawubona <u>{user_first_name}</u>, '
             'ngicela ngingakusiza njani?</b> \U0001F642',
        920: f'<b>Γειά σας <u>{user_first_name}</u>, '
             'πώς μπορώ να σε βοηθήσω?</b> \U0001F642',
        'default': f'<b><u>{user_first_name}</u>, '
                   'чем я могу вам помочь?</b> \U0001F642'
    }

    lang = randint(1, 1000)
    return lang_greet_dict.get(
        lang,
        lang_greet_dict['default']
    )

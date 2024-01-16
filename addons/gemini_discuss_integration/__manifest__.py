# -*- coding: utf-8 -*-
# Copyright (c) 2024-Present Elias Owis. (<https://engelias.website//>)

{
    'name': "gemini_discuss_integration",

    'summary': "Gemini Integration with Discuss App",

    'description': """
        Supercharge your Odoo and Discuss with "Gemini Integration"! \
        This magical module lets you chat with Gemini, a brainy AI, right from your familiar interface. \
        Need a creative nudge for that email? Just ask Gemini! Want to spin out social posts in seconds? \
        Gemini's your genie. Get things done faster, smarter, and with a dash of AI magic. \
        Free API key with limits (60 queries/minute), but with enough power to boost productivity and open doors to \
        limitless possibilities. Unleash the AI within and watch your Discuss and Odoo shine!
    """,

    'author': "Elias Owis",
    'website': "https://engelias.website",
    'category': 'Uncategorized',
    'version': '0.1',

    'depends': ['base', 'base_setup', 'mail'],
    'external_dependencies': {'python': ['google-generativeai']},

    'license': 'LGPL-3',
    'maintainer': 'Elias Owis',

    'data': [
        'security/ir.model.access.csv',
        'data/gemini_model_data.xml',
        'data/mail_channel_data.xml',
        'data/user_partner_data.xml',
        'views/res_config_settings_views.xml',
    ],
    'images': [],
    'installable': True,
    'application': False,
    'auto_install': False,
}

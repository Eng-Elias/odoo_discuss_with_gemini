# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError

import google.generativeai as genai

import logging
_logger = logging.getLogger(__name__)


class GeminiModel(models.Model):
    _name = 'gemini.model'
    _description = "Gemini Model"

    name = fields.Char(string='Gemini Model', required=True)


class ResConfigSettings(models.TransientModel):
    _inherit = "res.config.settings"

    def _get_default_gemini_model(self):
        return self.env.ref('gemini_discuss_integration.gemini-pro-vision').id

    gemini_api_key = fields.Char(
        string="API Key",
        help="Provide Gemini API key here",
        config_parameter="gemini_discuss_integration.gemini_api_key"
    )
    gemini_model_id = fields.Many2one(
        'gemini.model',
        'Gemini Model',
        ondelete='cascade',
        default=_get_default_gemini_model,
        config_parameter="gemini_discuss_integration.gemini_model"
    )


class Channel(models.Model):
    _inherit = 'discuss.channel'

    def _notify_thread(self, message, msg_vals=None, **kwargs):
        rdata = super(Channel, self)._notify_thread(message, msg_vals=msg_vals, **kwargs)

        prompt = msg_vals.get('body')
        if not prompt:
            return rdata

        gemini_channel_id = self.env.ref('gemini_discuss_integration.channel_gemini')
        user_gemini = self.env.ref("gemini_discuss_integration.user_gemini")
        partner_gemini = self.env.ref("gemini_discuss_integration.partner_gemini")
        author_id = msg_vals.get('author_id')
        gemini_name = str(partner_gemini.name or '') + ', '

        _logger.info(msg_vals)

        try:
            if (
                author_id != partner_gemini.id  # prevent Gemini to reply itself
                and (
                    gemini_name in msg_vals.get('record_name', '')
                    or 'Gemini,' in msg_vals.get('record_name', '')
                )
                and self.channel_type == 'chat'     # respond to private chat with Gemini
            ):
                response_text = self._get_gemini_response(prompt=prompt).text
                self.with_user(user_gemini).message_post(
                    body=response_text,
                    message_type='comment',
                    subtype_xmlid='mail.mt_comment'
                )   # respond to Gemini channel
            elif (
                author_id != partner_gemini.id
                and msg_vals.get('model', '') == 'discuss.channel'
                and msg_vals.get('res_id', 0) == gemini_channel_id.id
            ):
                response_text = self._get_gemini_response(prompt=prompt).text
                gemini_channel_id.with_user(user_gemini).message_post(
                    body=response_text,
                    message_type='comment',
                    subtype_xmlid='mail.mt_comment'
                )
        except Exception as e:
            raise ValidationError(e)

        return rdata

    def _get_gemini_response(self, prompt):
        config_parameter = self.env['ir.config_parameter'].sudo()
        gemini_api_key = config_parameter.get_param('gemini_discuss_integration.gemini_api_key')
        gemini_model_id = config_parameter.get_param('gemini_discuss_integration.gemini_model')
        gemini_model = 'gemini-pro'
        try:
            if gemini_model_id:
                gemini_model = self.env['gemini.model'].browse(int(gemini_model_id)).name
        except Exception as e:
            gemini_model = 'gemini-pro'
            print(e)
        try:
            genai.configure(api_key=gemini_api_key)
            model = genai.GenerativeModel(gemini_model)

            chat = model.start_chat(history=[])

            response = chat.send_message(prompt)
            return response
        except Exception as e:
            raise UserError(_(e))

# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError

import google.generativeai as genai
from google.ai import generativelanguage as glm
import base64
import io
from PIL import Image

import logging
_logger = logging.getLogger(__name__)


GEMINI_MODEL = {
    'gemini_pro': 'gemini-pro',
    'gemini_pro_vision': 'gemini-pro-vision',
}


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
        attachments = msg_vals.get('attachment_ids')
        if not prompt and len(attachments) == 0:
            return rdata

        gemini_channel_id = self.env.ref('gemini_discuss_integration.channel_gemini')
        user_gemini = self.env.ref("gemini_discuss_integration.user_gemini")
        partner_gemini = self.env.ref("gemini_discuss_integration.partner_gemini")
        author_id = msg_vals.get('author_id')
        gemini_name = str(partner_gemini.name or '') + ', '

        try:
            attached_images_ids = []
            for attachment_tuple in attachments:
                attachment_id = attachment_tuple[1]
                if self.is_image_attachment(attachment_id):
                    attached_images_ids.append(attachment_id)
            if (
                author_id != partner_gemini.id  # prevent Gemini to reply itself
                and (
                    gemini_name in msg_vals.get('record_name', '')
                    or 'Gemini,' in msg_vals.get('record_name', '')
                )
                and self.channel_type == 'chat'     # respond to private chat with Gemini
            ):
                response_text = self._get_gemini_response(prompt=prompt, attached_images_ids=attached_images_ids).text
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
                response_text = self._get_gemini_response(prompt=prompt, attached_images_ids=attached_images_ids).text
                gemini_channel_id.with_user(user_gemini).message_post(
                    body=response_text,
                    message_type='comment',
                    subtype_xmlid='mail.mt_comment'
                )
        except Exception as e:
            _logger.error(e)
            raise ValidationError(e)

        return rdata

    def is_image_attachment(self, attachment_id):
        attachment = self.env['ir.attachment'].browse(attachment_id)
        data = base64.b64decode(attachment.datas)

        try:
            with Image.open(io.BytesIO(data)) as img:
                img.verify()  # Ensure image integrity
                return True
        except (IOError, SyntaxError) as e:
            return False

    def _get_gemini_response(self, prompt, attached_images_ids=[]):
        config_parameter = self.env['ir.config_parameter'].sudo()
        gemini_api_key = config_parameter.get_param('gemini_discuss_integration.gemini_api_key')
        gemini_model_id = config_parameter.get_param('gemini_discuss_integration.gemini_model')
        gemini_model = GEMINI_MODEL['gemini_pro']
        try:
            if gemini_model_id:
                gemini_model = self.env['gemini.model'].browse(int(gemini_model_id)).name
        except Exception as e:
            gemini_model = GEMINI_MODEL['gemini_pro']
            _logger.error(e)
        try:
            if len(attached_images_ids) == 0:
                gemini_model = GEMINI_MODEL['gemini_pro']
            genai.configure(api_key=gemini_api_key)
            model = genai.GenerativeModel(gemini_model)
            chat = model.start_chat(history=[])
            if gemini_model == GEMINI_MODEL['gemini_pro']:
                response = chat.send_message(prompt)
            else:
                gemini_input_parts = [glm.Part(text=prompt)]
                for attachment_id in attached_images_ids:
                    attachment = self.env['ir.attachment'].browse(attachment_id)
                    data = base64.b64decode(attachment.datas)
                    gemini_input_parts.append(
                        glm.Part(
                            inline_data=glm.Blob(
                                mime_type=attachment.mimetype,
                                data=io.BytesIO(data).read(),
                            )
                        )
                    )
                response = chat.send_message(
                    glm.Content(
                        parts=gemini_input_parts,
                    ),
                )
            return response
        except Exception as e:
            _logger.error(e)
            raise UserError(_(e))

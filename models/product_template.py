import itertools
import logging

from collections import defaultdict

from odoo import _, api, fields, models, tools
from odoo.exceptions import UserError, ValidationError

class ProductTemplate(models.Model):
    _inherit = "product.template"

    default_code = fields.Char(
        'Part Number', compute='_compute_default_code',
        inverse='_set_default_code', store=True)
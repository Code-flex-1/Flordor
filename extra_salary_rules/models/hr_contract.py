from odoo import _, api, fields, models


class HrContract(models.Model):
  _inherit = 'hr.contract'
  _description = 'Hr Contract'

  housing_allowance = fields.Float('Housing Allowance')
  transportation_allowance = fields.Float('Transportation Allowance')

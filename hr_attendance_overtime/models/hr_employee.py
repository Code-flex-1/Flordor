from odoo import _, api, fields, models


class HrEmployee(models.Model):
  _inherit = 'hr.employee'

  overtime_ids = fields.One2many(
      'hr.overtime',
      'employee_id',
      string='overtimes',
  )

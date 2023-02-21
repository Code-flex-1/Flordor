from odoo import _, api, fields, models


class HrMisstime(models.Model):
  _name = 'hr.misstime'
  _description = 'Hr Deduction Time'
  _rec_name = 'employee_id'
  employee_id = fields.Many2one(
      'hr.employee',
      string='Employee',
  )
  date = fields.Date('Deduction Time Date')
  duration = fields.Float('Duration')
  notes = fields.Text('Notes')
  overtime_batch_id = fields.Many2one(
      'hr.overtime.batch',
      string='Overtime Batch',
  )

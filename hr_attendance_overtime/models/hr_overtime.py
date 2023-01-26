from odoo import _, api, fields, models


class HrOvertime(models.Model):
  _name = 'hr.overtime'
  _description = 'Hr  Overtime'
  _rec_name = 'employee_id'
  employee_id = fields.Many2one(
      'hr.employee',
      string='Employee',
  )
  date = fields.Date('Overtime Date')
  duration = fields.Float('Duration')
  notes = fields.Text('Notes')
  overtime_batch_id = fields.Many2one('hr.overtime.batch', string='Overtime Batch')

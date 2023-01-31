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
  paid_amount = fields.Float('Paid Amount', compute='_compute_paid_amount')

  def _compute_paid_amount(self):
    for overtime in self:
      if overtime.duration >= 60 and overtime.employee_id.contract_id:
        overtime.paid_amount = (overtime.duration / 60) * (overtime.employee_id.contract_id.wage /30/
                                                           8)
      else:
        overtime.paid_amount = 0
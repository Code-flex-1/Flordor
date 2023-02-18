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
      overtime_rules = self.env['hr.overtime.rule'].search([
          ('overtime_duration', '<=', overtime.duration),
      ])
      if overtime_rules:
        selected_rule = max(overtime_rules, key=lambda rule: rule.overtime_duration)
        if selected_rule.paid_type == 'fixed':
          overtime.paid_amount = (overtime.duration / 60) * selected_rule.fixed_amount
        elif selected_rule.paid_type == 'percentage':
          overtime.paid_amount = (overtime.duration / 60) * (
              (overtime.employee_id.contract_id.wage / 30 / 8) * selected_rule.rate_amount)
        else:
          overtime.paid_amount = 0
      else:
        overtime.paid_amount = 0

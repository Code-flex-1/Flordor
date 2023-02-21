from odoo import _, api, fields, models


class HrOvertimeRule(models.Model):
  _name = 'hr.overtime.rule'
  _description = 'Hr Overtime Rule'

  name = fields.Char('Name')
  paid_type = fields.Selection(
      [
          ('fixed', 'Fixed'),
          ('percentage', 'Percentage'),
      ],
      default='fixed',
      string='Paid Type',
  )
  overtime_duration = fields.Float(
      'Overtime Duration',
      help='overtime duration in minutes',
  )

  fixed_amount = fields.Float('Fixed Amount')
  rate_amount = fields.Float('Rate Amount')

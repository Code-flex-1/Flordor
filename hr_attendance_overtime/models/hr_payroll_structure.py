from odoo import _, api, fields, models


class HrPayrollStructure(models.Model):
  _inherit = 'hr.payroll.structure'
  _description = 'Hr Payroll Structure'

  rule_ids = fields.One2many(
      'hr.salary.rule',
      'struct_id',
      string='Salary Rules',
      default=lambda self: self._get_default_rule_ids(),
  )

  @api.model
  def _get_default_rule_ids(self):
    rules = super()._get_default_rule_ids()
    rules += [(0, 0, {
        'name': _('Overtime'),
        'sequence': 1,
        'code': 'OVTR',
        'category_id': self.env.ref('hr_payroll.ALW').id,
        'condition_select': 'none',
        'amount_select': 'code',
        'amount_python_compute': 'result = payslip.total_overtime_paid_amount',
    },)]
    return rules

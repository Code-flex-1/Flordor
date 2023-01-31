from odoo import _, api, fields, models


class HrPayslip(models.Model):
  _inherit = 'hr.payslip'

  total_overtime_paid_amount = fields.Float(
      'Total OVertime Paid Amount',
      compute="_compute_total_overtime_paid_amount",
  )

  def _compute_total_overtime_paid_amount(self):
    for payslip in self:
      payslip.total_overtime_paid_amount = sum(
          payslip.employee_id.overtime_ids.filtered(lambda overtime: payslip.date_from <= overtime.
                                                    date <= payslip.date_to).mapped('paid_amount'))

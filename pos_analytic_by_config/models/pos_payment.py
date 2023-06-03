from odoo import _, api, fields, models


# inherit from pos.payment
class PosPayment(models.Model):
  _inherit = "pos.payment"

  # add analytic account to journal entry
  def _create_payment_moves(self):
    result = super(PosPayment, self)._create_payment_moves()
    result.analytic_account_id = self.session_id.config_id.account_analytic_id.id
    result.line_ids.analytic_account_id = self.session_id.config_id.account_analytic_id.id
    return result

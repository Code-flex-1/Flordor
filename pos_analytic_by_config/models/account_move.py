from odoo import models, fields


class AccountMove(models.Model):
  _inherit = 'account.move'
  analytic_account_id = fields.Many2one(
      comodel_name='account.analytic.account',
      string='Analytic Account',
      required=False,
  )

  # override create method to add analytic account
  def create(self, vals):
    result = super(AccountMove, self).create(vals)
    if self._context.get('analytic_account_id') and self._context.get('pos_analytic'):
      result.analytic_account_id = self._context.get('analytic_account_id')
    return result

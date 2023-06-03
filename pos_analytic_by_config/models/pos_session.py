# Copyright 2021 Tecnativa - David Vidal
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import models


class PosSession(models.Model):
  _inherit = "pos.session"

  def _credit_amounts(
      self,
      partial_move_line_vals,
      amount,
      amount_converted,
      force_company_currency=False,
  ):
    """We only want the analyitic account set in the sales items from the account
        move. This is called from `_get_sale_vals` but from other credit methods
        as well. To ensure that only sales items get the analytic account we flag
        the context from the former method with the proper analytic account id.
        """
    account_analytic_id = self.env.context.get("account_analytic_id")
    if account_analytic_id:
      partial_move_line_vals.update({"analytic_account_id": account_analytic_id})
    return super()._credit_amounts(partial_move_line_vals, amount, amount_converted,
                                   force_company_currency)

  def _get_sale_vals(self, key, amount, amount_converted):
    """The method that allowed to add the analytic account to the sales items
        has been dropped in v13, so we have to add it in the moment the sales
        items values are prepared.
        """
    account_analytic_id = self.config_id.account_analytic_id
    if account_analytic_id:
      return super(
          PosSession,
          self.with_context(account_analytic_id=account_analytic_id.id),
      )._get_sale_vals(key, amount, amount_converted)
    return super()._get_sale_vals(key, amount, amount_converted)

  # call close session with context

  def close_session_from_ui(self, bank_payment_method_diff_pairs=None):
    self_ctx = self.with_context(
        pos_analytic=True,
        analytic_account_id=self.config_id.account_analytic_id.id,
    )
    return super(PosSession, self_ctx).close_session_from_ui(bank_payment_method_diff_pairs)

  def action_pos_session_close(
      self,
      balancing_account=False,
      amount_to_balance=0,
      bank_payment_method_diffs=None,
  ):
    self_ctx = self.with_context(
        pos_analytic=True,
        analytic_account_id=self.config_id.account_analytic_id.id,
    )
    return super(PosSession, self_ctx).action_pos_session_close(
        balancing_account,
        amount_to_balance,
        bank_payment_method_diffs,
    )

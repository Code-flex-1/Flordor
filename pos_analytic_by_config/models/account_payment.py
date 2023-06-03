from odoo import api, fields, models


class AccountPayment(models.Model):
    _inherit = 'account.payment'

    analytic_account_id = fields.Many2one(
        comodel_name='account.analytic.account',
        string='Analytic Account',
        domain="[('partner_id', '=',partner_id)]",
        required=False,
    )


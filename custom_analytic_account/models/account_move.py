from odoo import models, fields


class AccountPayment(models.Model):
    _inherit = 'account.move'
    analytic_account_id = fields.Many2one(
        comodel_name='account.analytic.account',
        string='Analytic Account',
        required=False,
    )

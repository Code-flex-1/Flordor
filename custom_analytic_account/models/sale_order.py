from odoo import models, fields, api


class SaleOrder(models.Model):
    _inherit = "sale.order"
    analytic_account_id = fields.Many2one(
        'account.analytic.account',
        'Analytic Account',
        domain="[('partner_id', '=',partner_id)]",
    )

    @api.onchange('partner_id')
    def select_analytic_account_id(self):
        for order in self:
            if order.partner_id:
                related_accounts =self.env['account.analytic.account'].search([('partner_id', '=', order.partner_id.id)])
                order.analytic_account_id = related_accounts[-1] if related_accounts else None

    def default_get(self, fields_list):
        data = super(SaleOrder, self).default_get(fields_list)
        account = self.env['account.analytic.account'].search([('partner_id', '=', self.partner_id.id)])
        if account :
            data['analytic_account_id'] = account
        return data

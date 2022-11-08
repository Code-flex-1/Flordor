from odoo import fields, models, api


class Picking(models.Model):
    _inherit = "stock.picking"

    def button_validate(self):
        result = super().button_validate()
        # sale_order_analytic_account = self.sale_id.analytic_account_id
        # for picking in self:
        #     picking.move_lines.analytic_account_line_id = sale_order_analytic_account.id
        return result
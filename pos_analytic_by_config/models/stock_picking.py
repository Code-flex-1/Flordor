from odoo import fields, models, api


class Picking(models.Model):
  _inherit = "stock.picking"
  analytic_account_id = fields.Many2one(
      comodel_name='account.analytic.account',
      string='Analytic Account',
      required=False,
  )


  def _create_picking_from_pos_order_lines(
      self,
      location_dest_id,
      lines,
      picking_type,
      partner=False,
  ):
    result = super()._create_picking_from_pos_order_lines(
        location_dest_id,
        lines,
        picking_type,
        partner=False,
    )
    result.analytic_account_id = lines.order_id.config_id.account_analytic_id.id
    return result

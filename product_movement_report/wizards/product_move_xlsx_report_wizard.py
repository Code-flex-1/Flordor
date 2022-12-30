from datetime import datetime, date, time
from odoo import fields, models, _


class ProductMoveXlsx(models.TransientModel):
    _name = 'wizard.product.report'
    start_date = fields.Date(
        string='Start Date',
        required=True,
        default=date.today().replace(day=1, month=1),
        readonly=True,
    )
    end_date = fields.Date(
        string='End Date',
        required=True,
        default=fields.Date.today(),
    )
    location_id = fields.Many2one(
        comodel_name='stock.location',
        string='Location',
        required=True,
    )
    product_id = fields.Many2one(
        comodel_name='product.product',
        string='Product',
        required=True,
    )

    def prepare_product_moves_xlsx_report(self):
        product_moves = self.env['stock.move.line'].search(
            [
                '&',
                ('product_id', '=', self.product_id.id),
                ('state', '=', 'done'),
                '|',
                ('location_id', '=', self.location_id.id),
                ('location_dest_id', '=', self.location_id.id),
                '&',
                ('date', '<=',
                 datetime.combine(date=self.end_date, time=time.max)),
                ('date', '>=',
                 datetime.combine(date=self.start_date, time=time.max)),
            ],
            order='date',
        )
        flat_product_moves = [[
            move.date,
            move.picking_type_id.name,
            move.reference,
            str(move.qty_done)
            if self.location_id == move.location_dest_id else 0,
            str(move.qty_done)
            if self.location_id != move.location_dest_id else 0,
            str(0),
        ] for move in product_moves]
        data = {
            'start_date': self.start_date,
            'end_date': self.end_date,
            'moves': flat_product_moves,
            'product_name': self.product_id.name,
        }
        return self.env.ref(
            "product_movement_report.product_move_xlsx_action").report_action(
                self,
                data=data,
            )


class ProductReportXlsx(models.AbstractModel):
    _name = 'report.product_movement_report.report_product'
    _inherit = 'report.report_xlsx.abstract'

    def generate_xlsx_report(self, workbook, data, *args):
        sheet = workbook.add_worksheet("Report")
        head = workbook.add_format({
            'align': 'center',
            'bold': True,
            'font_size': '20px'
        })
        txt = workbook.add_format({'font_size': '10px'})
        cell_format = workbook.add_format({'font_size': '12px'})
        sheet.set_column(0, 3, 20)
        sheet.merge_range('A2:F3', 'Product Moves Report', head)
        sheet.write('A6', 'From:', cell_format)
        sheet.merge_range('B6:C6', data['start_date'], cell_format)
        sheet.write('D6', 'To:', cell_format)
        sheet.merge_range('E6:F6', data['end_date'], cell_format)
        sheet.merge_range('A7:F7', data['product_name'], cell_format)
        sheet.add_table(
            'A8:F20', {
                'columns': [
                    {
                        'header': 'Date'
                    },
                    {
                        'header': 'Operation Type'
                    },
                    {
                        'header': 'Reference'
                    },
                    {
                        'header': 'In'
                    },
                    {
                        'header': 'Out'
                    },
                    {
                        'header': 'Balance'
                    },
                ],
                'data':
                data['moves'],
            })

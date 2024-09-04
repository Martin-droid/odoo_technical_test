from odoo import models, api

class ProfitReport(models.AbstractModel):
    _name = 'report.client_app.profit_report'

    @api.model
    def _get_report_values(self, docids, data=None):
        orders = self.env['client.app.order'].browse(docids)
        total_revenue = sum(order.total_amount for order in orders)
        total_discount = sum(order.discount for order in orders)
        total_profit = total_revenue - total_discount - sum(order.advance_payment for order in orders)
        
        return {
            'doc_ids': docids,
            'doc_model': 'client.app.order',
            'docs': orders,
            'total_revenue': total_revenue,
            'total_discount': total_discount,
            'total_profit': total_profit,
        }

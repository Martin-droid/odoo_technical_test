from odoo import http
from odoo.http import request

class ClientApp(http.Controller):

    @http.route('/api/order/<int:order_id>', auth='public', methods=['GET'])
    def order(self, order_id):
        order = request.env['client.app.order'].sudo().browse(order_id)
        if order:
            return {
                'order_id': order.id,
                'order_name': order.name,
                'customer_id': order.customer_id.id,
                'total_amount': order.total_amount,
                'state': order.state,
                'delivery_date': order.delivery_date,
                'notes': order.notes,
                'priority': order.priority
            }
        return {'error': 'Order not found'}, 404

    @http.route('/api/order/<int:order_id>/payments', auth='public', methods=['GET'])
    def order_payments(self, order_id):
        payments = request.env['client.app.payment'].sudo().search([('order_id', '=', order_id)])
        if payments:
            return [{'payment_id': p.id, 'amount': p.amount, 'payment_date': p.payment_date, 'payment_method': p.payment_method, 'transaction_id': p.transaction_id} for p in payments]
        return {'error': 'No payments found'}, 404

    @http.route('/api/order/invoice/<int:invoice_id>', auth='public', methods=['GET'])
    def order_invoice(self, invoice_id):
        invoice = request.env['client.app.invoice'].sudo().browse(invoice_id)
        if invoice:
            return {
                'invoice_id': invoice.id,
                'invoice_number': invoice.name,
                'order_id': invoice.order_id.id,
                'total_amount': invoice.total_amount,
                'invoice_date': invoice.invoice_date,
                'is_paid': invoice.is_paid,
                'due_date': invoice.due_date,
                'payment_status': invoice.payment_status
            }
        return {'error': 'Invoice not found'}, 404

    @http.route('/api/orders', auth='public', methods=['GET'])
    def orders(self, **kwargs):
        orders = request.env['client.app.order'].sudo().search([])
        return [{
            'order_id': order.id,
            'order_name': order.name,
            'customer_id': order.customer_id.id,
            'total_amount': order.total_amount,
            'state': order.state,
            'delivery_date': order.delivery_date,
            'notes': order.notes,
            'priority': order.priority
        } for order in orders]

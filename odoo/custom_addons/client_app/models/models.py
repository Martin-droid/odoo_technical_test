from odoo import models, fields, api
from odoo.exceptions import UserError

class ClientAppOrder(models.Model):
    _name = 'client.app.order'
    _description = 'Client Order Management'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(string="Order Name", required=True, tracking=True)
    customer_id = fields.Many2one('res.partner', string="Customer", required=True, tracking=True)
    order_date = fields.Date(string="Order Date", default=fields.Date.context_today, required=True, tracking=True)
    delivery_date = fields.Date(string="Delivery Date", required=True, tracking=True)
    total_amount = fields.Float(string="Total Amount", required=True, tracking=True)
    advance_payment = fields.Float(string="Advance Payment", compute='_compute_advance_payment', store=True, tracking=True)
    state = fields.Selection([
        ('draft', 'Draft'),
        ('confirmed', 'Confirmed'),
        ('delivered', 'Delivered'),
        ('cancelled', 'Cancelled'),
        ('closed', 'Closed')
    ], string="Status", default='draft', required=True, tracking=True)
    notes = fields.Text(string="Order Notes")
    priority = fields.Selection([('low', 'Low'), ('medium', 'Medium'), ('high', 'High')], string="Priority", default='medium')
    discount = fields.Float(string="Discount", compute='_compute_discount')

    @api.depends('total_amount')
    def _compute_advance_payment(self):
        for order in self:
            order.advance_payment = 0.4 * order.total_amount

    @api.depends('state')
    def _compute_discount(self):
        for order in self:
            if order.state == 'delivered':
                order.discount = order.total_amount * 0.02

    def confirm_order(self):
        self.state = 'confirmed'
        self.message_post(body="Order confirmed.")

    def deliver_order(self):
        self.state = 'delivered'
        self.message_post(body="Order delivered.")

    def cancel_order(self):
        if self.state != 'delivered':
            self.state = 'cancelled'
            self.message_post(body="Order cancelled.")
        else:
            raise UserError("Cannot cancel a delivered order.")

    def close_order(self):
        self.state = 'closed'
        self.message_post(body="Order closed.")

    def apply_discount(self):
        if self.state == 'delivered':
            self.total_amount *= 0.98
            self.message_post(body="2% discount applied due to late delivery.")

class ClientAppPayment(models.Model):
    _name = 'client.app.payment'
    _description = 'Client Payment Management'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    order_id = fields.Many2one('client.app.order', string="Order", required=True, tracking=True)
    customer_id = fields.Many2one('res.partner', string="Customer", related='order_id.customer_id', store=True, tracking=True)
    amount = fields.Float(string="Payment Amount", required=True, tracking=True)
    payment_date = fields.Date(string="Payment Date", default=fields.Date.context_today, required=True, tracking=True)
    invoice_id = fields.Many2one('client.app.invoice', string="Invoice", tracking=True)
    payment_method = fields.Selection([('bank', 'Bank Transfer'), ('credit', 'Credit Card'), ('paypal', 'PayPal')], string="Payment Method", required=True)
    transaction_id = fields.Char(string="Transaction ID")
    
    @api.constrains('amount')
    def _check_amount(self):
        for payment in self:
            if payment.amount <= 0:
                raise UserError("The payment amount must be greater than zero.")

class ClientAppInvoice(models.Model):
    _name = 'client.app.invoice'
    _description = 'Client Invoice Management'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(string="Invoice Number", required=True, tracking=True)
    order_id = fields.Many2one('client.app.order', string="Order", required=True, tracking=True)
    total_amount = fields.Float(string="Total Amount", required=True, tracking=True)
    invoice_date = fields.Date(string="Invoice Date", default=fields.Date.context_today, required=True, tracking=True)
    is_paid = fields.Boolean(string="Paid", default=False, tracking=True)
    due_date = fields.Date(string="Due Date", required=True)
    payment_status = fields.Selection([('unpaid', 'Unpaid'), ('paid', 'Paid'), ('overdue', 'Overdue')], string="Payment Status", compute='_compute_payment_status', store=True)

    @api.depends('is_paid', 'due_date')
    def _compute_payment_status(self):
        for invoice in self:
            if invoice.is_paid:
                invoice.payment_status = 'paid'
            elif invoice.due_date and fields.Date.context_today(self) > invoice.due_date:
                invoice.payment_status = 'overdue'
            else:
                invoice.payment_status = 'unpaid'

    @api.constrains('due_date')
    def _check_due_date(self):
        for invoice in self:
            if invoice.due_date < invoice.invoice_date:
                raise UserError("Due date cannot be earlier than the invoice date.")

import jwt
import datetime
from odoo import http
from odoo.http import request

SECRET_KEY = ''

class ClientAppAuth(http.Controller):

    def generate_jwt_token(self, user):
        payload = {
            'user_id': user.id,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=24)
        }
        return jwt.encode(payload, SECRET_KEY, algorithm='HS256')

    def decode_jwt_token(self, token):
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
            return request.env['res.users'].sudo().browse(payload['user_id'])
        except jwt.ExpiredSignatureError:
            return None
        except jwt.InvalidTokenError:
            return None

    @http.route('/api/customer/login', auth='public', methods=['POST'], csrf=False)
    def login(self, **kwargs):
        username = kwargs.get('username')
        password = kwargs.get('password')
        user = request.env['res.users'].sudo().search([('login', '=', username)], limit=1)
        if user and user._check_password(password):
            token = self.generate_jwt_token(user)
            return {'token': token}
        return {'error': 'Invalid credentials'}, 401

    @http.route('/api/customer/logout', auth='public', methods=['POST'], csrf=False)
    def logout(self, **kwargs):
        # JWT token invalidation logic (if needed)
        return {'message': 'Logged out successfully'}

    @http.route('/api/customer/profile', auth='user', methods=['GET'])
    def profile(self, **kwargs):
        token = kwargs.get('token')
        user = self.decode_jwt_token(token)
        if user:
            return {
                'user_id': user.id,
                'name': user.name,
                'email': user.email,
                'phone': user.phone
            }
        return {'error': 'Invalid or expired token'}, 401

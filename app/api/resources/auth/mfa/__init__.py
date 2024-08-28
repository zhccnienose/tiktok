from flask import Blueprint
from flask_restful import Api

from .QRcode import MfaQRcode
from .bind import MfaBind
mfa_bp = Blueprint('mfa', __name__, url_prefix='/mfa')
mfa = Api(mfa_bp)

mfa.add_resource(MfaQRcode, "/qrcode",methods=['GET'])
mfa.add_resource(MfaBind,'/bind',methods=['POST'])

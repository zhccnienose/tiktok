import qrcode
import base64
from io import BytesIO


def make_qrcode(data) -> str:
    # 创建一个二维码对象，并设置需要编码的内容
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(data)
    qr.make(fit=True)
    # 生成二维码图像
    img = qr.make_image(fill='black', back_color='white')
    img.save('qrcode.png')
    # 图像转base64
    buf = BytesIO()
    img.save(buf, format='PNG')
    heximage = base64.b64encode(buf.getvalue())
    return 'avatar:image/png;base64,' + heximage.decode()

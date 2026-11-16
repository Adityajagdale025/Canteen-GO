import io
from django.core.files.base import ContentFile
import qrcode


def generate_order_qr(order):
  qr_payload = f'CANTEENGO:{order.token_number}:{str(order.order_uuid)}'
  qr = qrcode.QRCode(
      version=1,
      error_correction=qrcode.constants.ERROR_CORRECT_M,
      box_size=8,
      border=3,
  )
  qr.add_data(qr_payload)
  qr.make(fit=True)
  img = qr.make_image(fill_color='black', back_color='white')

  buffer = io.BytesIO()
  img.save(buffer, format='PNG')
  filename = f'qr_{order.token_number}_{order.id}.png'
  order.qr_code.save(filename, ContentFile(buffer.getvalue()), save=False)
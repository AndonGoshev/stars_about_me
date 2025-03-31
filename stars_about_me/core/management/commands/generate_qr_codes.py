import os
import uuid

import qrcode
from django.core.management import BaseCommand

from stars_about_me import settings
from stars_about_me.core.models import QrCode

QR_FOLDER = 'media/testcodes/'

class Command(BaseCommand):
    help = 'Generate QR codes'

    def add_arguments(self, parser):
        parser.add_argument('--count', type=int, default=10, help='Number of QR codes to generate')

    def handle(self, *args, **kwargs):
        count = kwargs['count']

        if not os.path.exists(QR_FOLDER):
            os.makedirs(QR_FOLDER)  # Ensure directory exists

        for _ in range(count):
            qr_id = str(uuid.uuid4())[:8]
            qr_url = f'localhost:8000/luckies/{qr_id}.jpg'

            qr = qrcode.make(qr_url)
            qr_path = os.path.join(QR_FOLDER, f"{qr_id}.png")
            qr.save(qr_path)

            QrCode.objects.create(qr_id=qr_id, scanned=False)

            self.stdout.write(self.style.SUCCESS(f"Generated QR: {qr_id} → {qr_path}"))

        self.stdout.write(self.style.SUCCESS(f"✅ {count} QR codes generated successfully!"))
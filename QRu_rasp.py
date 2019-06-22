from QRu_rasp import apiclient, overlay, scanner
import os
import sys

# Default configuration of the scanner
resolution = (1024,768)
roi = (0.33, 0.33)
opacity = 128

API_KEY = os.environ.get('API_KEY')
API_URL = os.environ.get('API_URL')

if API_KEY is None or API_URL is None:
    print("Usage: API_KEY=... API_URL=... " + sys.argv[0])
    sys.exit(-1)

client = apiclient.APIClient(API_KEY, API_URL)
overlay = overlay.ROIOverlay(resolution, roi, opacity)
scanner = scanner.Scanner(overlay, client.verify_token)

scanner.run()

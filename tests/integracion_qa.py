"""Pruebas de integración: ejecuta docs/qa.html (38 pruebas sobre el motor exportado) en Chromium headless.

Uso: python tests/integracion_qa.py   (requiere: pip install playwright && playwright install chromium)
Sale con código 1 si alguna prueba falla. Actualiza docs/pruebas-resultados.json y docs/evidence/.
"""
import json, sys, threading
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'tools'))
import serve_game
from playwright.sync_api import sync_playwright

server = serve_game.make_server(0)
threading.Thread(target=server.serve_forever, daemon=True).start()
try:
    with sync_playwright() as pw:
        browser = pw.chromium.launch(args=['--use-gl=swiftshader', '--autoplay-policy=no-user-gesture-required'])
        page = browser.new_page()
        page.goto(f'http://127.0.0.1:{server.server_port}/docs/qa.html')
        page.click('#run')
        page.wait_for_function("document.querySelector('#report').textContent.length>0", timeout=180_000)
        report = json.loads(page.text_content('#report'))
        browser.close()
finally:
    server.shutdown()

for r in report['results']:
    print(('PASS ' if r['status'] == 'PASS' else 'FAIL ') + r['name'] + ('' if r['status'] == 'PASS' else ': ' + r['error']))
print(f"\n{report['passed']} / {report['total']} pruebas de integración aprobadas")
sys.exit(0 if report['passed'] == report['total'] else 1)

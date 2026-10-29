"""Pruebas unitarias del servidor local: solo acepta evidencia válida en rutas fijas."""
import sys, tempfile, threading, unittest, urllib.request, urllib.error
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'tools'))
import serve_game

PNG = b'\x89PNG\r\n\x1a\n' + b'0' * 32


class ServidorQA(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.tmp = tempfile.TemporaryDirectory()
        serve_game.root = Path(cls.tmp.name)  # escribe en una carpeta temporal, no en docs/
        cls.server = serve_game.make_server(0)
        cls.url = f'http://127.0.0.1:{cls.server.server_port}'
        threading.Thread(target=cls.server.serve_forever, daemon=True).start()

    @classmethod
    def tearDownClass(cls):
        cls.server.shutdown(); cls.server.server_close(); cls.tmp.cleanup()

    def post(self, path, data):
        try:
            return urllib.request.urlopen(urllib.request.Request(self.url + path, data=data, method='POST')).status
        except urllib.error.HTTPError as e:
            e.close()
            return e.code

    def test_guarda_reporte_json(self):
        self.assertEqual(self.post('/__qa/report.json', b'{"passed":1}'), 200)
        self.assertEqual((serve_game.root / 'docs/pruebas-resultados.json').read_bytes(), b'{"passed":1}')

    def test_guarda_captura_png(self):
        self.assertEqual(self.post('/__qa/juego.png', PNG), 200)
        self.assertTrue((serve_game.root / 'docs/evidence/juego.png').exists())

    def test_rechaza_ruta_no_permitida(self):
        self.assertEqual(self.post('/__qa/../../evil.txt', b'x'), 404)
        self.assertEqual(self.post('/__qa/otro.png', PNG), 404)

    def test_rechaza_json_invalido(self):
        self.assertEqual(self.post('/__qa/report.json', b'no es json'), 400)

    def test_rechaza_png_falso(self):
        self.assertEqual(self.post('/__qa/boss.png', b'GIF89a'), 400)

    def test_rechaza_cuerpo_vacio(self):
        self.assertEqual(self.post('/__qa/report.json', b''), 400)


if __name__ == '__main__':
    unittest.main()

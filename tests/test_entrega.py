"""Pruebas unitarias de integridad de la entrega: proyecto Construct y exportación HTML5."""
import json, unittest, zipfile
import xml.etree.ElementTree as ET
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
EXPORT = ROOT / 'export/html5'
AUDIO = ['parque', 'batalla', 'recoger', 'correcto', 'error', 'victoria', 'fin', 'aviso', 'lanzar', 'golpe']


class Proyecto(unittest.TestCase):
    def setUp(self):
        self.capx = zipfile.ZipFile(ROOT / 'EcoGame.capx')

    def tearDown(self):
        self.capx.close()

    def test_capx_sin_corrupcion(self):
        self.assertIsNone(self.capx.testzip())

    def test_capx_contiene_proyecto_layout_y_eventos(self):
        for name in ['EcoGame.caproj', 'Layouts/Layout 1.xml', 'Event sheets/Event sheet 1.xml']:
            ET.fromstring(self.capx.read(name))  # XML bien formado

    def test_layout_tiene_cuatro_capas(self):
        layout = ET.fromstring(self.capx.read('Layouts/Layout 1.xml'))
        self.assertEqual([l.get('name') for l in layout.iter('layer')], ['Fondo', 'Parque', 'Interfaz', 'Pantallas'])

    def test_variables_globales_del_juego(self):
        sheet = self.capx.read('Event sheets/Event sheet 1.xml').decode('utf-8')
        for var in ['State', 'Score', 'Lives', 'TimeLeft', 'Carry', 'BossHP']:
            self.assertIn(f'name="{var}"', sheet)


class Exportacion(unittest.TestCase):
    def test_archivos_principales(self):
        for name in ['index.html', 'c2runtime.js', 'data.js', 'appmanifest.json']:
            self.assertTrue((EXPORT / name).is_file(), name)

    def test_data_js_es_json_valido(self):
        data = json.loads((EXPORT / 'data.js').read_text(encoding='utf-8-sig'))
        self.assertIn('project', data)

    def test_manifest_y_iconos(self):
        manifest = json.loads((EXPORT / 'appmanifest.json').read_text(encoding='utf-8-sig'))
        for icon in manifest['icons']:
            self.assertTrue((EXPORT / icon['src']).is_file(), icon['src'])

    def test_audio_completo(self):
        for name in AUDIO:
            path = EXPORT / 'media' / f'{name}.ogg'
            self.assertGreater(path.stat().st_size, 1000, name)
            self.assertEqual(path.read_bytes()[:4], b'OggS', name)

    def test_sprites_son_png(self):
        images = list((EXPORT / 'images').glob('*.png'))
        self.assertGreater(len(images), 20)
        for img in images:
            self.assertEqual(img.read_bytes()[:8], b'\x89PNG\r\n\x1a\n', img.name)


if __name__ == '__main__':
    unittest.main()

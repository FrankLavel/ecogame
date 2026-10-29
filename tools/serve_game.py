"""Local-only launcher for the exported Construct game and its acceptance tests."""
from http.server import ThreadingHTTPServer, SimpleHTTPRequestHandler
from pathlib import Path
from functools import partial
import argparse, webbrowser, threading, json

root=Path(__file__).resolve().parents[1]
class Handler(SimpleHTTPRequestHandler):
    def do_POST(self):
        # Test evidence is local and constrained to these explicit destinations.
        paths={'/__qa/report.json':'docs/pruebas-resultados.json',
               '/__qa/juego.png':'docs/evidence/juego.png',
               '/__qa/victoria.png':'docs/evidence/victoria.png',
               '/__qa/boss.png':'docs/evidence/boss.png',
               '/__qa/intro.png':'docs/evidence/intro.png',
               '/__qa/embestida.png':'docs/evidence/embestida.png',
               '/__qa/pausa.png':'docs/evidence/pausa.png'}
        if self.path not in paths:
            self.send_error(404);return
        try:size=int(self.headers.get('Content-Length','0'))
        except ValueError:size=0
        if not 0<size<8_000_000:
            self.send_error(400);return
        data=self.rfile.read(size)
        if self.path.endswith('.json'):
            try:json.loads(data)
            except ValueError:
                self.send_error(400);return
        elif not data.startswith(b'\x89PNG\r\n\x1a\n'):
            self.send_error(400);return
        dest=root/paths[self.path];dest.parent.mkdir(parents=True,exist_ok=True);dest.write_bytes(data)
        self.send_response(200);self.end_headers();self.wfile.write(b'OK')
def make_server(port):
    return ThreadingHTTPServer(('127.0.0.1',port),partial(Handler,directory=str(root)))
if __name__=='__main__':
    p=argparse.ArgumentParser()
    p.add_argument('--port',type=int,default=8765)
    p.add_argument('--no-browser',action='store_true')
    args=p.parse_args()
    server=make_server(args.port)
    url=f'http://127.0.0.1:{args.port}/export/html5/'
    print('EcoGame: '+url,flush=True)
    print('Mantén esta ventana abierta mientras juegas. Ctrl+C para cerrar.',flush=True)
    if not args.no_browser:threading.Timer(.5,lambda:webbrowser.open(url)).start()
    try:server.serve_forever()
    except KeyboardInterrupt:server.server_close()

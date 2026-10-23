#!/usr/bin/env python3
import os
import sys
import json
from http.server import SimpleHTTPRequestHandler, HTTPServer

# Добавляем корневую директорию проекта в путь поиска модулей, чтобы импортировать ai_core
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from ai_core.filter import AICoreFilter

class PlanetaryNodeAPI(SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        self.ai_filter = AICoreFilter()
        super().__init__(*args, **kwargs)

    def do_GET(self):
        """Маршрутизация GET-запросов: отдача статики и статуса ноды"""
        if self.path == '/' or self.path == '/index.html':
            self.path = '/app/index.html'
            return super().do_GET()
        
        elif self.path == '/api/v1/node/status':
            # Имитация системного API статуса P2P-ноды и начисления CI
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            
            status_data = {
                "node_id": "PI-883-ALPHA",
                "network_type": "Web4 P2P (Hydra)",
                "peers_connected": 142,
                "memory_allocated_gb": 2.0,
                "status": "ONLINE"
            }
            self.wfile.write(json.dumps(status_data).encode('utf-8'))
        else:
            return super().do_GET()

    def do_POST(self):
        """Маршрутизация POST-запросов: обработка научных заявок через ИИ-ядро"""
        if self.path == '/api/v1/project/analyze':
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            
            try:
                payload = json.loads(post_data.decode('utf-8'))
                title = payload.get('title', 'Без названия')
                text = payload.get('text', '')
                
                # Запускаем контур фильтрации и кросс-анализа ИИ, созданный ранее
                ai_report_json = self.ai_filter.process_project(title, text)
                
                self.send_response(200)
                self.send_header('Content-Type', 'application/json')
                self.send_header('Access-Control-Allow-Origin', '*')
                self.end_headers()
                self.wfile.write(ai_report_json.encode('utf-8'))
                
            except Exception as e:
                self.send_response(400)
                self.end_headers()
                self.wfile.write(json.dumps({"status": "ERROR", "reason": str(e)}).encode('utf-8'))

def run(server_class=HTTPServer, handler_class=PlanetaryNodeAPI, port=8080):
    # Корректно меняем рабочую директорию на корень проекта для раздачи index.html
    os.chdir(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print(f"Planetary API Server started on port {port}...")
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        httpd.server_close()

if __name__ == "__main__":
    run()

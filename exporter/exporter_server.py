"""
exporter_server.py
------------------
Servidor HTTP responsável por expor as métricas Prometheus
coletadas pelo sistema (e futuramente pelo Firebird).
"""

from prometheus_client import start_http_server
import threading


def start_exporter_server(port: int = 8000):
    """
    Inicia o servidor HTTP que expõe as métricas em /metrics.

    Args:
        port (int): Porta de escuta (padrão: 8000).
    """
    try:
        thread = threading.Thread(target=start_http_server, args=(port,))
        thread.daemon = True
        thread.start()
        print(f"[OK] Servidor Exporter iniciado em http://localhost:{port}/metrics")
    except Exception as e:
        print(f"[ERRO] Falha ao iniciar o Exporter: {e}")

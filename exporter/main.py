"""
main.py
-------
Ponto de entrada do Exporter de métricas do sistema e Firebird.
Inicializa o servidor HTTP (/metrics) e a coleta contínua de métricas.
"""

import threading
import time
from exporter_server import start_exporter_server
from metrics_system import collect_system_metrics
from metrics_firebird import collect_firebird_metrics


def main():
    print("=" * 60)
    print("🚀 Iniciando Exporter de Monitoramento - Python Prometheus")
    print("=" * 60)

    # 1️⃣ Inicia o servidor HTTP Prometheus (/metrics)
    start_exporter_server(port=8000)
    print("[OK] Servidor Exporter iniciado em http://localhost:8000/metrics")

    # 2️⃣ Inicia a coleta contínua de métricas do sistema
    system_thread = threading.Thread(target=collect_system_metrics, args=(5,))
    system_thread.daemon = True
    system_thread.start()
    print("🧠 Coleta de métricas do sistema iniciada...")

    # 3️⃣ Inicia a coleta de métricas do Firebird
    firebird_thread = threading.Thread(
        target=collect_firebird_metrics,
        kwargs={
            "host": "localhost",
            "database_path": r"C:\piracaiasoft\dados\PARQUE-BRASIL-LOJA1.fdb",  # ✅ Caminho Windows correto
            "user": "sysdba",
            "password": "masterkey",
            "interval": 10,
        },
    )
    firebird_thread.daemon = True
    firebird_thread.start()
    print("🔥 Coleta de métricas do Firebird iniciada...")

    # 4️⃣ Mantém o processo principal ativo
    try:
        while True:
            time.sleep(60)
    except KeyboardInterrupt:
        print("\n🛑 Exporter finalizado manualmente.")


if __name__ == "__main__":
    main()

"""
metrics_system.py
-----------------
Coleta de métricas do sistema operacional (CPU, memória, disco)
para exposição no endpoint Prometheus (/metrics).
Compatível com Linux e Windows.
"""

import psutil
from prometheus_client import Gauge
import time


# === Definição das métricas === #
cpu_usage_gauge = Gauge(
    'system_cpu_usage_percent',
    'Percentual de uso da CPU'
)

memory_usage_gauge = Gauge(
    'system_memory_usage_percent',
    'Percentual de uso da memória RAM'
)

disk_usage_gauge = Gauge(
    'system_disk_usage_percent',
    'Percentual de uso do disco principal'
)


def collect_system_metrics(interval: int = 5):
    """
    Função que coleta e atualiza métricas do sistema a cada `interval` segundos.
    Essa função será chamada em loop no main.py.
    """
    while True:
        try:
            # CPU
            cpu_percent = psutil.cpu_percent(interval=1)
            cpu_usage_gauge.set(cpu_percent)

            # Memória
            memory_percent = psutil.virtual_memory().percent
            memory_usage_gauge.set(memory_percent)

            # Disco (partição raiz)
            disk_percent = psutil.disk_usage('/').percent
            disk_usage_gauge.set(disk_percent)

        except Exception as e:
            print(f"[ERRO] Falha ao coletar métricas do sistema: {e}")

        time.sleep(interval)
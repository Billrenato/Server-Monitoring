import os
import fdb
import time
from prometheus_client import Gauge

firebird_up = Gauge('firebird_up', 'Status do banco de dados Firebird (1 = online, 0 = offline)')
firebird_latency = Gauge('firebird_query_latency_seconds', 'Tempo de resposta da consulta de teste (ping) ao Firebird, em segundos')
firebird_connections = Gauge('firebird_active_connections', 'Número de conexões ativas ao banco (estimado para Firebird 2.5.9)')

def collect_firebird_metrics(interval=10):
    host = os.getenv("FIREBIRD_HOST", "host.docker.internal")
    database = os.getenv("FIREBIRD_DB")
    user = os.getenv("FIREBIRD_USER", "sysdba")
    password = os.getenv("FIREBIRD_PASSWORD", "masterkey")

    dsn = f"{host}:{database}"
    print(f"🔥 Iniciando coleta de métricas do Firebird em {dsn}")

    while True:
        try:
            start_time = time.time()
            with fdb.connect(dsn=dsn, user=user, password=password, charset="WIN1252") as con:
                cur = con.cursor()
                cur.execute("SELECT 1 FROM RDB$DATABASE;")
                cur.fetchone()
                latency = time.time() - start_time
                firebird_latency.set(latency)
                firebird_up.set(1)

                # Conexões ativas
                cur.execute("""
                    SELECT COUNT(*) 
                    FROM MON$ATTACHMENTS 
                    WHERE MON$SYSTEM_FLAG = 0
                """)
                result = cur.fetchone()
                firebird_connections.set(result[0] if result else 0)

        except Exception as e:
            print(f"[ERRO] Falha ao conectar ao Firebird: {e}")
            firebird_up.set(0)
            firebird_latency.set(0)
            firebird_connections.set(0)

        time.sleep(interval)

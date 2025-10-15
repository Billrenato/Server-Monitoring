import fdb
import time
from prometheus_client import Gauge

firebird_up = Gauge('firebird_up', 'Status do banco de dados Firebird (1 = online, 0 = offline)')
firebird_latency = Gauge('firebird_query_latency_seconds', 'Tempo de resposta da consulta de teste (ping) ao Firebird, em segundos')
firebird_connections = Gauge('firebird_active_connections', 'Número de conexões ativas ao banco (estimado para Firebird 2.5.9)')

def collect_firebird_metrics(host="localhost", database_path="C:/piracaiasoft/dados/PARQUE-BRASIL-LOJA1.fdb",
                             user="sysdba", password="masterkey", interval=10):
    """Conecta ao Firebird periodicamente e atualiza as métricas."""
    
    dsn = f"{host}:{database_path}"  # ✅ Corrigido
    print(f"🔥 Iniciando coleta de métricas do Firebird em {dsn}")

    while True:
        try:
            start_time = time.time()
            with fdb.connect(dsn=dsn, user=user, password=password) as con:
                cur = con.cursor()
                cur.execute("SELECT 1 FROM RDB$DATABASE;")
                cur.fetchone()
                latency = time.time() - start_time
                firebird_latency.set(latency)
                firebird_up.set(1)

            try:
                cur.execute("""
                    SELECT COUNT(*) 
                    FROM MON$ATTACHMENTS 
                    WHERE MON$SYSTEM_FLAG = 0
                """)
                result = cur.fetchone()
                firebird_connections.set(result[0] if result else 0)
            except Exception:
                # Se falhar, atribui 0 (ou -1 se quiser indicar erro)
                firebird_connections.set(0)
        except Exception as e:
            print(f"[ERRO] Falha ao coletar métricas do Firebird: {e}")
            firebird_up.set(0)
            firebird_latency.set(0)
            firebird_connections.set(0)

        time.sleep(interval)

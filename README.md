# Firebird & System Metrics Exporter - Python Prometheus

## Sumário

1. Descrição
2. Funcionalidades
3. Pré-requisitos
4. Instalação
5. Configuração
6. Estrutura do Projeto
7. Uso
8. Métricas Disponíveis
9. Integração com Prometheus e Grafana
10. Docker e CI/CD
11. Licença

---

## Descrição

Este projeto implementa um Exporter em Python que coleta métricas do banco de dados Firebird 2.5.9 e do sistema operacional (CPU, memória e disco), expondo-as em um endpoint HTTP compatível com Prometheus. O Exporter permite monitoramento contínuo do desempenho do banco de dados e do servidor, podendo ser integrado facilmente a dashboards como Grafana.

---

## Funcionalidades

* Coleta de métricas do Firebird:

  * Status do banco (online/offline)
  * Latência de consulta de teste (ping)
  * Número de conexões ativas

* Coleta de métricas do sistema operacional:

  * Percentual de uso de CPU
  * Percentual de uso de memória RAM
  * Percentual de uso do disco principal

* Servidor HTTP para exposição das métricas no padrão Prometheus (`/metrics`)

* Coleta contínua em threads separadas

* Intervalos de coleta configuráveis

---

## Pré-requisitos

* Python 3.10 ou superior
* Banco de dados Firebird 2.5.9 ou compatível
* Bibliotecas Python:

```bash
pip install psutil fdb prometheus_client
```

---

## Instalação

1. Clone o repositório:

```bash
git clone https://github.com/seu-usuario/firebird-exporter.git
cd firebird-exporter
```

2. Instale as dependências:

```bash
pip install -r requirements.txt
```

3. Configure o caminho do banco Firebird e credenciais no arquivo `main.py` ou via variáveis de ambiente.

---

## Configuração

No arquivo `main.py`, configure os parâmetros do Firebird:

```python
firebird_thread = threading.Thread(
    target=collect_firebird_metrics,
    kwargs={
        "host": "localhost",
        "database_path": r"C:\piracaiasoft\dados\banco-dados.fdb",
        "user": "sysdba",
        "password": "masterkey",
        "interval": 10,
    },
)
```

Parâmetros:

* `host`: endereço do servidor Firebird
* `database_path`: caminho completo do arquivo `.fdb`
* `user`: usuário do banco
* `password`: senha do banco
* `interval`: intervalo de coleta em segundos

No arquivo `metrics_system.py`, é possível definir o intervalo de coleta das métricas do sistema:

```python
collect_system_metrics(interval=5)
```

---

## Estrutura do Projeto

```
firebird-exporter/
│
├── main.py                 # Ponto de entrada do Exporter
├── metrics_system.py       # Coleta de métricas do sistema operacional
├── metrics_firebird.py     # Coleta de métricas do Firebird
├── exporter_server.py      # Inicialização do servidor Prometheus (/metrics)
├── requirements.txt        # Dependências do projeto
└── README.md               # Documentação
```

---

## Uso

Para executar o Exporter:

```bash
python main.py
```

O servidor HTTP será iniciado em:

```
http://localhost:8000/metrics
```

As métricas podem ser acessadas diretamente pelo Prometheus ou navegador.

Para encerrar o Exporter:

```bash
CTRL + C
```

---

## Métricas Disponíveis

### Firebird

| Métrica                          | Descrição                                          |
| -------------------------------- | -------------------------------------------------- |
| `firebird_up`                    | Status do banco Firebird (1 = online, 0 = offline) |
| `firebird_query_latency_seconds` | Latência da consulta de teste em segundos          |
| `firebird_active_connections`    | Número de conexões ativas no banco                 |

### Sistema Operacional

| Métrica                       | Descrição                            |
| ----------------------------- | ------------------------------------ |
| `system_cpu_usage_percent`    | Percentual de uso da CPU             |
| `system_memory_usage_percent` | Percentual de uso da memória RAM     |
| `system_disk_usage_percent`   | Percentual de uso do disco principal |

---

## Integração com Prometheus e Grafana

1. Configure o Prometheus para coletar métricas do Exporter:

```yaml
scrape_configs:
  - job_name: 'firebird_exporter'
    static_configs:
      - targets: ['localhost:8000']
```

2. No Grafana, crie dashboards utilizando as métricas expostas:

   * Gráficos de CPU, memória e disco do servidor
   * Gráficos de disponibilidade e latência do Firebird
   * Painéis de conexões ativas no banco

---

## Docker e CI/CD

O projeto pode ser containerizado para facilitar deploy e integração contínua.

Exemplo de Dockerfile:

```dockerfile
FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["python", "main.py"]
```

Recomenda-se utilizar variáveis de ambiente para passar credenciais do Firebird ao container, evitando hardcoding. O Exporter está pronto para pipelines CI/CD, permitindo build e deploy automáticos.

---

## Licença

Este projeto está licenciado sob a Licença MIT.

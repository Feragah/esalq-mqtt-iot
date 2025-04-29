# MBA USP Esalq - IoT - Demonstração do protocolo MQTT com Mosquitto

Este projeto faz parte da aula prática de demonstração do protocolo **MQTT** utilizando o middleware **Mosquitto**. O objetivo é ilustrar o funcionamento do padrão **publish/subscribe** por meio de dois sensores que publicam dados (temperatura e umidade) em um broker MQTT, enquanto um _dashboard_ permanece assinante (subscriber) do tópico e é notificado a cada nova mensagem recebida.

---

## Clonando o Repositório

Para obter o código-fonte do projeto, clone o repositório diretamente do GitHub:

```bash
git clone https://github.com/Feragah/esalq-mqtt-iot
cd esalq-mqtt-iot
```

---

## Índice

1. [Pré-requisitos](#pré-requisitos)
2. [Estrutura do Projeto](#estrutura-do-projeto)
3. [Passo a Passo - Execução Inicial](#passo-a-passo---execução-inicial)
4. [Visualização dos Logs](#visualização-dos-logs)
5. [Encerrando os Recursos](#encerrando-os-recursos)
6. [Ajustando os Tópicos de Publicação](#ajustando-os-tópicos-de-publicação)
7. [Rodando o Dashboard Gráfico](#rodando-o-dashboard-gráfico)
8. [Desafios] (#desafios-práticos)
9. [Conclusão](#conclusão)

---

## Pré-requisitos

- **Docker** instalado (versão compatível com _docker-compose_ ou _docker compose_);
- Ambiente configurado para execução dos comandos Docker no terminal/shell.
- Versão do NodeJS > 18
- Não está usando a porta 8080 para outro serviço
---

## Estrutura do Projeto

A pasta raiz do projeto, denominada **esalq-mqtt-iot**, contém os seguintes principais itens:

- **docker-compose.yml**
  - Descreve os serviços necessários para executar:
    - Broker Mosquitto;
    - Sensor de Temperatura (pub_sensor_temperatura);
    - Sensor de Umidade (pub_sensor_umidade);
    - Dashboard (sub_dashboard).
- **pub_sensor_temperatura** (pasta)
  - Contém o arquivo `pub_sensor_temperatura.py`.
- **pub_sensor_umidade** (pasta)
  - Contém o arquivo `pub_sensor_umidade.py`.
- **sub_dashboard** (pasta)
  - Pode conter o arquivo principal do _dashboard_.

---

## Passo a Passo - Execução Inicial

1. **Entrar na pasta raiz do projeto**:

   ```bash
   cd esalq-mqtt-iot
   ```

2. **Subir os contêineres em segundo plano**:

   ```bash
   docker-compose up -d
   ```

   > Este comando irá baixar as imagens necessárias (caso ainda não estejam em cache) e criar os contêineres descritos no arquivo `docker-compose.yml`.

3. **Verificar se os contêineres subiram corretamente**:
   ```bash
   docker ps
   ```
   > Aqui você deve encontrar o broker Mosquitto, o sensor de temperatura, o sensor de umidade e o sub_dashboard em execução.

---

## Visualização dos Logs

Para conferir se tudo está funcionando corretamente, você pode acompanhar os logs de cada serviço:

1. **Dashboard (assinante)**:

   ```bash
   docker logs sub_dashboard -f
   ```

   - Use `CTRL + C` para parar a visualização dos logs.

2. **Sensor de Temperatura**:

   ```bash
   docker logs pub_sensor_temperatura -f
   ```

   - Acompanhe as mensagens que ele publica.

3. **Sensor de Umidade**:
   ```bash
   docker logs pub_sensor_umidade -f
   ```
   - Acompanhe as mensagens que ele publica.

Enquanto os sensores estiverem rodando, o _dashboard_ deve apresentar mensagens recebidas a cada nova publicação, validando o funcionamento do padrão **publish/subscribe** via MQTT.

---

## Encerrando os Recursos

Quando quiser parar e remover os contêineres, além de remover as imagens relacionadas, execute:

```bash
docker compose down --rmi all
```

- **down**: Para e remove os contêineres.
- **--rmi all**: Remove todas as imagens criadas pelo _docker-compose_.

---

## Ajustando os Tópicos de Publicação

Por padrão, tanto o sensor de temperatura quanto o de umidade estão publicando em `home/sensors`. Para separar as publicações em tópicos distintos, faça o seguinte:

1. **Abra o arquivo** `pub_sensor_temperatura.py` na pasta `pub_sensor_temperatura`:

   - Localize e comente a linha:
     ```python
     #TOPIC = "home/sensors"
     ```
   - Descomente a linha que define o tópico como `home/sensors/temperatura`:
     ```python
     TOPIC = "home/sensors/temperatura"
     ```

2. **Abra o arquivo** `pub_sensor_umidade.py` na pasta `pub_sensor_umidade`:
   - Localize e comente a linha:
     ```python
     #TOPIC = "home/sensors"
     ```
   - Descomente a linha que define o tópico como `home/sensors/umidade`:
     ```python
     TOPIC = "home/sensors/umidade"
     ```
**OBS: Salve todos os arquivos modificados antes das próximas etapas**

   - Com isso, cada sensor passa a publicar em um tópico próprio, facilitando a distinção das mensagens entre temperatura e umidade.

---

## Rodando o Dashboard Gráfico
### Execute novamente o docker compose:
   ```bash
   docker compose up -d
   ```

### Abra o browser e acesse: localhost:8080

O dashboard gráfico deve se conectar ao broker MQTT e exibir as mensagens recebidas de forma visual.

---
## 🧠 Desafios Práticos

### 🔐 Desafio 1: Comunicação Segura com TLS

Configure os serviços para utilizarem **TLS** com os certificados disponíveis na pasta `certs`. Os comandos necessários já estão comentados nos arquivos `pub_sensor_*.py` e `sub_dashboard`, e os certificados já estão gerados.

**Etapas:**
1. Descomente as linhas de código relacionadas ao TLS nos scripts.
2. Altere as portas nos scripts de `1883` para `8883`.
3. Atualize a configuração do `mosquitto.conf` para ativar o listener TLS.
4. Altere o `docker-compose.yml` para expor a porta `8883`.
5. Execute novamente:
   ```bash
   docker compose down
   docker compose up -d
   ```

### 📡 Desafio 2: Análise de Comunicação via Tcpdump

Capture e analise os pacotes MQTT utilizando `tcpdump` dentro do container do Mosquitto.

**Captura sem TLS (plaintext):**
```bash
docker exec -it mosquitto tcpdump -i eth0 -n -w /tmp/mqtt-capture-plain.pcap
# aguarde alguns segundos e depois:
docker cp mosquitto:/tmp/mqtt-capture-plain.pcap ./mqtt-capture-plain.pcap
```

**Captura com TLS:**
Repita o procedimento após configurar o ambiente com TLS:
```bash
docker exec -it mosquitto tcpdump -i eth0 -n -w /tmp/mqtt-capture-tls.pcap
docker cp mosquitto:/tmp/mqtt-capture-tls.pcap ./mqtt-capture-tls.pcap
```

**Dica:** Abra os arquivos `.pcap` no **Wireshark** e compare as comunicações com e sem criptografia.
## Conclusão

Este projeto demonstra de forma simples como utilizar **Docker** para orquestrar um ecossistema que implementa o protocolo **MQTT** com o broker **Mosquitto**. Você viu:

- Como clonar o repositório do GitHub.
- Como subir os contêineres com _docker-compose_.
- Como verificar logs para assegurar o correto funcionamento do _publish/subscribe_.
- Como encerrar os recursos e remover imagens.
- Como customizar os tópicos, separando as publicações de cada sensor.
- Como executar um _dashboard_ gráfico para visualizar os dados.

Sinta-se à vontade para expandir este exemplo, adicionando mais sensores ou assinantes (subscribers), ou até mesmo criando um _dashboard_ mais completo para visualização dos dados em tempo real.

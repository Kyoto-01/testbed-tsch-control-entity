# Testbed TSCH Control Entity

O módulo Control Entity é responsável por gerenciar as instâncias de ambientes de experimentação. Este módulo fornece funcionalidades para o consumo de mensagens de um
broker, alocação de motes, criação e destruição de ambientes de experimentação. O módulo
Control Entity é escrito em Python e utiliza a biblioteca Pika para se comunicar com um broker RabbitMQ.

## Setup

* Crie um arquivo ```config.ini``` em ```testbed/docker/config/``` e preencha-o de acordo com o modelo disponibilizado em ```testbed/docker/config/config.example.ini```.

* Execute o script de setup.
```
./setup.sh
```
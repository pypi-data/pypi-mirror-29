**************************************************************
Portal Modelo: Integração com sistemas do processo legislativo
**************************************************************

.. contents:: Conteúdo
   :depth: 2

Introdução
==========

Este pacote permite a integração do `Sistema de Apoio ao Processo
Legislativo`_ (SAPL) e outros sistemas no Portal Modelo do Programa
Interlegis.

Adicionalmente o pacote define tipos de conteúdo para representar os seguintes
objetos dentro da estrutura de uma Câmara Legislativa:

* Parlamentar
* Legistatura
* Sessão legislativa

O pacote também fornece uma view chamada ``@@pl-json`` disponibilizada na
raiz do portal que retorna essa informação em formato JSON.

Descrição dos tipos de conteúdo
===============================

Parlamentar
-----------

Um Parlamentar é um tipo de conteúdo baseado no Dexterity que contém os
seguintes campos:

* Nome
* Nome completo
* Aniversário
* Biografia
* Retrato
* Endereço
* CEP
* Telefone
* Filiação partidaria (sigla do partido e datas de filiação e desfiliação)

Legistatura
-----------

Uma Legislatura é um tipo de conteúdo baseado no Dexterity que contém os
seguintes campos:

* Número
* Descripção
* Data de inicio
* Data de término
* Membros (parlamentares eleitos)

Sessão legislativa
------------------

Uma Sessão legislativa é um tipo de conteúdo baseado no Dexterity que
representa um período dentro de uma legislatura. Dentro de uma sessão está
definida a conposição da mesa diretora desse período. Contém os seguintes
campos:

* Número
* Descrição
* Data de início
* Data de final
* Mesa diretora (membro e cargo)

Sincronização com o SAPL
========================

Caso de Uso
-----------

Este pacote implementa mecanismo de sincronização de uma via entre SAPL e Portal Modelo para os tipos de conteúdo Legislatura, Parlamentar e Sessão legislativa.

Considerando que em sua Câmara Legislativa exista uma versão atual do SAPL, a integração é feita em três passos:

* Configuração do SAPL para sincronização (veja o manual do SAPL)
* Configuração do Portal Modelo, via painel de controle, dos dados de acesso ao SAPL
* Acesso à url http://<portalmodelo>/@@sync-sapl autenticado como usuário administrador

Painel de Controle
------------------

Acesse o painel de controle do Portal Modelo e clique na opção **Configuração do SAPL Sync**.

São dois campos que podem ser configurados:

* Endpoint JSON do SAPL: URL do SAPL que gera o arquivo JSON
* Armazenamento local do SAPL: Caminho, no Portal Modelo, para armazenamento das informações de Legislatura, Parlamentar e Sessão Legislativa.

Formato Arquivo SAPL
---------------------

Utilizamos um arquivo JSON, disponibilizado pelo SAPL, para importação automática das Legislaturas, Parlamentares e Sessões Legislativas.

Abaixo temos um exemplo de arquivo JSON completo utilizado por este pacote::

    {
        "legislatures": [
            {
                "description": "",
                "end_date": "2016-12-31",
                "id": "legislature-01",
                "members": ["000000000001"],
                "sessions": [
                    {
                        "description": "First Legislative Session",
                        "end_date": "2014-12-31",
                        "id": "session-01",
                        "legislative_board": [
                            {
                                "member": "000000000001",
                                "position": "Board President"
                            }
                        ],
                        "start_date": "2013-01-01",
                        "title": "1st (2013-2014)"
                    },
                ],
                "start_date": "2013-01-01",
                "title": "1st Legislature"
            }
        ],
        "parliamentarians": [
            {
                "address": "Av. N2, Anexo E do Senado Federal, Brasilia/DF",
                "birthday": "1943-01-09",
                "description": "Bruxo do Cosme Velho, escritor.",
                "full_name": "Joaquim Maria Machado de Assis",
                "id": "000000000001",
                "image": "http://sapl.interlegis.leg.br/p/machado-assis/image.jpg",
                "party_affiliation": [
                    {
                        "date_affiliation": "1975-12-19",
                        "date_disaffiliation": "",
                        "party": "ABL"
                    }
                ],
                "postal_code": "70165-900",
                "telephone": "+55615553213",
                "title": "Machado de Assis"
            },
        ]
    }

Algumas considerações sobre o formato adotado:

* Datas devem ser exibidas no formato ISO 8601
* Utilizaremos os mesmos IDs dos objetos cadastrados no SAPL
* Imagens serão referenciadas a partir de sua URL completa. Este pacote realizará o download delas.

.. _`Sistema de Apoio ao Processo Legislativo`: https://colab.interlegis.leg.br/wiki/ProjetoSapl

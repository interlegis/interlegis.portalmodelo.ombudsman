***********************************
Portal Modelo: Sistema de Ouvidoria
***********************************

.. contents:: Conteúdo
   :depth: 2

Introdução
-----------

Este pacote integra um Sistema de informações ao cidadão no Portal Modelo do
Programa Interlegis.

O pacote define tipos de conteúdo para representar uma ouvidoria e as
solicitações, um workflow, um name chooser e uma view que retorna informação
em formato JSON.

Tipos de conteúdo
=================

Ouvidoria (OmbudsOffice)
------------------------

Uma Ouvidoria é um tipo de conteúdo baseado no Dexterity que contém os
seguintes campos:

* Nome
* Descrição
* Tipos de solicitações
* Áreas
* Administradores

Solicitação (Claim)
-------------------

Uma Solicitação é um tipo de conteúdo baseado no Dexterity que contém os
seguintes campos:

* Tipo de solicitação
* Área
* Assunto
* Detalhes
* Nome do solicitante
* Email do solicitante
* Gênero
* Idade
* Endereço
* CEP
* Cidade
* Estado

A solicitação tem atribuído um workflow especial chamado de
``claim_workflow``. O workflow é mudado pelos responsáveis por atender a
solicitação no processo de resolução da mesma.

As respostas a uma solicitação são armazenadas em anotações no objeto.

Qualquer usuário anônimo pode cadastrar uma solicitação, mas só usuários
autorizados podem mudar o estado da mesma e adicionar comentários.

Ao criar uma solicitação um número de protocolo é gerado de forma automática;
esse número de protocolo é formado pela data e um número adicional indicando a
hora de criação da solicitação.

Workflow
---------

O workflow das solicitações é simples e inclui 4 estados diferentes:

Pendente
    O estado inicial da solicitação; ela foi criada e está esperando o
    responsável avaliá-la.

Aceita
    A solicitação foi aceita e está em processo de iniciar o trâmite.

Rejeitada
    A solicitação não foi aceita.

Tramitando
    A solicitação está sendo tramitada.

Resolvida
    A solicitação teve uma resposta e, portanto, se considera resolvida.

Consulta de solicitações
------------------------

A view padrão da ouvidoria mostra uma caixa de buscas que permite buscar uma
solicitação usando seu número de protocolo.

Os usuários registrados podem ver também uma listagem das solicitações que
pode ser ordenado por título, estado, data de envio e data da última
modificação.

Notificações
------------

O sistema envia notificações cada vez que uma solicitação é criada ou
modificada. A lista de destinatarios inclui o responsável da área e o
solicitante.

O pacote depende do complemento `collective.watcherlist`_ sendo completamente
configurável.

.. _`collective.watcherlist`: https://pypi.python.org/pypi/collective.watcherlist

JSON API
--------

O pacote fornece uma view chamada ``@@ombudsman-json`` disponibilizada na raiz
do portal que retorna essa informação em formato JSON.

A informação mostrada inclui ouvidorias e solicitações num formato simples::

    {
        "claims": [
            {
                "address": "Rua Comendador Roberto Ugolini, 20",
                "age": "50",
                "area": "comunicacao-social",
                "city": "Mooca",
                "description": "Lorem ipsum dolor sit amet, consectetur adipiscing elit.",
                "email": "foo@bar.com",
                "genre": "m",
                "kind": "solicitacao-de-informacao",
                "name": "Zé Ninguém",
                "postal_code": "03125-010",
                "state": "SP",
                "title": "Lorem ipsum",
                "uri": "http://localhost:8080/Plone/ouvidoria/20140423103340"
            },
        ],
        "ombudsoffices": [
            {
                "areas": [
                    {
                        "area": "Recursos Humanos",
                        "email": "fulano@foo.gov.br",
                        "responsible": "Fulano"
                    }
                ],
                "claim_types": [
                    {
                        "claim_type": "Solicitação de informação"
                    }
                ],
                "description": "Lorem ipsum dolor sit amet, consectetur adipiscing elit.",
                "managers": [],
                "title": "Ouvidoria",
                "uri": "http://localhost:8080/Plone/ouvidoria"
            }
        ]
    }

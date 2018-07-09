Changelog
=========

1.3 (2018-07-09)
----------------

- Add statistic chart to ombudsman office and structured JSON to populate the chart.
  [IolaneAndrade]


1.2 (2017-12-05)
----------------

- Add recaptcha support
  [rafahela]


1.1 (unreleased)
----------------

- Fix email for non existing templates
  [jeanferri]

- Add option to hide the open claims listing
  [hersonrodrigues]

- Add templates for emails customization
  [hersonrodrigues]


1.0 (2015-09-25)
----------------

- Change the title in claim view
  [jeanferri]

- Improve review state stuff on response select box
  [jeanferri]

- Remove ':' from translations
  [jeanferri]

- Link the name of author for responses and attachments
  [jeanferri]

- Sort claims table for modification date reversed
  [jeanferri]

- Fix translations
  [jeanferri]

- Add permission to view claim personal info, with tests
  [ramiroluz]

- Update translations
  [jeanferri]

- Improve claim view
  [jeanferri]

- Add pagination to claims table
  [jeanferri]

- Fix protocol search for anonymous users in IDG themes
  [jeanferri]


1.0rc2 (2015-08-26)
-------------------

- Fix test to add a new ombudsman office
  [jeanferri]


1.0rc1 (2015-06-17)
-------------------

- Normalize area title so the Choice value can be used to find respective email address
  [ramiroluz]

- Fix test test_setup.py
  [marciomazza]

- Fix Add Claim button for anonymous user
  [jeanferri]


1.0b3 (2014-08-25)
------------------

- Suporte a adição de arquivos em Claims (refs. https://colab.interlegis.leg.br/ticket/2949).
  [ericof]

- Usamos o Portal Transforms para converter o texto de uma resposta para x-web-intelligent (refs. https://colab.interlegis.leg.br/ticket/2975).
  [ericof]


1.0b2 (2014-07-02)
------------------

- As informações pessoais não devem ser exibida para usuários anônimos,
  somente para os usuários administradores da ouvidoria
  (refs. https://colab.interlegis.leg.br/ticket/2946).
  [hvelarde]

- Exibe a tabela Solicitações abertas também para usuários anônimos, para que
  todos saibam quais os pedidos já foram feitos e quais as suas respostas
  (refs. https://colab.interlegis.leg.br/ticket/2946).
  [hvelarde]

- Adiciona o `Linkify`_, um plugin do jQuery para criar links automaticamente se for dada uma resposta com uma URL (refs. https://colab.interlegis.leg.br/ticket/2946).
  [hvelarde]

- O preenchimento dos campos Endereço, CEP, Cidade e Estado e agora opcional.
  Os campos Gênero e Idade foram removidos do formulário (refs. https://colab.interlegis.leg.br/ticket/2946).
  [hvelarde]


1.0b1 (2014-05-16)
------------------

- Informações pessoais dos usuários não devem ser disponibilizadas para
  usuários anónimos nas solicitações, nem acessando a API.


1.0a1 (2014-04-27)
------------------

- Initial release.

.. _`Linkify`: https://github.com/SoapBox/jQuery-linkify

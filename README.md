# Crescimento dos Veículos Elétricos no Brasil

Plataforma de Engenharia de Dados para analisar o crescimento dos veículos elétricos no Brasil utilizando dados públicos da SENATRAN.

## Objetivo

Este projeto tem como objetivo construir uma plataforma de dados utilizando Databricks e arquitetura Medallion para analisar a evolução da frota de veículos elétricos e híbridos no Brasil.

Além da análise dos dados, o projeto foi desenvolvido com foco no aprendizado prático de Engenharia de Dados e na aplicação de conceitos utilizados em ambientes reais.

## Fonte dos dados

Os dados utilizados serão provenientes da Secretaria Nacional de Trânsito (SENATRAN), utilizando bases públicas relacionadas à frota de veículos brasileira.

## Arquitetura

O projeto utilizará arquitetura Medallion:

```text
SENATRAN
    ↓
Ingestão
    ↓
Bronze
    ↓
Silver
    ↓
Gold
    ↓
Dashboard
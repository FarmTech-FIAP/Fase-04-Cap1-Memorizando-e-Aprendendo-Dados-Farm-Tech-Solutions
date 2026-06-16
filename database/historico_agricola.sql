-- Script de Criação da Tabela para o Projeto FarmTech Solutions
-- Banco de Dados: Oracle SQL (Docker)

CREATE TABLE HISTORICO_AGRICOLA (
    umidade_solo             NUMBER(10, 2),
    ph_solo                  NUMBER(10, 2),
    nivel_n                  NUMBER(1), -- Representa o INTEGER (0 ou 1) para Nitrogênio
    nivel_p                  NUMBER(1), -- Representa o INTEGER (0 ou 1) para Fósforo
    nivel_k                  NUMBER(1), -- Representa o INTEGER (0 ou 1) para Potássio
    volume_irrigacao_litros  NUMBER(10, 2),
    produtividade_kg         NUMBER(10, 2)
);

-- Comentário opcional para checagem rápida após a ingestão:
-- SELECT * FROM HISTORICO_AGRICOLA;
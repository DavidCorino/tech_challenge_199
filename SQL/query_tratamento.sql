 SELECT ano::text ||
        CASE
            WHEN v1013 = 9 THEN '09'::text
            ELSE v1013::text
        END AS ano_mes,
    ano,
    v1013 AS mes,
    uf_nome,
    sigla,
    regiao,
    a002 AS idade,
        CASE
            WHEN a003 = 1 THEN 'Homem'::text
            WHEN a003 = 2 THEN 'Mulher'::text
            ELSE NULL::text
        END AS sexo,
        CASE
            WHEN a004 = 1 THEN 'Branca'::text
            WHEN a004 = 2 THEN 'Preta'::text
            WHEN a004 = 3 THEN 'Amarela'::text
            WHEN a004 = 4 THEN 'Parda'::text
            WHEN a004 = 5 THEN 'Indígena'::text
            WHEN a004 = 9 THEN 'Ignorado'::text
            ELSE NULL::text
        END AS cor_raca,
        CASE a005
            WHEN '1'::bigint THEN 'Sem instrução'::text
            WHEN '2'::bigint THEN 'Fundamental incompleto'::text
            WHEN '3'::bigint THEN 'Fundamental completa'::text
            WHEN '4'::bigint THEN 'Médio incompleto'::text
            WHEN '5'::bigint THEN 'Médio completo'::text
            WHEN '6'::bigint THEN 'Superior incompleto'::text
            WHEN '7'::bigint THEN 'Superior completo'::text
            WHEN '8'::bigint THEN 'Pós-graduação, mestrado ou doutorado'::text
            ELSE NULL::text
        END AS escolaridade,
        CASE b0011
            WHEN 1 THEN 'Sim'::text
            WHEN 2 THEN 'Não'::text
            WHEN 3 THEN 'Não sabe'::text
            WHEN 9 THEN 'Ignorado'::text
            ELSE NULL::text
        END AS febre,
        CASE b0012
            WHEN 1 THEN 'Sim'::text
            WHEN 2 THEN 'Não'::text
            WHEN 3 THEN 'Não sabe'::text
            WHEN 9 THEN 'Ignorado'::text
            ELSE NULL::text
        END AS tosse,
        CASE b0014
            WHEN 1 THEN 'Sim'::text
            WHEN 2 THEN 'Não'::text
            WHEN 3 THEN 'Não sabe'::text
            WHEN 9 THEN 'Ignorado'::text
            ELSE NULL::text
        END AS dificuldade_respirar,
        CASE b0019
            WHEN 1 THEN 'Sim'::text
            WHEN 2 THEN 'Não'::text
            WHEN 3 THEN 'Não sabe'::text
            WHEN 9 THEN 'Ignorado'::text
            ELSE NULL::text
        END AS fadiga,
        CASE b00111
            WHEN 1 THEN 'Sim'::text
            WHEN 2 THEN 'Não'::text
            WHEN 3 THEN 'Não sabe'::text
            WHEN 9 THEN 'Ignorado'::text
            ELSE NULL::text
        END AS teve_perda_olfato_paladar,
        CASE c001
            WHEN 1 THEN 'Sim'::text
            WHEN 2 THEN 'Não'::text
            ELSE 'Não aplicável'::text
        END AS trabalhou_semana_passada,
    c001,
        CASE c004
            WHEN 1 THEN 'Sim'::text
            WHEN 2 THEN 'Não'::text
            WHEN 3 THEN 'O trabalho já não era remunerado'::text
            ELSE 'Não aplicável'::text
        END AS continuou_remunerado,
        CASE c007b
            WHEN 1 THEN 'Sim, tem carteira de trabalho assinada'::text
            WHEN 2 THEN 'Sim, é servidor público estatutário'::text
            WHEN 3 THEN 'Não'::text
            ELSE 'Não aplicável'::text
        END AS tipo_vinculo_trabalhista,
        CASE c007c
            WHEN '1'::double precision THEN 'Empregado doméstico, diarista, cozinheiro (em domicílios particulares);'::text
            WHEN '2'::double precision THEN 'Faxineiro, auxiliar de limpeza etc. (em empresa pública ou privada).'::text
            WHEN '3'::double precision THEN 'Auxiliar de escritório, escriturário'::text
            WHEN '4'::double precision THEN 'Secretária, recepcionista'::text
            WHEN '5'::double precision THEN 'Operador de Telemarketing'::text
            WHEN '6'::double precision THEN 'Comerciante (dono do bar, da loja etc.)'::text
            WHEN '7'::double precision THEN 'Balconista, vendedor de loja'::text
            WHEN '8'::double precision THEN 'Vendedor a domicílio, representante de vendas, vendedor de catálogo (Avon, Natura etc.)'::text
            WHEN '9'::double precision THEN 'Vendedor ambulante (feirante, camelô, comerciante de rua, quiosque)'::text
            WHEN '10'::double precision THEN 'Cozinheiro e garçom (de restaurantes, empresas)'::text
            WHEN '11'::double precision THEN 'Padeiro, açougueiro e doceiro'::text
            WHEN '12'::double precision THEN 'Agricultor, criador de animais, pescador, silvicultor e jardineiro'::text
            WHEN '13'::double precision THEN 'Auxiliar da agropecuária (colhedor de frutas, boia fria, etc.)'::text
            WHEN '14'::double precision THEN 'Motorista (de aplicativo, de taxi, de van, de mototaxi, de ônibus)'::text
            WHEN '15'::double precision THEN 'Motorista de caminhão (caminhoneiro)'::text
            WHEN '16'::double precision THEN 'Motoboy'::text
            WHEN '17'::double precision THEN 'Entregador de mercadorias (de restaurante, de farmácia, de loja, Uber Eats, iFood, Rappy etc.)'::text
            WHEN '18'::double precision THEN 'Pedreiro, servente de pedreiro, pintor, eletricista, marceneiro'::text
            WHEN '19'::double precision THEN 'Mecânico de veículos, máquinas industriais etc.'::text
            WHEN '20'::double precision THEN 'Artesão, costureiro e sapateiro'::text
            WHEN '21'::double precision THEN 'Cabeleireiro, manicure e afins'::text
            WHEN '22'::double precision THEN 'Operador de máquinas, montador na indústria'::text
            WHEN '23'::double precision THEN 'Auxiliar de produção, de carga e descarga'::text
            WHEN '24'::double precision THEN 'Professor da educação infantil, de ensino fundamental, médio ou superior.'::text
            WHEN '25'::double precision THEN 'Pedagogo, professor de idiomas, música, arte e reforço escolar'::text
            WHEN '26'::double precision THEN 'Médico, enfermeiro, profissionais de saúde de nível superior'::text
            WHEN '27'::double precision THEN 'Técnico, profissional da saúde de nível médio'::text
            WHEN '28'::double precision THEN 'Cuidador de crianças, doentes ou idosos'::text
            WHEN '29'::double precision THEN 'Segurança, vigilante, outro trabalhador dos serviços de proteção'::text
            WHEN '30'::double precision THEN 'Policial civil'::text
            WHEN '31'::double precision THEN 'Porteiro, zelador'::text
            WHEN '32'::double precision THEN 'Artista, religioso (padre, pastor etc.)'::text
            WHEN '33'::double precision THEN 'Diretor, gerente, cargo político ou comissionado'::text
            WHEN '34'::double precision THEN 'Outra profissão de nível superior (advogado, engenheiro, contador, jornalista etc.)'::text
            WHEN '35'::double precision THEN 'Outro técnico ou profissional de nível médio'::text
            WHEN '36'::double precision THEN 'Outros'::text
            ELSE 'não aplicável'::text
        END AS ocupacao,
        CASE c007d
            WHEN '1'::double precision THEN 'Agricultura, pecuária, produção florestal e pesca'::text
            WHEN '2'::double precision THEN 'Extração de petróleo, carvão mineral, minerais metálicos, pedra, areia, sal etc.'::text
            WHEN '3'::double precision THEN 'Indústria da transformação (inclusive confecção e fabricação caseira)'::text
            WHEN '4'::double precision THEN 'Fornecimento de eletricidade e gás, água, esgoto e coleta de lixo'::text
            WHEN '5'::double precision THEN 'Construção'::text
            WHEN '6'::double precision THEN 'Comércio no atacado e varejo;'::text
            WHEN '7'::double precision THEN 'Reparação de veículos automotores e motocicletas'::text
            WHEN '8'::double precision THEN 'Transporte de passageiros'::text
            WHEN '9'::double precision THEN 'Transporte de mercadorias'::text
            WHEN '10'::double precision THEN 'Armazenamento, correios e serviços de entregas'::text
            WHEN '11'::double precision THEN 'Hospedagem (hotéis, pousadas etc.)'::text
            WHEN '12'::double precision THEN 'Serviço de alimentação (bares, restaurantes, ambulantes de alimentação)'::text
            WHEN '13'::double precision THEN 'Informação e comunicação (jornais, rádio e televisão, telecomunicações e informática)'::text
            WHEN '14'::double precision THEN 'Bancos, atividades financeiras e de seguros'::text
            WHEN '15'::double precision THEN 'Atividades imobiliárias'::text
            WHEN '16'::double precision THEN 'Escritórios de advocacia, engenharia, publicidade e veterinária (Atividades profissionais, científicas e técnicas)'::text
            WHEN '17'::double precision THEN 'Atividades de locação de mão de obra, segurança, limpeza, paisagismo e teleatendimento'::text
            WHEN '18'::double precision THEN 'Administração pública (governo federal, estadual e municipal)'::text
            WHEN '19'::double precision THEN 'Educação'::text
            WHEN '20'::double precision THEN 'Saúde humana e assistência social'::text
            WHEN '21'::double precision THEN 'Organizações religiosas, sindicatos e associações'::text
            WHEN '22'::double precision THEN 'Atividade artísticas, esportivas e de recreação'::text
            WHEN '23'::double precision THEN 'Cabeleireiros, tratamento de beleza e serviços pessoais'::text
            WHEN '24'::double precision THEN 'Serviço doméstico remunerado (será imputado da posição na ocupação)'::text
            WHEN '25'::double precision THEN 'Outro'::text
            ELSE 'Não aplicável'::text
        END AS atividade_principal_empresa,
        CASE c0101
            WHEN 1 THEN 'Em dinheiro'::text
            ELSE 'Não aplicável'::text
        END AS recebia_em_dinheiro,
        CASE c01011
            WHEN '0'::double precision THEN '0 - 100'::text
            WHEN '1'::double precision THEN '101 - 300'::text
            WHEN '2'::double precision THEN '301 - 600'::text
            WHEN '3'::double precision THEN '601 - 800'::text
            WHEN '4'::double precision THEN '801 - 1.600'::text
            WHEN '5'::double precision THEN '1.601 - 3.000'::text
            WHEN '6'::double precision THEN '3.001 - 10.000'::text
            WHEN '7'::double precision THEN '10.001 - 50.000'::text
            WHEN '8'::double precision THEN '50.001 - 100.000'::text
            WHEN '9'::double precision THEN 'Mais de 100.000'::text
            ELSE 'Não aplicável'::text
        END AS faixa_rendimento_dinheiro,
        CASE c013
            WHEN 1 THEN 'Sim'::text
            WHEN 2 THEN 'Não'::text
            ELSE 'Não aplicável'::text
        END AS home_office,
        CASE d0031
            WHEN 1 THEN 'Sim'::text
            WHEN 2 THEN 'Não'::text
            ELSE NULL::text
        END AS rendimento_bolsa_familia,
        CASE
            WHEN d0033 IS NULL THEN 'Não aplicável'::text
            ELSE d0033::text
        END AS valor_bolsa_familia,
        CASE d0061
            WHEN 1 THEN 'Sim'::text
            WHEN 2 THEN 'Não'::text
            ELSE NULL::text
        END AS recebe_seguro_desemprego,
        CASE
            WHEN d0063 IS NULL THEN 'Não aplicável'::text
            ELSE d0063::text
        END AS valor_seguro_desemprego,
        CASE e001
            WHEN 1 THEN 'Sim, e pelo menos um morador conseguiu'::text
            WHEN 2 THEN 'Sim, mas nenhum morador conseguiu'::text
            WHEN 3 THEN 'Não solicitou'::text
            ELSE NULL::text
        END AS solicitou_emprestimo_pandemia
   FROM questionario_pnad_covid


SELECT DISTINCT d.prontuario,
    d.dt_nascimento,
    atd.dthr_inicio AS dataInternacao,
    (res.valor::NUMERIC(20,2)/100) resultado
 
FROM agh.agh_atendimentos atd
 
JOIN agh.ael_solicitacao_exames soe ON atd.seq = soe.atd_seq
 
JOIN agh.ael_item_solicitacao_exames ise ON soe.seq = ise.soe_seq  
 
JOIN agh.ael_resultados_exames res ON ise.soe_seq = res.ise_soe_seq 
    and ise.seqp = res.ise_seqp
 
JOIN agh.ain_internacoes int ON atd.int_seq = int.seq
 
JOIN agh.aip_pacientes d ON atd.pac_codigo = d.codigo
 
WHERE 
    (
    ise.ufe_ema_exa_sigla = 'CRE'
    AND  to_char(soe.criado_em,'yyyy-MM-dd') BETWEEN '2018-01-01' AND '2023-05-30' 
    )
    AND atd.origem = 'I'
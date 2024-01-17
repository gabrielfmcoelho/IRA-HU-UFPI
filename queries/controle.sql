SELECT pa.prontuario,
    inter.dthr_internacao, 
    gc.descricao AS grupo_controle,
    ic.descricao AS tipo_controle,
    hc.data_hora, 
    cp.medicao AS medida,
    tam.descricao as alta

FROM 
    agh.ain_internacoes inter

JOIN agh.aip_pacientes pa ON pa.codigo = inter.pac_codigo

JOIN agh.ain_tipos_alta_medica tam ON tam.codigo = inter.tam_codigo

JOIN agh.ecp_horario_controles hc ON hc.pac_codigo = pa.codigo

JOIN agh.ecp_controle_pacientes cp ON cp.hct_seq = hc.seq

JOIN agh.ecp_item_controles ic ON ic.seq = cp.ice_seq

JOIN agh.ecp_grupo_controles gc ON gc.seq = ic.gco_seq

JOIN agh.mpm_unidade_medida_medicas umm ON umm.seq = cp.umm_seq

WHERE 
    inter.esp_seq = 200 
    --or inter.esp_seq=17 )--cardiologia
    --and gc.descricao = 'Sinais Vitais' AND 
    AND gc.seq IN(1,2,3,4,5,11)
    AND inter.dthr_internacao between '2018-01-01' AND '2023-05-30'
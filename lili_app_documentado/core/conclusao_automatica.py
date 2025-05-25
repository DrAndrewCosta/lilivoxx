# core/conclusao_automatica.py

def conclusao_padrao_por_exame(tipo_exame):
    conclusoes = {
        "Abdome": "Exame dentro dos padrões da normalidade.",
        "Rins": "Exame dentro dos limites da normalidade.",
        "Próstata": "Volume prostático estimado em ___ g. Demais achados dentro dos padrões da normalidade.",
        "Mama": "Exame sem alterações ecográficas significativas. Seguimento de rotina conforme diretrizes.",
        "Parede abdominal": "Sem evidência de hérnias ou massas. Exame dentro da normalidade.",
        "Cervical": "Sem alterações nos linfonodos ou glândulas. Exame normal.",
        "Joelho": "Sem sinais de tendinopatia ou alterações estruturais significativas.",
        "Ombro": "Sem sinais de bursite, ruptura tendínea ou calcificações.",
        "Tireoide": "Parênquima homogêneo, sem nódulos. Exame normal.",
        "Transvaginal": "Útero e ovários com morfologia preservada. Exame normal."
    }
    return conclusoes.get(tipo_exame, None)

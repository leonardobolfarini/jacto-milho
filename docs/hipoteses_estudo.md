# 🌿 FarmLab - Hipóteses e Comprovações Práticas

**Objetivo Central:** Fornecer à gestão matrizes justificáveis do porquê a infestação de pragas (especialmente *Spodoptera frugiperda* e *Cigarrinha-do-milho*) não quebrou o ciclo apesar das pulverizações pesadas indicadas pelo mapa de telemetria da máquina.

Abaixo, refinamos as **8 hipóteses principais** cruzando telemetria geoespacial, dados de IoT e geometria da lavoura. Mais importante, listamos o protocolo de **COMO PROVAR** agronomicamente caso a diretoria demande evidências físicas dessa análise.

---

### 1. Falhas Operacionais: Efeito Bordadura e Cabeceira
**A Análise:** O mapa geoespacial mostrou ausência de rastros finos de pulverização e baixa cobertura nas curvas e cantos mais extremos da malha leste/sul. As armadilhas explodiram nesses perímetros.
**A Prova Física:** Para provar que não houve pulverização na borda, a equipe deve inspecionar fisicamente as **5 primeiras linhas de plantio junto à cerca**. Nessas linhas não cruzadas pelo trator, deve-se aplicar o papel hidrossensível e observar a injúria foliar. Se a nota de dano foliar na borda for grau 4 e no centro (onde tem rastro azul do mapa) for grau 1, comprova-se ineficácia por desleixo nas margens do talhão.

### 2. O Ponto Cego Biológico: Lavoura Convencional Excluída
**A Análise:** Foi detectado via mapa que **0 (nenhuma) armadilha** atende os polígonos vermelhos da lavoura Convencional, enquanto 100% dos sensores MIIP operam dentro do polígono 4.0. Não há praga excludente; a praga ataca na base vermelha silenciosamente, e migra explodindo na base verde, nos dizendo que "a saúde da verde está ruim" quando ela é apenas o anteparo.
**A Prova Prática:** Realocar ou instalar imediatamente 2 armadilhas analógicas de feromônio no centro magnético dos talhões convencionais que não têm cobertura. Se na contagem de D+7 e D+14 houver uma explosão superando a 4.0, escancara-se que os polígonos adjacentes estão servindo cegamente de chocadeiras em massa pra fazenda toda.

### 3. Operação Fantasma (Desperdício GPS fora do perímetro)
**A Análise:** Das 81.678 linhas registradas como "Operação" ligada, absurdos 64% caíram *fora da área dos talhões*. A máquina aplicou nas estradas, áreas públicas, ou houve pane de registro na ECU (Computador de Bordo).
**A Prova Auditável:** Para comprovar erro operacional (e desperdício imenso de R$), cruzar o relatório de "Vazão Total" de calda gasta com os Hectares Plantados oficiais. Se o tratorista derramou química no asfalto/carreador esquecendo de fechar a seção, a matemática do Volume Lg/ha vai acusar uma conta insustentável. Além de checar o `LAYER_MAP_SPEED` e verificar as velocidades nesses setores alheios.

### 4. Zonas Inadvertidas de Subdosagem (Queda de Pressão no Relevo)
**A Análise:** Algumas áreas em plena cruzada do trator pelo centro da fazenda ainda figuram armadilhas ativas e sem contenção. Suspeita-se de baixa pressão barométrica impedindo que as gotas atinjam o colmo basal (parte interna e escuda da folha onde a lagarta reside).
**A Prova Agronômica:** Fixar papéis hidrossensíveis sob a sombra das palhas inferiores exatamente nas mesmas latitudes do mapa onde a armadilha está em nível "Crítico", para cruzar e verificar a micronização do escoamento. Se não houver pintas azuis da gota atingindo as costas da folha abaixo de 40cm, é comprovada deficiência de alcance em copa úmida por flutuação de pressão.

### 5. Assincronia Tática (O "Timing" de Aplicação vs Ciclo da Praga)
**A Análise:** Visualizado em dados, a praga eclodiu na armadilha dias ou semanas *antes* da manobra densa de pulverização. O tempo cronológico errou.
**A Prova Entomológica:** Encurralar insetos vivos na região tratada. Se a biometria/estágio da lagarta coletada ou mariposa demonstrar ser da variante adulta, com alta prevalência de Posturas Recentes ou Primeiro Ínstar (Neonato), significa que o inseticida dizimou no último "gap" os hospedeiros maduros tardiamente; não inibindo a fecundação prematura que sobrevive imune na palhada esperando a próxima rodada de nascimento.

### 6. Velocidade Linear Excessiva (Escoamento / Lavagem Aerodinâmica)
**A Análise:** Tratores em piloto com linhas perfeitas no meio da área foram os maiores responsáveis pela não diminuição de pragas devido à facilidade de acelerar perante a reta longa.
**A Prova Via Telemetria/Física:** Bater o registro do ID do Talhão com o log de velocidade do sistema (`LAYER_MAP_SPEED`). Caso a ECU do pulverizador acuse >25km/h nas linhas centrais extensas e velocidade padrão inferior na meia-encosta das curvas, cruza-se a evidência de que a alta aerodinâmica causou "washout" das gotas não aderindo ao produto estomático, anulando o choque ali.

### 7. Aplicação Homogênea 'Cega' (Desperdício Espectro-Largo)
**A Análise:** Catação excessiva de veneno base forte em polígonos não críticos erradica até a fauna amiga em prol de uma cega meta diária da frota local.
**A Prova Analítica:** Fazer o inventário zoológico num metro quadrado a oeste onde a armadilha aponta estabilidade versus a nordeste. Constatando completa ausência de predadores benignos (tesourinhas, percevejo-predador e parasitoides locais), teremos consolidado que a pulverização homogênea desbalanceou e isolou o sistema, forjando ilhas de estresse biológico por conta de aplicações injustificáveis de amplo espectro na fazenda inteira pela frota, que induz seleção massiva a produtos reativos nas cigarrinhas sobreviventes.

### 8. Barreira Natural Extrema (A Interlocução de Ponte-Verde Externa)
**A Análise:** Na fronteira sul-leste, o limite tratorável cessa. É ali o abrigo massivo onde o rastreador acaba perante matos não rurais paralelos.
**A Prova Geográfica / Preventiva:** Disparar iscas e armadilhas limiares de *Ponte Verde* atreladas diretamente nas cercas. Caso a curva seja inversamente proporcional, revelando saturação nas iscas adjacentes antes do impacto dentro da roça, prova categoricamente migração exógena constante da propriedade vizinha ou brejo escuro. Confirmando que a estratégia requer bloqueio biológico por Trichogramma ou contenção externa antes que transbordem pros hectares rastreados pela jacto.

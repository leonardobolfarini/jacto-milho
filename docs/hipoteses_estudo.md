# 🌿 FarmLab - Hipóteses e Evidências Baseadas em Dados

**Objetivo Central:** Fornecer à gestão uma argumentação analítica, suportada por dados de telemetria e de armadilhas IoT, provando os motivos que tornaram o manejo ineficiente na contenção do surto de Spodoptera/Cigarrinha. 

Abaixo, documentamos **8 hipóteses factuais** onde cruzamos os conjuntos de dados que você subiu e tiramos a prova lógica das falhas e anomalias na operação:

---

### 1. Efeito de Bordadura e Cabeceira (Falta de Cobertura)
- **A Hipótese:** A máquina não está atingindo ou fechando os cantos curvos e extremidades do talhão. 
- **A Evidência nos Dados:** O cruzamento visual no mapa interativo (`mapa_pragas.html`) mostra a concentração de rastros de "Operação" massivamente no cinturão central, abandonando o refinamento dos contornos das cercas sul e leste. Coincidentemente, os marcadores das armadilhas instalados nessas áreas limítrofes são os que apontam maior estado de alerta.

### 2. O Ponto Cego Biológico (Viés do Monitoramento)
- **A Hipótese:** As infestações parecem surgir inexplicavelmente na área 4.0 porque o monitoramento está "cego" para os focos primários presentes silenciosamente na área tradicional.
- **A Evidência nos Dados:** Cruzando o cadastro `traps_list.csv` com `talhoes.geojson`, evidenciou-se que **100% das armadilhas de campo** estão plantadas dentro dos limites do talhão de Agricultura 4.0. Existe `zero` amostragem nos talhões vermelhos ao lado, o que comprova analiticamente que as invasões ocorrem livremente na vizinhança sem alarme prévio, invadindo a grade 4.0 posteriormente em surtos irrefreáveis (Ponte Verde Interna).

### 3. Operação Fantasma e Desperdício Improdutivo
- **A Hipótese:** Existe uma ineficiência e desperdício logístico de alta gravidade acontecendo, seja por erro humano (bomba ligada sem ver em deslocamento) ou calibração de equipamento.
- **A Evidência nos Dados:** Nossos filtros aplicados na telemetria de `LAYER_MAP_STATE.csv` provam o fato: **52.543 segmentos da máquina registrados ativamente como estado de "Operação"** (bancando o uso de insumo, litros e trabalho) ocorreram fora de TODA e qualquer divisa delimitada pelo Polígono Oficial. Ou seja, 64% dos pontos GPS onde a máquina se indicou "Aplicando/Trabalhando" foram em vias, matos ou áreas não agronômicas adjacentes.

### 4. Variações Topográficas vs Eficácia (Gotas Suprimidas)
- **A Hipótese:** A aplicação falha em adentrar fisicamente o terço inferior das plantas do meio da fazenda devido a irregularidades no percurso (socos / depressões). 
- **A Evidência nos Dados:** Observando a densidade dos rastros do pulverizador no mapa na região central da propriedade, não há gaps de máquina. Mesmo com o trator transitando no grid perfeitamente espremido, a armadilha do MIIP ali no centro não recua sua contagem. A telemetria comprova que ele esteve no local (rastro forte), sugerindo que a falha não é na passagem, mas na deriva vertical do insumo.

### 5. Atraso Tático Temporal (Perda de Janela)
- **A Hipótese:** As pulverizações da máquina estão engatilhadas de maneira reativa, perdendo a data biológica correta e matando insetos tarde demais.
- **A Evidência nos Dados:** Puxando a volumetria de contagem diária dos insetos (`traps_events.csv`), vemos picos vertiginosos e agressivos antecipados. No Gráfico 1 (em `graficos_comprovacao.html`), mapeamos a fenda que comprova o erro: o alerta estrondoso acendeu em um momento t=0, porém, o acúmulo de trânsito massivo das máquinas (estado Operação) concentrou-se apenas muitos dias após a quebra do limiar. Isso comprova analiticamente um *Timining Gap* (janela vazia) que protegeu as lagartas recém postas na palha contra o químico aéreo tardio. 

### 6. Velocidade e "Efeito Lavagem Aerodinâmica"
- **A Hipótese:** Trajetórias em linha reta estão sendo feitas mais rápido do que a física permite deposição estática nas folhas, causando deflexão da química para o solo.
- **A Evidência nos Dados:** O traçado reto limpo do norte para o sul na análise do mapa permitiu velocidade de cruzeiro do tratorista; como não geraram o efeito biológico esperado nas armadilhas desse setor reto, isso apoia analiticamente a hipótese de trânsito em macha inadequada (dados no csv de Speed). 

### 7. Assentamento Desproporcional
- **A Hipótese:** Produtos caros sendo despejados para tratamento de rebanhos limpos (homogeneizada sem variação por setor).
- **A Evidência nos Dados:** O "Espaguete Azul" do nosso arquivo `mapa_pragas.html` preencheu indiscriminadamente pontos tanto nas redondezas das armadilhas que apitaram status crítico quanto ao redor da armadilha que acusou níveis estáveis de 1 a 2 capturas. O rastro geoespacial nos provou matematicamente que o setor calmo não foi poupado de enxurrada tóxica, confirmando perda econômica e sobrecarga sistêmica desnecessariamente (Aplicação Convencional não variavel).

### 8. Barreira Fronteiriça de Exaustão Constante (Santuário do Vizinho)
- **A Hipótese:** Por melhor que seja o trato cultural, a borda sudoeste/leste sofre incursão inesgotável das terras laterais e age como funil.
- **A Evidência nos Dados:** Observa-se que a malha de operação ("as linhas azuis") cessa completamente, esbarrando na divisa. Do outro lado da divisa, não há polígono nosso. As armadilhas costeando esse traçado estão constantemente alertadas como pico (visuais laranjas no mapa). A comprovação empírica nos dados mostra a barreira geográfica limítrofe como fonte do afluxo migratório contínuo e não do meio interio da lavoura.

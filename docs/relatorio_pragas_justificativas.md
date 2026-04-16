# Análise de Persistência de Pragas no Milho

Este documento sumariza os motivos biológicos e operacionais pelos quais as pragas cadastradas continuam sendo registradas em crescimento no monitoramento (MIIP) da lavoura, apesar das práticas corretas de controle. O foco aqui foi a **Lagarta Spodoptera** e a **Cigarrinha**.

## Motivos da Persistência das Pragas

1. **O "Esconderijo" Anatômico (Comportamental)**
   A *Lagarta Spodoptera* (Peso de dano 5 - Risco Máximo) possui um comportamento de ataque particular: ela se abriga fundo no cartucho do milho. Isso significa que mesmo com a diluição, a pressão ou o produto químico no momento ideal, o inseticida de contato raramente consegue atingir a lagarta nessa profundidade. Suas fezes, muitas vezes, servem como um "tampão", piorando a eficiência do controle. O resultado é a permanência do inseto e a progressão para danos severos, como o sintoma de "coração morto".

2. **Migração e Efeito "Ponte Verde"**
   Insetos com grande mobilidade geográfica, sobretudo a *Cigarrinha* (Dalbulus maidis - Peso de Dano 4) e *Percevejos*, movem-se trazidos pelo vento advindos de lavouras ou pastagens vizinhas. Se o controle dos lotes próximos for ineficaz ou a janela de colheitas for escalonada, há migração contínua ao seu talhão (a chamada "ponte verde"). Matar 100% da sua área hoje não impede 10.000 insetos de chegarem do vizinho amanhã.

3. **Danos Rápidos Indiretos (Viroses e Molicutes)**
   Muitas vezes o controle curativo não funciona para a Cigarrinha pois o dano primário que ela causa não é a sucção de seiva, mas sim a transmissão de **molicutes** (microrganismos que causam o letal Enfezamento). Apenas poucos minutos após aterrissar sobre várias plantas da sua lavoura, mesmo que esse inseto seja atingido por uma cobertura inseticida letal algumas horas depois, a praga já infectou a planta. A infecção já começou, e o metabolismo do milho sofrerá o impacto irreversível, reduzindo drasticamente o número/peso dos grãos.

4. **Resistência aos Ativos e Biotecnologia (Toxinas Bt)**
   O uso repetido das mesmas moléculas e contaminação em áreas onde produtores não cultivam adequadamente o *refúgio agrícola* acelera severamente a resistência do inseto. Aquela fração decimal da população (os menores 1 ou 2%) que possuem tolerância natural aos produtos conseguem prosperar na ausência de competição, gerando surtos ainda piores que parecem ser "invulneráveis" aos defensivos habituais.

## Como os Dados Podem Reforçar Essa Justificativa?
Para atestar esses cenários de persistência e auxiliar sua tomada de decisão com evidências quantitativas no código, fizemos as seguintes adaptações nas estruturas do `main.py`:

- **Fixação do Agrupamento Corretamente Cronológico:** Originalmente, o cálculo do Delta de pragas entre datas misturava dados de todos os IDs de armadilhas como se fossem a mesma medição, gerando ruído (`groupby("plotName")` sendo que os valores eram traços "-"). Agrupando por `trapId`, acompanhamos exatamente como cada ponto físico reage com o passar do tempo.
- **Novas Features Analíticas de Monitoramento:**
  - `dias_desde_ultima_leitura`: Identifica se o crescimento da população é culpa de espaços gigantes de tempo entre uma visita do técnico e outra (as armadilhas possuem vida útil em *feronômios* e *pisos adesivos*, normalmente 7 a 30 dias).
  - `taxa_crescimento_diario`: Proporção direta que dita: quão rápida aquela área explodiu seu número de insetos a cada 24 horas. Indicador vital de surto súbito migratório ("chegou do vizinho").
  - `crescimento_continuo`: Explicita a cronologia e a eficiência dos tratamentos. Demonstra quantas vezes seguidas aquela armadilha reportou elevação da infestação, provando a ineficácia real sobre gerações recorrentes da praga.

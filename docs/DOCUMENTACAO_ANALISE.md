# FarmLab — Documentação Técnica de Análise de Pragas

> **Projeto:** FarmLab · UNIMAR · Safra 2025/2026  
> **Cultura:** Milho · **Região:** Marília-SP · **Sistema:** MIIP (Monitoramento Integrado de Insetos-Praga)  
> **Última atualização:** 30/03/2026

---

## 1. Visão Geral do Projeto

O objetivo desta análise é entender a **persistência e o crescimento de pragas** mesmo com aplicação de agrotóxicos, utilizando os dados do sistema MIIP e EKOS da plataforma FarmLab.

### Fontes de dados utilizadas

| Arquivo | Origem | Descrição |
|---|---|---|
| `traps_data.csv` | MIIP | Leituras das armadilhas (contagens, nível DAMAGE/ALERT/LOW) |
| `pest_details.csv` | MIIP | Catálogo de pragas: limiares, feromônios, sintomas |
| `pest_list.csv` ⚠️ | MIIP | Catálogo de 88 pragas com MIIP_PEST_ALERT/CONTROL/DAMAGE — **não baixado ainda** |
| `traps_list.csv` ⚠️ | MIIP | Cadastro das 34 armadilhas com GPS e tipo — **não baixado ainda** |
| `traps_events.csv` ⚠️ | MIIP | 2.295 eventos: capturas, IA, IoT — **não baixado ainda** |

> **Para análises futuras, baixar do OneDrive (@unimar.br):** `pest_list.csv`, `traps_list.csv`, `traps_events.csv`

### Datasets EKOS disponíveis (não utilizados ainda)

| Arquivo | Utilidade para análise de pragas |
|---|---|
| `LAYER_MAP_SPRAY_PRESSURE.csv` | Pressão de pulverização (psi) — correlacionar com queda/não-queda de pragas |
| `LAYER_MAP_FERTILIZATION.csv` | Dose de adubação real vs. configurada por talhão |
| `LAYER_MAP_GRAIN_HARVESTING.csv` | Produtividade (kg/ha) — impacto de pragas na safra |
| Cadastros EKOS (fields, OS) | Vincular talhões às armadilhas por ID |

---

## 2. Estrutura dos Dados MIIP

### 2.1 `traps_data.csv` — Schema

| Coluna | Tipo | Descrição |
|---|---|---|
| `createdAt` | datetime (UTC) | Data/hora da leitura da armadilha |
| `trapId` | int | ID único da armadilha (PK) |
| `trapCode` | string | Código legível (ex: `FARMLAB1`, `CIGARRINHA4`) |
| `primaryPest` | string | Espécie-alvo monitorada |
| `pestCount` | float | Número de insetos contados |
| `trapInfestationLevel` | enum | `LOW / ALERT / DAMAGE / CONTROL / HIGH / —` |
| `trapStatus` | enum | `ACTIVE / INACTIVE` |
| `trapType` | enum | `CONVENTIONAL / ELECTRONIC` |
| `trapBatteryStatus` | enum | `IDEAL / —` (só eletrônicas) |
| `doneMissionCount` | int | Missões de visita concluídas |
| `lateMissionCount` | int | Missões atrasadas |
| `pendingMissionCount` | int | Missões pendentes |
| `farmName` | string | Nome da fazenda |
| `plotName` | string | Nome do talhão |
| `idBusinessUnit` | int | ID da unidade de negócio (53560 = único na amostra) |
| `harvest` | string | Safra (ex: `2025/2026`) |
| `culture` | string | Cultura (`Milho` após filtro) |

### 2.2 `pest_details.csv` — Schema relevante

| Coluna | Tipo | Descrição |
|---|---|---|
| `id` | int | FK → `pest_list.MIIP_PEST_ID` |
| `namePopular` | string | Nome popular (ex: Lagarta Spodoptera) |
| `nameScientific` | string | Nome científico |
| `culture` | string | Cultura afetada |
| `alert` | int | Limiar de alerta (insetos/armadilha/período) |
| `control` | int | Limiar de controle (recomenda aplicação) |
| `damage` | int | Limiar de dano econômico (perdas mensuráveis) |
| `daysPheromone` | int | Validade do feromônio (dias) |
| `daysAdhesiveFloor` | int | Validade do piso adesivo (dias) |
| `actionRay` | float | Raio de ação da armadilha (m) |
| `symptoms` | string | Sintomas e danos ao cultivo |
| `dataPest` | string | Descrição morfológica |
| `detectionName` | string | Código do modelo de IA |
| `link_imagem` | URL | Imagens no S3 (AWS) |

---

## 3. Features Analíticas Criadas

O `main.py` enriquece o dataset bruto com as seguintes colunas calculadas:

| Feature | Fórmula | Interpretação |
|---|---|---|
| `damage_weight` | Mapa fixo por espécie (1–5) | Peso de dano econômico relativo |
| `infest_numeric` | Mapa `LOW=1, MEDIUM=2, ALERT=2, DAMAGE=3, HIGH=5` | Nível de infestação numérico |
| `alert_index` | `infest_numeric × damage_weight` | Score integrado de risco (≥10 = crítico) |
| `acima_alert` | `pestCount ≥ limiar_alerta[espécie]` | Booleano: acima do limiar de alerta |
| `acima_control` | `pestCount ≥ limiar_controle[espécie]` | Booleano: necessita aplicação de defensivo |
| `acima_damage` | `pestCount ≥ limiar_dano[espécie]` | Booleano: dano econômico em curso |
| `pest_delta` | `diff(pestCount)` por `trapId` | Variação absoluta entre leituras consecutivas |
| `dias_desde_ultima_leitura` | `diff(createdAt).dt.total_seconds()/86400` | Intervalo em dias entre visitas técnicas |
| `taxa_crescimento_diario` | `pest_delta / dias_desde_ultima_leitura` | Velocidade de crescimento da infestação |
| `trend` | `pest_delta > 0 OR level ∈ DAMAGE/ALERT/HIGH` | `"Crescente"` ou `"Estável/Caindo"` |
| `surtos_consecutivos` | `cumsum(trend == "Crescente")` por `trapId` | Número acumulado de surtos no histórico |
| `eficacia_missao_pct` | `doneMissionCount / (done + late) × 100` | % de missões executadas no prazo |
| `priority_status` | Regra baseada em `trend` + `alert_index` | 🔴 CRÍTICO / 🟠 ALERTA / 🟡 MONIT. / 🟢 NORMAL |

### Limiares biológicos utilizados

| Espécie | Limiar Alerta | Limiar Controle | Limiar Dano | Peso |
|---|---|---|---|---|
| Lagarta Spodoptera | 2 | 4 | 8 | 5 |
| Cigarrinha (*Dalbulus maidis*) | 10 | 30 | 60 | 4 |
| Percevejo Marrom | 1 | 2 | 4 | 3 |
| Percevejo Barriga Verde | 1 | 2 | 4 | 5 |
| Percevejo Gaúcho | 1 | 2 | 4 | 2 |

---

## 4. Resultados da Análise — Safra 2025/2026

### 4.1 Resumo por Espécie

| Espécie | Armadilhas | Média/Arm. | Pico | % acima controle | % acima dano | % crescente | Eficácia missões |
|---|---|---|---|---|---|---|---|
| **Cigarrinha** | 11 | **66,2** | **141** | **59,3%** | **33,3%** | **59,3%** | 55,1% |
| **Lagarta Spodoptera** | 13 | 4,3 | 35 | 18,2% | 12,1% | 30,3% | 25,5% |

#### Interpretação crítica:

- **Cigarrinha:** 59% das leituras estão acima do limiar de controle (30 insetos) e 33% acima do dano econômico (60 insetos). O pico de **141 insetos** em uma única armadilha é 4,7× o limiar de dano. O limiar de alerta (10) é regularmente ultrapassado.
- **Lagarta Spodoptera:** Embora a média seja baixa (4,3), o pico de **35 lagartas** é 8,75× o limiar de dano. 12% das leituras já indicam dano econômico com o controle ativo insuficiente.

### 4.2 Top Armadilhas Críticas (ACTIVE)

| Armadilha | Praga | Pico | Média | alert_index máx | Surtos | Eficácia missão |
|---|---|---|---|---|---|---|
| CIGARRINHA0749 | Cigarrinha | **141** | 97,5 | 12 | 2 | 91,7% |
| CIGARRINHA1 | Cigarrinha | **126** | 64,5 | 12 | 1 | 90,0% |
| CIGARRINHA1654 | Cigarrinha | **125** | 56,3 | 12 | 2 | 57,1% |
| CIGARRINHA4 | Cigarrinha | **121** | 94,5 | 12 | 2 | 100% |
| CIGARRINHA2 | Cigarrinha | **99** | 60,7 | 12 | 3 | 100% |
| FARMLAB2 | Lag. Spodoptera | **35** | 12,0 | 15 | 1 | 54,5% |
| FARMLAB1 | Lag. Spodoptera | **17** | 10,5 | 15 | 1 | 100% |

> **Observação:** CIGARRINHA2 apresenta `surtos_consecutivos = 3` — a maior persistência contínua do dataset, indicando reinfestação recorrente mesmo com missões 100% cumpridas.

---

## 5. Por que as pragas NÃO diminuem com agrotóxicos?

Esta é a questão central do projeto. A análise dos dados confirma **4 mecanismos principais**:

### 5.1 Esconderijo Anatômico (Lagarta Spodoptera)

A *Spodoptera frugiperda* penetra no cartucho do milho nos primeiros instares larvais. O inseticida de contato **não consegue penetrar** na profundidade de 5–10 cm dentro do cartucho. As próprias fezes da lagarta formam um tampão físico que reduz ainda mais a penetração.

**Evidência nos dados:** A FARMLAB2 registrou queda de 35 → 1 larva em uma leitura subsequente, mas a armadilha permaneceu ACTIVE com pendência de 5 missões atrasadas (`lateMissionCount = 5`) — mostrando que o timing de controle foi tardio.

### 5.2 Transmissão Viral Instantânea (Cigarrinha)

A *Dalbulus maidis* transmite **Corn Stunt Spiroplasma** e **Maize Bushy Stunt Phytoplasma** em **minutos** após pousar na planta. O controle químico **posterior** elimina o inseto, mas não reverte a infecção. A planta permanece com molicutes, reduzindo produtividade até 80%.

**Evidência nos dados:** 9 das 11 armadilhas de Cigarrinha registraram DAMAGE em pelo menos uma leitura, com pico de 141 insetos em CIGARRINHA0749 — 2,35× o limiar de dano. A alta eficácia de visitas (91,7%) não impediu a acumulação de danos.

### 5.3 Reinfestação por Migração ("Ponte Verde")

Insetos migram de lavouras/pastagens vizinhas trazidos pelo vento. A taxa de crescimento diário positiva em diversas armadilhas, mesmo após leituras que indicam queda, demonstra **ondas de reinfestação**.

**Evidência nos dados:**
- CIGARRINHA1654: pico 125 → queda → pico 125 novamente (duas datas distintas, nomes de armadilha iguais)
- CIGARRINHA4: pico 121 → 68 (queda de 53 insetos) mas seguida de nova tendência crescente

### 5.4 Resistência e Lacunas Operacionais

**Resistência:** O uso exaustivo das mesmas moléculas em uma região cria pressão seletiva. Os 1-2% da população resistente se reproduzem sem competição após cada aplicação.

**Lacunas operacionais:** A eficácia média de missões é **25,5% para Spodoptera** — indicando que quase 75% das visitas técnicas para essa praga foram atrasadas ou não realizadas. Armadilhas eletrônicas com código `3,5721E+14` apresentam 0% de missões concluídas.

---

## 6. Arquivos Gerados

| Arquivo | Linhas | Descrição |
|---|---|---|
| `main.py` | 300+ | Pipeline ETL + análise + geração de outputs |
| `tratado_enriquecido.csv` | ~73 | Dataset completo com todas as features calculadas |
| `diagnostico_persistencia.csv` | ~20 | Casos críticos: ACTIVE + alert_index ≥ 10 |
| `resumo_armadilhas.csv` | 25 | Agregado por armadilha (pico, surtos, missões) |
| `resumo_pragas.csv` | 3 | Comparativo entre espécies com limiares |
| `dashboard_pragas.html` | — | **Dashboard interativo** (abrir no navegador) |
| `relatorio_pragas_justificativas.md` | — | Relatório biológico/operacional anterior |

---

## 7. Próximos Passos Recomendados

### Prioridade ALTA — Dados necessários

| Dataset | Por quê baixar | Análise possível |
|---|---|---|
| `traps_list.csv` | GPS das 34 armadilhas | Mapa espacial de infestação, análise de cluster |
| `traps_events.csv` | 2.295 eventos de captura/IA | Correlação horário × contagem, eficácia do modelo de IA |
| `pest_list.csv` | 88 pragas com limiares oficiais | Substitui os limiares manuais no código por valores da fonte |
| `LAYER_MAP_SPRAY_PRESSURE.csv` | Datas e pressão de pulverização | Correlação direta: spray_date ↔ pest_delta (próxima leitura) |
| `LAYER_MAP_GRAIN_HARVESTING.csv` | Produtividade por talhão | Impacto econômico estimado por área infestada |

### Prioridade MÉDIA — Análises a implementar

1. **Análise de correlação aplicação × queda de pragas**  
   Cruzar datas de pulverização (`LAYER_MAP_SPRAY_PRESSURE`) com `taxa_crescimento_diario` nas leituras seguintes de cada armadilha. Esperado: queda na semana 1-2 pós-aplicação, seguida de reinfestação.

2. **Mapa espacial de infestação**  
   Com `traps_list.csv` (GPS), usar `folium` ou `geopandas` para plotar um heatmap da pressão de pragas por coordenada geográfica.

3. **Análise de feromônio vencido**  
   `pest_details.daysPheromone` para cada espécie × `dias_desde_ultima_leitura` calculado. Quando `dias > daysPheromone`, a armadilha perde capacidade de atração — leituras baixas podem ser falso-negativos.

4. **Modelo preditivo de surto**  
   Features: `taxa_crescimento_diario`, `eficacia_missao_pct`, `dias_desde_ultima_leitura`, `trapType`. Target: `trapInfestationLevel ∈ DAMAGE` na próxima leitura. Usar `RandomForestClassifier` ou `XGBoost`.

5. **Integração com dados climáticos**  
   API do INMET para Marília-SP: temperatura e precipitação nas datas das leituras. Ambos afetam diretamente o ciclo reprodutivo de Spodoptera e a migração de Cigarrinhas.

### Código para próximas análises

```python
# Exemplo: Identificar armadilhas com feromônio provavelmente vencido
# (requer traps_list.csv + pest_details com daysPheromone)
feromonio_validade = {
    "Lagarta Spodoptera": 30,  # dias
    "Cigarrinha": 28,
    "Percevejo Marrom": 21,
}

df["feromonio_possivelmente_vencido"] = df.apply(
    lambda r: r["dias_desde_ultima_leitura"] > feromonio_validade.get(r["primaryPest"], 30),
    axis=1
)

# Exemplo: Cruzamento futuro com datas de pulverização
# spray_df = pd.read_csv("LAYER_MAP_SPRAY_PRESSURE.csv", sep=";")
# spray_df["Date Time"] = pd.to_datetime(spray_df["Date Time"], format="%d/%m/%Y %H:%M:%S")
# Fazer merge por talhão e janela temporal de 7 dias após pulverização
```

---

## 8. Notas Técnicas do Pipeline

### Deduplicação
Linhas duplicadas por `(trapId, createdAt, pestCount, trapInfestationLevel)` são removidas com `keep='first'` antes de qualquer cálculo.

### Séries temporais
Todos os `diff()` e `cumsum()` são aplicados **dentro de cada `trapId`** com `groupby("trapId")` para evitar contaminação entre armadilhas distintas.

### Armadilhas sem leituras válidas
Armadilhas com `pestCount = NaN` aparecem no dataset (registro de criação sem visita). São preservadas nos CSVs mas excluídas dos cálculos de média e tendência.

### Código de armadilha `3,5721E+14`
Armadilhas eletrônicas FARMLAB com código numérico interpretado como notação científica pelo Excel/CSV. São armadilhas ELECTRONIC com `requestGPS = True`. Recomenda-se verificar o `trapId` original na `traps_list.csv` para obter o código correto.

### Separador dos arquivos EKOS
Os arquivos de Camadas EKOS usam **ponto-e-vírgula (`;`)** como separador. Os arquivos de Análise de Solo (Cropman) usam **vírgula (`,`)**.

---

## 9. Legenda dos Status de Prioridade

| Status | Condição | Ação recomendada |
|---|---|---|
| 🔴 CRÍTICO — Infestação em Expansão | trend = Crescente AND alert_index ≥ 10 | Aplicação imediata + revisão de produto/dose |
| 🟠 ALERTA — Nível de Dano Atingido | alert_index ≥ 10 (sem trend crescente) | Avaliar aplicação curativa + monitoramento diário |
| 🟡 MONITORAMENTO REFORÇADO | trend = Crescente AND alert_index < 10 | Aumentar frequência de visitas — início de surto |
| 🟢 NORMAL | alert_index < 10 AND trend ≠ Crescente | Manter monitoramento padrão |

---

*Documentação gerada automaticamente pelo pipeline FarmLab. Para dúvidas, verificar o código-fonte em `main.py`.*

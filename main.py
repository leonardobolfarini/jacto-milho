import pandas as pd
import json
from datetime import datetime

PESOS_PRAGAS = {
    "Percevejo Barriga Verde": 5,
    "Lagarta Spodoptera":      5,
    "Cigarrinha":              4,
    "Percevejo Marrom":        3,
    "Percevejo Gaúcho":        2,
}

LIMIARES = {
    "Lagarta Spodoptera": {"alert": 2,   "control": 4,  "damage": 8},
    "Cigarrinha":         {"alert": 10,  "control": 30, "damage": 60},
    "Percevejo Marrom":   {"alert": 1,   "control": 2,  "damage": 4},
    "Percevejo Barriga Verde": {"alert": 1, "control": 2, "damage": 4},
    "Percevejo Gaúcho":   {"alert": 1,   "control": 2,  "damage": 4},
}

MAP_INFESTACAO = {"LOW": 1, "MEDIUM": 2, "ALERT": 2, "DAMAGE": 3, "HIGH": 5, "CONTROL": 1}

def carregar_dados():
    pest_details = pd.read_csv("./input/pest_details.csv", sep=";", on_bad_lines="skip")
    traps_data   = pd.read_csv("./input/traps_data.csv",   sep=";", on_bad_lines="skip")

    traps_data["createdAt"] = pd.to_datetime(traps_data["createdAt"], utc=True, errors="coerce")
    traps_data["pestCount"] = pd.to_numeric(traps_data["pestCount"], errors="coerce")

    traps_data = traps_data.drop_duplicates(
        subset=["trapId", "createdAt", "pestCount", "trapInfestationLevel"],
        keep="first"
    )

    pest_details = pest_details[pest_details["culture"] == "Milho"]
    traps_data   = traps_data[traps_data["culture"] == "Milho"]
    traps_data   = traps_data.sort_values(by=["trapId", "createdAt"]).reset_index(drop=True)

    return traps_data, pest_details

def calcular_prioridade(row):
    score = row["alert_index"]
    trend = row["trend"]
    if trend == "Crescente" and score >= 10:
        return "CRÍTICO"
    elif score >= 10:
        return "ALERTA"
    elif trend == "Crescente":
        return "MONITORAMENTO REFORÇADO"
    else:
        return "NORMAL"


def verificar_acima_limiar(row, limiar_tipo="control"):
    pest = row.get("primaryPest", "")
    count = row.get("pestCount", 0)
    if pd.isna(count) or pest not in LIMIARES:
        return False
    return count >= LIMIARES[pest].get(limiar_tipo, 9999)


def enriquecer(traps_data: pd.DataFrame) -> pd.DataFrame:
    df = traps_data.copy()

    # Pesos e scores base
    df["damage_weight"]   = df["primaryPest"].map(PESOS_PRAGAS).fillna(1)
    df["infest_numeric"]  = df["trapInfestationLevel"].map(MAP_INFESTACAO).fillna(0)
    df["alert_index"]     = df["infest_numeric"] * df["damage_weight"]

    # Limiares absolutos por espécie
    df["acima_alert"]   = df.apply(lambda r: verificar_acima_limiar(r, "alert"),   axis=1)
    df["acima_control"] = df.apply(lambda r: verificar_acima_limiar(r, "control"), axis=1)
    df["acima_damage"]  = df.apply(lambda r: verificar_acima_limiar(r, "damage"),  axis=1)

    # Série temporal por armadilha
    df["pest_delta"] = df.groupby("trapId")["pestCount"].diff().fillna(0)
    df["dias_desde_ultima_leitura"] = (
        df.groupby("trapId")["createdAt"].diff().dt.total_seconds() / 86400
    ).fillna(0).round(2)
    df["taxa_crescimento_diario"] = (
        df["pest_delta"] / df["dias_desde_ultima_leitura"].replace(0, 1)
    ).round(2)

    # Tendência
    df["trend"] = df.apply(
        lambda r: "Crescente"
        if r["pest_delta"] > 0 or r["trapInfestationLevel"] in ["DAMAGE", "ALERT", "HIGH"]
        else "Estável/Caindo",
        axis=1,
    )

    # Contagem cumulativa de surtos consecutivos por armadilha
    df["surtos_consecutivos"] = (
        (df["trend"] == "Crescente")
        .groupby(df["trapId"])
        .cumsum()
    )

    # Eficácia de missões: missões concluídas / (concluídas + atrasadas)
    df["doneMissionCount"]  = pd.to_numeric(df["doneMissionCount"],  errors="coerce").fillna(0)
    df["lateMissionCount"]  = pd.to_numeric(df["lateMissionCount"],  errors="coerce").fillna(0)
    total_missoes = df["doneMissionCount"] + df["lateMissionCount"]
    df["eficacia_missao_pct"] = (
        (df["doneMissionCount"] / total_missoes.replace(0, 1)) * 100
    ).round(1)

    # Status de prioridade
    df["priority_status"] = df.apply(calcular_prioridade, axis=1)

    # Data formatada legível
    df["data_leitura"] = df["createdAt"].dt.strftime("%Y-%m-%d")

    return df


# ─────────────────────────────────────────────
# 3. RESUMOS AGREGADOS
# ─────────────────────────────────────────────

def gerar_resumo_armadilhas(df: pd.DataFrame) -> pd.DataFrame:
    """Resumo por armadilha: pico, tendência final, missões."""
    agg = df.groupby(["trapId", "trapCode", "primaryPest", "trapType", "trapStatus"]).agg(
        leituras           = ("pestCount",          "count"),
        max_pest_count     = ("pestCount",          "max"),
        media_pest_count   = ("pestCount",          "mean"),
        max_alert_index    = ("alert_index",        "max"),
        surtos_total       = ("surtos_consecutivos","max"),
        missoes_concluidas = ("doneMissionCount",   "sum"),
        missoes_atrasadas  = ("lateMissionCount",   "sum"),
        acima_damage_count = ("acima_damage",       "sum"),
        primeira_leitura   = ("data_leitura",       "min"),
        ultima_leitura     = ("data_leitura",       "max"),
    ).reset_index()

    total_m = agg["missoes_concluidas"] + agg["missoes_atrasadas"]
    agg["eficacia_missao_pct"] = ((agg["missoes_concluidas"] / total_m.replace(0, 1)) * 100).round(1)
    agg["media_pest_count"]    = agg["media_pest_count"].round(2)

    return agg.sort_values("max_alert_index", ascending=False)


def gerar_resumo_pragas(df: pd.DataFrame, pest_details: pd.DataFrame) -> pd.DataFrame:
    """Resumo por espécie: pressão média, limiares, % acima do limiar de controle."""
    agg = df.groupby("primaryPest").agg(
        armadilhas_monitoradas = ("trapId",         "nunique"),
        leituras_totais        = ("pestCount",      "count"),
        media_pesticidas       = ("pestCount",      "mean"),
        max_pesticidas         = ("pestCount",      "max"),
        pct_acima_control      = ("acima_control",  "mean"),
        pct_acima_damage       = ("acima_damage",   "mean"),
        pct_crescente          = ("trend",          lambda x: (x == "Crescente").mean()),
        eficacia_missao_media  = ("eficacia_missao_pct", "mean"),
        max_surtos_consecutivos= ("surtos_consecutivos", "max"),
    ).reset_index()

    agg["pct_acima_control"]  = (agg["pct_acima_control"]  * 100).round(1)
    agg["pct_acima_damage"]   = (agg["pct_acima_damage"]   * 100).round(1)
    agg["pct_crescente"]      = (agg["pct_crescente"]      * 100).round(1)
    agg["eficacia_missao_media"] = agg["eficacia_missao_media"].round(1)
    agg["media_pesticidas"]   = agg["media_pesticidas"].round(2)

    # Adiciona limiares da documentação
    agg["limiar_alerta"]   = agg["primaryPest"].map(lambda p: LIMIARES.get(p, {}).get("alert",  "N/D"))
    agg["limiar_controle"] = agg["primaryPest"].map(lambda p: LIMIARES.get(p, {}).get("control","N/D"))
    agg["limiar_dano"]     = agg["primaryPest"].map(lambda p: LIMIARES.get(p, {}).get("damage", "N/D"))
    agg["peso_dano"]       = agg["primaryPest"].map(PESOS_PRAGAS).fillna(1)

    return agg.sort_values("pct_acima_damage", ascending=False)


# ─────────────────────────────────────────────
# 4. GERAÇÃO DO DASHBOARD HTML
# ─────────────────────────────────────────────

def gerar_dashboard(df: pd.DataFrame, resumo_armadilhas: pd.DataFrame, resumo_pragas: pd.DataFrame):
    """Gera dashboard interativo com Chart.js."""

    # Prepara dados para os gráficos
    # 4a. Série temporal de contagem por praga (média diária)
    df_temporal = df[df["pestCount"].notna()].copy()
    df_temporal["data"] = df_temporal["createdAt"].dt.strftime("%Y-%m-%d")
    serie = df_temporal.groupby(["data", "primaryPest"])["pestCount"].mean().reset_index()

    pragas_unicas = sorted(serie["primaryPest"].unique())
    datas_unicas  = sorted(serie["data"].unique())

    cores_pragas = {
        "Lagarta Spodoptera": "#f97316",
        "Cigarrinha":         "#22c55e",
        "Percevejo Marrom":   "#a855f7",
        "Percevejo Barriga Verde": "#ef4444",
        "Percevejo Gaúcho":   "#3b82f6",
    }

    datasets_linha = []
    for praga in pragas_unicas:
        sub = serie[serie["primaryPest"] == praga].set_index("data")["pestCount"]
        pontos = [round(sub.get(d, None) or 0, 2) for d in datas_unicas]
        cor = cores_pragas.get(praga, "#94a3b8")
        datasets_linha.append({
            "label": praga,
            "data": pontos,
            "borderColor": cor,
            "backgroundColor": cor + "33",
            "fill": False,
            "tension": 0.4,
            "pointRadius": 5,
            "pointHoverRadius": 8,
        })

    # 4b. Bar chart por armadilha (top 12 por max_pest_count)
    top = resumo_armadilhas.nlargest(12, "max_pest_count")
    bar_labels  = top["trapCode"].tolist()
    bar_values  = top["max_pest_count"].tolist()
    bar_species = top["primaryPest"].tolist()
    bar_colors  = [cores_pragas.get(p, "#94a3b8") for p in bar_species]

    # 4c. Distribuição de prioridade
    prio_counts = df["priority_status"].value_counts()
    prio_labels = prio_counts.index.tolist()
    prio_values = prio_counts.values.tolist()
    prio_colors = ["#ef4444", "#f97316", "#eab308", "#22c55e"][:len(prio_labels)]

    # 4d. Tabela de casos críticos
    criticos = df[
        (df["alert_index"] >= 10) & (df["trapStatus"] == "ACTIVE")
    ].sort_values("pestCount", ascending=False).head(20)

    def tabela_criticos_html(df_c):
        linhas = ""
        for _, r in df_c.iterrows():
            status_cls = "critical" if "CRÍTICO" in str(r["priority_status"]) else "warning"
            linhas += f"""
            <tr>
                <td><span class="trap-badge">{r.get('trapCode','—')}</span></td>
                <td>{r.get('primaryPest','—')}</td>
                <td><strong>{int(r['pestCount']) if pd.notna(r['pestCount']) else '—'}</strong></td>
                <td>{r.get('trapInfestationLevel','—')}</td>
                <td><span class="status-badge {status_cls}">{r['priority_status']}</span></td>
                <td>{r.get('data_leitura','—')}</td>
                <td>{r.get('taxa_crescimento_diario', 0):.2f}/dia</td>
            </tr>"""
        return linhas

    # 4e. KPIs
    total_armadilhas = df["trapId"].nunique()
    armadilhas_ativas = df[df["trapStatus"] == "ACTIVE"]["trapId"].nunique()
    pct_critico = round(len(df[df["priority_status"].str.contains("CRÍTICO", na=False)]) / max(len(df), 1) * 100, 1)
    max_cigarrinha = int(df[df["primaryPest"] == "Cigarrinha"]["pestCount"].max() or 0)
    max_spodo  = int(df[df["primaryPest"] == "Lagarta Spodoptera"]["pestCount"].max() or 0)
    eficacia_media = round(df["eficacia_missao_pct"].mean(), 1)

    # 4f. Resumo pragas para tabela
    def tabela_pragas_html(df_p):
        linhas = ""
        for _, r in df_p.iterrows():
            cor = cores_pragas.get(r["primaryPest"], "#94a3b8")
            linhas += f"""
            <tr>
                <td><span class="dot" style="background:{cor}"></span> {r['primaryPest']}</td>
                <td>{r['armadilhas_monitoradas']}</td>
                <td>{r['media_pesticidas']:.1f}</td>
                <td>{r['max_pesticidas']:.0f}</td>
                <td>{r['pct_acima_control']}%</td>
                <td>{r['pct_acima_damage']}%</td>
                <td>{r['pct_crescente']}%</td>
                <td>{r['limiar_alerta']} / {r['limiar_controle']} / {r['limiar_dano']}</td>
            </tr>"""
        return linhas

    html = html # apenas pra não dar erro de variável não definida
    with open("./dashboard_pragas.html", "w", encoding="utf-8") as f:
        f.write(html)
    print("[INFO] dashboard_pragas.html gerado com sucesso.")


# ─────────────────────────────────────────────
# 5. EXECUÇÃO PRINCIPAL
# ─────────────────────────────────────────────

if __name__ == "__main__":
    traps_data, pest_details = carregar_dados()

    print(f"[INFO] Espécies de milho em traps_data: {traps_data['primaryPest'].unique().tolist()}")
    print(f"[INFO] Armadilhas únicas: {traps_data['trapId'].nunique()}")

    df_enriquecido = enriquecer(traps_data)

    resumo_arm   = gerar_resumo_armadilhas(df_enriquecido)
    resumo_pragas = gerar_resumo_pragas(df_enriquecido, pest_details)

    diagnostico = df_enriquecido[
        (df_enriquecido["alert_index"] >= 10) &
        (df_enriquecido["trapStatus"] == "ACTIVE")
    ].sort_values("pestCount", ascending=False)

    # Salva CSVs
    df_enriquecido.to_csv("./output/tratado_enriquecido.csv",    index=False)
    diagnostico.to_csv("./output/diagnostico_persistencia.csv",  index=False)
    resumo_arm.to_csv("./output/resumo_armadilhas.csv",          index=False)
    resumo_pragas.to_csv("./output/resumo_pragas.csv",           index=False)

    # Dashboard HTML
    gerar_dashboard(df_enriquecido, resumo_arm, resumo_pragas)

    print("\n── RESUMO POR ESPÉCIE ──")
    print(resumo_pragas[["primaryPest","armadilhas_monitoradas","media_pesticidas",
                          "pct_acima_damage","pct_crescente","limiar_controle"]].to_string(index=False))

    print("\n── TOP 5 ARMADILHAS CRÍTICAS ──")
    print(resumo_arm[["trapCode","primaryPest","max_pest_count","max_alert_index","eficacia_missao_pct"]]
          .head(5).to_string(index=False))

    print("\n✅ Concluído. Abra dashboard_pragas.html no navegador.\n")

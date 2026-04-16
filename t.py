html = f"""<!DOCTYPE html>
<html lang="pt-BR">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>FarmLab — Dashboard de Pragas | Safra 2025/2026</title>
<script src="https://cdn.jsdelivr.net/npm/chart.js@4.4.0/dist/chart.umd.min.js"></script>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap" rel="stylesheet">
<style>
  :root {{
    --bg: #0a0f1e;
    --surface: #111827;
    --surface2: #1a2235;
    --border: #1e2d45;
    --text: #e2e8f0;
    --muted: #64748b;
    --accent: #f97316;
    --green: #22c55e;
    --red: #ef4444;
    --yellow: #eab308;
    --blue: #3b82f6;
    --purple: #a855f7;
  }}
  * {{ box-sizing: border-box; margin: 0; padding: 0; }}
  body {{
    font-family: 'Inter', sans-serif;
    background: var(--bg);
    color: var(--text);
    min-height: 100vh;
    padding: 0;
  }}

  /* HEADER */
  .header {{
    background: linear-gradient(135deg, #0f172a 0%, #1a1035 50%, #0a1628 100%);
    border-bottom: 1px solid var(--border);
    padding: 2rem 2.5rem;
    display: flex;
    align-items: center;
    justify-content: space-between;
    position: relative;
    overflow: hidden;
  }}
  .header::before {{
    content: '';
    position: absolute;
    inset: 0;
    background: radial-gradient(ellipse at 20% 50%, rgba(249,115,22,0.08) 0%, transparent 60%),
                radial-gradient(ellipse at 80% 30%, rgba(34,197,94,0.06) 0%, transparent 50%);
  }}
  .header-left {{ position: relative; z-index: 1; }}
  .header-logo {{ display: flex; align-items: center; gap: 0.75rem; margin-bottom: 0.5rem; }}
  .header-logo-icon {{
    width: 44px; height: 44px; border-radius: 12px;
    background: linear-gradient(135deg, #f97316, #ea580c);
    display: flex; align-items: center; justify-content: center;
    font-size: 1.4rem; box-shadow: 0 0 20px rgba(249,115,22,0.4);
  }}
  .header-title {{ font-size: 1.6rem; font-weight: 800; letter-spacing: -0.02em; }}
  .header-title span {{ color: var(--accent); }}
  .header-sub {{ font-size: 0.85rem; color: var(--muted); margin-top: 0.25rem; }}
  .header-badges {{ display: flex; gap: 0.5rem; flex-wrap: wrap; position: relative; z-index: 1; }}
  .badge {{
    padding: 0.35rem 0.9rem; border-radius: 999px; font-size: 0.75rem; font-weight: 600;
    border: 1px solid; backdrop-filter: blur(8px);
  }}
  .badge-orange {{ background: rgba(249,115,22,0.12); border-color: rgba(249,115,22,0.3); color: #fb923c; }}
  .badge-green  {{ background: rgba(34,197,94,0.12);  border-color: rgba(34,197,94,0.3);  color: #4ade80; }}
  .badge-blue   {{ background: rgba(59,130,246,0.12); border-color: rgba(59,130,246,0.3); color: #60a5fa; }}

  /* LAYOUT */
  .main {{ padding: 2rem 2.5rem; max-width: 1600px; margin: 0 auto; }}

  /* KPI CARDS */
  .kpi-grid {{
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
    gap: 1rem;
    margin-bottom: 2rem;
  }}
  .kpi-card {{
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: 16px;
    padding: 1.25rem 1.5rem;
    position: relative;
    overflow: hidden;
    transition: transform 0.2s, border-color 0.2s;
  }}
  .kpi-card:hover {{ transform: translateY(-2px); border-color: rgba(249,115,22,0.4); }}
  .kpi-card::before {{
    content: ''; position: absolute; inset: 0;
    background: var(--glow, transparent);
    opacity: 0.05; pointer-events: none;
  }}
  .kpi-icon {{ font-size: 1.6rem; margin-bottom: 0.6rem; }}
  .kpi-value {{ font-size: 2rem; font-weight: 800; letter-spacing: -0.03em; }}
  .kpi-label {{ font-size: 0.78rem; color: var(--muted); margin-top: 0.2rem; text-transform: uppercase; letter-spacing: 0.05em; }}
  .kpi-sub {{ font-size: 0.75rem; margin-top: 0.5rem; padding-top: 0.5rem; border-top: 1px solid var(--border); color: var(--muted); }}

  /* CHART CARDS */
  .charts-grid {{
    display: grid;
    grid-template-columns: 2fr 1fr;
    gap: 1.5rem;
    margin-bottom: 2rem;
  }}
  .chart-card {{
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: 16px;
    padding: 1.5rem;
  }}
  .chart-card.full {{ grid-column: 1 / -1; }}
  .chart-header {{ margin-bottom: 1.25rem; }}
  .chart-title {{ font-size: 1rem; font-weight: 700; }}
  .chart-sub {{ font-size: 0.78rem; color: var(--muted); margin-top: 0.2rem; }}
  .chart-canvas {{ width: 100% !important; }}

  /* TABLES */
  .table-card {{
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: 16px;
    overflow: hidden;
    margin-bottom: 2rem;
  }}
  .table-header {{
    padding: 1.25rem 1.5rem;
    border-bottom: 1px solid var(--border);
    display: flex; align-items: center; justify-content: space-between;
  }}
  .table-title {{ font-size: 1rem; font-weight: 700; }}
  .table-count {{
    font-size: 0.75rem; background: var(--surface2); border: 1px solid var(--border);
    padding: 0.25rem 0.75rem; border-radius: 999px; color: var(--muted);
  }}
  .table-wrap {{ overflow-x: auto; }}
  table {{ width: 100%; border-collapse: collapse; font-size: 0.84rem; }}
  th {{
    padding: 0.75rem 1rem; text-align: left; font-size: 0.72rem;
    text-transform: uppercase; letter-spacing: 0.06em;
    color: var(--muted); border-bottom: 1px solid var(--border);
    background: var(--surface2);
  }}
  td {{ padding: 0.75rem 1rem; border-bottom: 1px solid rgba(30,45,69,0.5); }}
  tr:last-child td {{ border-bottom: none; }}
  tr:hover td {{ background: rgba(255,255,255,0.02); }}

  /* BADGES / STATUS */
  .trap-badge {{
    background: var(--surface2); border: 1px solid var(--border);
    padding: 0.2rem 0.6rem; border-radius: 6px; font-size: 0.75rem;
    font-family: monospace; color: var(--accent);
  }}
  .status-badge {{
    padding: 0.2rem 0.7rem; border-radius: 999px; font-size: 0.72rem; font-weight: 600;
  }}
  .status-badge.critical {{ background: rgba(239,68,68,0.15); color: #f87171; border: 1px solid rgba(239,68,68,0.3); }}
  .status-badge.warning  {{ background: rgba(249,115,22,0.15); color: #fb923c; border: 1px solid rgba(249,115,22,0.3); }}
  .dot {{
    display: inline-block; width: 10px; height: 10px; border-radius: 50%; margin-right: 6px; vertical-align: middle;
  }}

  /* SECTION TITLE */
  .section-title {{
    font-size: 0.7rem; text-transform: uppercase; letter-spacing: 0.1em;
    color: var(--muted); margin-bottom: 0.75rem; padding-left: 2px;
  }}

  /* ALERTS BOX */
  .alert-box {{
    background: rgba(239,68,68,0.07);
    border: 1px solid rgba(239,68,68,0.25);
    border-radius: 12px;
    padding: 1rem 1.25rem;
    margin-bottom: 2rem;
  }}
  .alert-box h3 {{ font-size: 0.9rem; color: #f87171; margin-bottom: 0.5rem; }}
  .alert-box ul {{ list-style: none; }};
  .alert-box li {{ font-size: 0.82rem; color: var(--muted); padding: 0.25rem 0; }}
  .alert-box li::before {{ content: '→ '; color: #f87171; }}

  /* FOOTER */
  .footer {{
    text-align: center; padding: 2rem; color: var(--muted);
    font-size: 0.75rem; border-top: 1px solid var(--border);
    margin-top: 2rem;
  }}

  @media (max-width: 900px) {{
    .charts-grid {{ grid-template-columns: 1fr; }}
    .kpi-grid {{ grid-template-columns: repeat(2, 1fr); }}
    .header {{ flex-direction: column; gap: 1rem; align-items: flex-start; }}
    .main {{ padding: 1rem; }}
  }}
</style>
</head>
<body>

<header class="header">
  <div class="header-left">
    <div class="header-logo">
      <div class="header-logo-icon">🌿</div>
      <div>
        <div class="header-title">Farm<span>Lab</span> · Pragas</div>
        <div class="header-sub">Monitoramento MIIP — Safra 2025/2026 · Milho · Marília-SP</div>
      </div>
    </div>
  </div>
  <div class="header-badges">
    <span class="badge badge-orange">⚠ {pct_critico}% registros críticos</span>
    <span class="badge badge-green">✅ {eficacia_media}% eficácia de missões</span>
    <span class="badge badge-blue">📡 {total_armadilhas} armadilhas · {armadilhas_ativas} ativas</span>
  </div>
</header>

<div class="main">

  <!-- KPIs -->
  <div class="section-title">Indicadores principais</div>
  <div class="kpi-grid">
    <div class="kpi-card" style="--glow: radial-gradient(circle at 50% 0%, #f97316, transparent)">
      <div class="kpi-icon">🪲</div>
      <div class="kpi-value" style="color:#fb923c">{total_armadilhas}</div>
      <div class="kpi-label">Armadilhas totais</div>
      <div class="kpi-sub">{armadilhas_ativas} ativas agora</div>
    </div>
    <div class="kpi-card" style="--glow: radial-gradient(circle at 50% 0%, #ef4444, transparent)">
      <div class="kpi-icon">🔴</div>
      <div class="kpi-value" style="color:#f87171">{pct_critico}%</div>
      <div class="kpi-label">Leituras críticas</div>
      <div class="kpi-sub">alert_index ≥ 10 e ACTIVE</div>
    </div>
    <div class="kpi-card" style="--glow: radial-gradient(circle at 50% 0%, #22c55e, transparent)">
      <div class="kpi-icon">🎯</div>
      <div class="kpi-value" style="color:#4ade80">{eficacia_media}%</div>
      <div class="kpi-label">Eficácia missões</div>
      <div class="kpi-sub">missões concluídas / total</div>
    </div>
    <div class="kpi-card" style="--glow: radial-gradient(circle at 50% 0%, #22c55e, transparent)">
      <div class="kpi-icon">🦗</div>
      <div class="kpi-value" style="color:#4ade80">{max_cigarrinha}</div>
      <div class="kpi-label">Pico Cigarrinha</div>
      <div class="kpi-sub">insetos/armadilha (limiar: 30)</div>
    </div>
    <div class="kpi-card" style="--glow: radial-gradient(circle at 50% 0%, #f97316, transparent)">
      <div class="kpi-icon">🐛</div>
      <div class="kpi-value" style="color:#fb923c">{max_spodo}</div>
      <div class="kpi-label">Pico Spodoptera</div>
      <div class="kpi-sub">lagartas/armadilha (limiar: 4)</div>
    </div>
    <div class="kpi-card">
      <div class="kpi-icon">📊</div>
      <div class="kpi-value" style="color:#60a5fa">{len(df)}</div>
      <div class="kpi-label">Total de leituras</div>
      <div class="kpi-sub">após deduplicação</div>
    </div>
  </div>

  <!-- ALERTA DE INTERPRETAÇÃO -->
  <div class="alert-box">
    <h3>⚠ Por que as pragas persistem mesmo com agrotóxicos?</h3>
    <ul>
      <li>A Lagarta Spodoptera se esconde no cartucho — inseticida de contato não atinge (esconderijo anatômico)</li>
      <li>Cigarrinha transmite molicutes em minutos de contato — controle pós-infecção é ineficaz</li>
      <li>Migração contínua de lavouras/pastagens vizinhas ("ponte verde") repovoamento constante</li>
      <li>Uso repetido das mesmas moléculas acelera resistência (1-2% da população resistente prospera)</li>
      <li>Eficácia de missões de {eficacia_media}% sugere janelas de monitoramento com lacunas operacionais</li>
    </ul>
  </div>

  <!-- GRÁFICOS -->
  <div class="section-title">Análise temporal e distribuição</div>
  <div class="charts-grid">
    <div class="chart-card">
      <div class="chart-header">
        <div class="chart-title">Evolução Temporal — Contagem Média por Praga</div>
        <div class="chart-sub">Média de insetos por armadilha por data de leitura</div>
      </div>
      <canvas id="lineChart" class="chart-canvas" height="250"></canvas>
    </div>
    <div class="chart-card">
      <div class="chart-header">
        <div class="chart-title">Distribuição de Prioridade</div>
        <div class="chart-sub">Status de alerta de todas as leituras</div>
      </div>
      <canvas id="pieChart" class="chart-canvas" height="250"></canvas>
    </div>
  </div>

  <div class="charts-grid">
    <div class="chart-card full">
      <div class="chart-header">
        <div class="chart-title">Top Armadilhas — Pico de Infestação</div>
        <div class="chart-sub">Máximo de insetos registrado por armadilha (12 maiores)</div>
      </div>
      <canvas id="barChart" class="chart-canvas" height="160"></canvas>
    </div>
  </div>

  <!-- TABELA COMPARATIVA POR ESPÉCIE -->
  <div class="section-title">Análise comparativa por espécie</div>
  <div class="table-card">
    <div class="table-header">
      <div class="table-title">📊 Pressão e Limiares por Praga</div>
      <span class="table-count">{len(resumo_pragas)} espécies</span>
    </div>
    <div class="table-wrap">
      <table>
        <thead>
          <tr>
            <th>Praga</th>
            <th>Armadilhas</th>
            <th>Média/Arm.</th>
            <th>Pico</th>
            <th>% acima controle</th>
            <th>% acima dano</th>
            <th>% crescente</th>
            <th>Limiares (A/C/D)</th>
          </tr>
        </thead>
        <tbody>
          {tabela_pragas_html(resumo_pragas)}
        </tbody>
      </table>
    </div>
  </div>

  <!-- TABELA CASOS CRÍTICOS -->
  <div class="section-title">Casos críticos ativos</div>
  <div class="table-card">
    <div class="table-header">
      <div class="table-title">🔴 Armadilhas ATIVAS com Infestação Crítica</div>
      <span class="table-count">Top 20</span>
    </div>
    <div class="table-wrap">
      <table>
        <thead>
          <tr>
            <th>Armadilha</th>
            <th>Praga</th>
            <th>Contagem</th>
            <th>Nível</th>
            <th>Status</th>
            <th>Data</th>
            <th>Taxa (diária)</th>
          </tr>
        </thead>
        <tbody>
          {tabela_criticos_html(criticos)}
        </tbody>
      </table>
    </div>
  </div>

</div><!-- /main -->

<footer class="footer">
  FarmLab · Dashboard gerado em {datetime.now().strftime("%d/%m/%Y %H:%M")} · Safra 2025/2026 · Marília-SP · MIIP
</footer>

<script>
Chart.defaults.color = '#64748b';
Chart.defaults.borderColor = '#1e2d45';
Chart.defaults.font.family = 'Inter';

// LINE CHART
new Chart(document.getElementById('lineChart'), {{
  type: 'line',
  data: {{
    labels: {json.dumps(datas_unicas)},
    datasets: {json.dumps(datasets_linha)}
  }},
  options: {{
    responsive: true,
    interaction: {{ mode: 'index', intersect: false }},
    plugins: {{
      legend: {{ position: 'top', labels: {{ boxWidth: 12, font: {{ size: 11 }} }} }},
      tooltip: {{
        backgroundColor: '#1a2235',
        borderColor: '#1e2d45',
        borderWidth: 1,
      }}
    }},
    scales: {{
      x: {{ grid: {{ color: '#1e2d4555' }}, ticks: {{ maxTicksLimit: 8 }} }},
      y: {{ grid: {{ color: '#1e2d4555' }}, beginAtZero: true, title: {{ display: true, text: 'Insetos/armadilha' }} }}
    }}
  }}
}});

// PIE CHART
new Chart(document.getElementById('pieChart'), {{
  type: 'doughnut',
  data: {{
    labels: {json.dumps(prio_labels)},
    datasets: [{{
      data: {json.dumps(prio_values)},
      backgroundColor: {json.dumps(prio_colors)},
      borderWidth: 2,
      borderColor: '#111827'
    }}]
  }},
  options: {{
    responsive: true,
    cutout: '65%',
    plugins: {{
      legend: {{ position: 'bottom', labels: {{ boxWidth: 12, font: {{ size: 10 }}, padding: 12 }} }},
      tooltip: {{ backgroundColor: '#1a2235', borderColor: '#1e2d45', borderWidth: 1 }}
    }}
  }}
}});

// BAR CHART
new Chart(document.getElementById('barChart'), {{
  type: 'bar',
  data: {{
    labels: {json.dumps(bar_labels)},
    datasets: [{{
      label: 'Pico de Infestação (insetos/armadilha)',
      data: {json.dumps(bar_values)},
      backgroundColor: {json.dumps(bar_colors)},
      borderRadius: 6,
      borderSkipped: false,
    }}]
  }},
  options: {{
    responsive: true,
    plugins: {{
      legend: {{ display: false }},
      tooltip: {{ backgroundColor: '#1a2235', borderColor: '#1e2d45', borderWidth: 1 }}
    }},
    scales: {{
      x: {{ grid: {{ display: false }} }},
      y: {{ grid: {{ color: '#1e2d4555' }}, beginAtZero: true }}
    }}
  }}
}});
</script>
</body>
</html>"""

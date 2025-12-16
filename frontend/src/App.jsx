import React, { useEffect, useState } from "react";
import DataTable from "./components/DataTable";
import StatsChart from "./components/StatsChart";
import { runPipeline, fetchPreview, fetchStats, downloadParquet } from "./api";

export default function App() {
  const [loading, setLoading] = useState(false);
  const [preview, setPreview] = useState([]);
  const [stats, setStats] = useState({ nutriscore: {}, nova_group: {}, total_rows: 0 });
  const [message, setMessage] = useState("Prêt à lancer le pipeline");

  const refreshData = async () => {
    const [previewData, statsData] = await Promise.all([fetchPreview(50), fetchStats()]);
    setPreview(previewData.preview || []);
    setStats(statsData);
  };

  useEffect(() => {
    refreshData().catch(() => {});
  }, []);

  const handleRun = async () => {
    setLoading(true);
    setMessage("Pipeline en cours...");
    try {
      const result = await runPipeline();
      setMessage(`Pipeline terminé : ${result.rows} lignes`);
      await refreshData();
    } catch (err) {
      console.error(err);
      setMessage(err?.response?.data?.detail || err?.message || "Erreur lors de l'exécution");
    } finally {
      setLoading(false);
    }
  };

  const handleDownload = () => downloadParquet();

  return (
    <div className="layout">
      <div className="hero">
        <div>
          <div className="badge">OpenFoodFacts • TP2</div>
          <h1>Pipeline Data & Visualisation</h1>
        </div>
        <div className="message">⚡ {message}</div>
      </div>

      <div className="card">
        <div className="actions">
          <button onClick={handleRun} disabled={loading}>
            {loading ? "En cours..." : "Lancer le pipeline"}
          </button>
          <button onClick={refreshData} className="secondary" disabled={loading}>
            Rafraîchir l'aperçu
          </button>
          <button onClick={handleDownload} className="secondary">
            Télécharger le Parquet
          </button>
        </div>

        <div className="kpi-grid">
          <div className="kpi-card">
            <p className="kpi-title">Lignes nettoyées</p>
            <p className="kpi-value">{stats.total_rows || 0}</p>
          </div>
          <div className="kpi-card">
            <p className="kpi-title">Prévisualisation</p>
            <p className="kpi-value">{preview.length} lignes</p>
          </div>
          <div className="kpi-card">
            <p className="kpi-title">Nutri-Score distincts</p>
            <p className="kpi-value">{Object.keys(stats.nutriscore || {}).length}</p>
          </div>
          <div className="kpi-card">
            <p className="kpi-title">NOVA distincts</p>
            <p className="kpi-value">{Object.keys(stats.nova_group || {}).length}</p>
          </div>
        </div>
      </div>

      <div style={{ marginTop: 20 }} className="card">
        <h3>Aperçu des données (50 premières lignes)</h3>
        <DataTable data={preview} />
      </div>

      <div style={{ marginTop: 20, display: "grid", gap: 16, gridTemplateColumns: "1fr 1fr" }}>
        <StatsChart title="Répartition Nutri-Score" data={stats.nutriscore} />
        <StatsChart title="Répartition NOVA" data={stats.nova_group} />
      </div>
    </div>
  );
}


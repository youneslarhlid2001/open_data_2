import React from "react";
import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
} from "recharts";

const toSeries = (obj) =>
  Object.entries(obj || {}).map(([name, value]) => ({ name, value }));

export default function StatsChart({ title, data }) {
  const serie = toSeries(data);

  return (
    <div className="card" style={{ height: 300 }}>
      <h3>{title}</h3>
      {serie.length === 0 ? (
        <p>Aucune donnée</p>
      ) : (
        <ResponsiveContainer width="100%" height="100%">
          <BarChart data={serie} margin={{ top: 10, right: 10, left: 0, bottom: 20 }}>
            <CartesianGrid strokeDasharray="3 3" />
            <XAxis dataKey="name" />
            <YAxis allowDecimals={false} />
            <Tooltip />
            <Bar dataKey="value" fill="#2563eb" radius={[6, 6, 0, 0]} />
          </BarChart>
        </ResponsiveContainer>
      )}
    </div>
  );
}


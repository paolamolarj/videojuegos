import React, { useState } from 'react';

interface GameRecommendation {
  game: string;
  genre: string;
  affinity: string;
}

interface PlayedGame {
  app_id: number;
  title: string;
  hours_played: number;
}

interface UserProfile {
  steam_id: string;
  total_games_owned: number;
  top_played_games: PlayedGame[];
}

interface ApiResponse {
  status: string;
  engine: string;
  user_profile: UserProfile;
  recommendations: GameRecommendation[];
}

function App() {
  const [steamId, setSteamId] = useState<string>('');
  const [loading, setLoading] = useState<boolean>(false);
  const [data, setData] = useState<ApiResponse | null>(null);
  const [error, setError] = useState<string | null>(null);

  const handleSearch = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!steamId.trim()) return;

    setLoading(true);
    setError(null);

    try {
      const response = await fetch(`http://localhost:8000/api/steam/user/${steamId}`);
      if (!response.ok) throw new Error("Error al consultar la API de Steam o el motor de Spark.");
      
      const result: ApiResponse = await response.json();
      setData(result);
    } catch (err: any) {
      setError("No se pudo conectar con el servidor o el SteamID no es válido.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div style={styles.container}>
      <header style={styles.header}>
        <h1 style={styles.title}>🎮 GameMatch Big Data Engine</h1>
        <p style={styles.subtitle}>Sistema de Recomendación Inteligente con Apache Spark & Steam Web API</p>
      </header>

      {/* Formulario de Consulta por SteamID */}
      <div style={styles.card}>
        <h2>Consultar Perfil de Steam</h2>
        <p style={styles.instruction}>Ingresa tu SteamID de 64 bits para analizar tus horas jugadas y generar recomendaciones personalizadas.</p>
        
        <form onSubmit={handleSearch} style={styles.form}>
          <input
            type="text"
            value={steamId}
            onChange={(e) => setSteamId(e.target.value)}
            placeholder="Ej. 76561198000000000"
            style={styles.input}
            required
          />
          <button type="submit" style={styles.button} disabled={loading}>
            {loading ? 'Procesando en Clúster...' : 'Analizar y Recomendar'}
          </button>
        </form>
        {error && <p style={styles.error}>{error}</p>}
      </div>

      {/* Resultados de la Consulta */}
      {data && (
        <div style={styles.resultsContainer}>
          {/* Información del Motor y Perfil */}
          <div style={styles.card}>
            <h3>📊 Resumen del Análisis Big Data</h3>
            <p><strong>Motor Utilizado:</strong> {data.engine}</p>
            <p><strong>Juegos en Biblioteca:</strong> {data.user_profile.total_games_owned}</p>
          </div>

          {/* Top Recomendaciones */}
          <div style={styles.card}>
            <h3>🎯 Videojuegos Recomendados para Ti</h3>
            <table style={styles.table}>
              <thead>
                <tr>
                  <th style={styles.th}>#</th>
                  <th style={styles.th}>Videojuego</th>
                  <th style={styles.th}>Género</th>
                  <th style={styles.th}>Afinidad (ALS)</th>
                </tr>
              </thead>
              <tbody>
                {data.recommendations.map((rec, index) => (
                  <tr key={index} style={styles.tr}>
                    <td style={styles.td}>{index + 1}</td>
                    <td style={styles.td}><strong>{rec.game}</strong></td>
                    <td style={styles.td}>{rec.genre}</td>
                    <td style={styles.td}>
                      <span style={styles.badge}>{rec.affinity}</span>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      )}
    </div>
  );
}

const styles: { [key: string]: React.CSSProperties } = {
  container: { fontFamily: 'Inter, system-ui, sans-serif', maxWidth: '900px', margin: '0 auto', padding: '40px 20px', color: '#333', backgroundColor: '#f8fafc', minHeight: '100vh' },
  header: { textAlign: 'center', marginBottom: '30px' },
  title: { fontSize: '2.5rem', color: '#1e293b', marginBottom: '10px' },
  subtitle: { fontSize: '1.1rem', color: '#64748b' },
  card: { background: '#ffffff', padding: '30px', borderRadius: '12px', boxShadow: '0 4px 6px -1px rgb(0 0 0 / 0.1)', marginBottom: '30px' },
  instruction: { color: '#64748b', fontSize: '0.95rem', marginBottom: '15px' },
  form: { display: 'flex', gap: '15px' },
  input: { flex: 1, padding: '12px 16px', fontSize: '1rem', borderRadius: '8px', border: '1px solid #cbd5e1', outline: 'none' },
  button: { background: '#2563eb', color: '#fff', border: 'none', padding: '12px 24px', fontSize: '1rem', fontWeight: 'bold', borderRadius: '8px', cursor: 'pointer' },
  error: { color: '#dc2626', marginTop: '10px' },
  resultsContainer: { display: 'flex', flexDirection: 'column', gap: '20px' },
  table: { width: '100%', borderCollapse: 'collapse', textAlign: 'left', marginTop: '15px' },
  th: { background: '#f1f5f9', padding: '12px', borderBottom: '2px solid #e2e8f0', color: '#475569' },
  tr: { borderBottom: '1px solid #e2e8f0' },
  td: { padding: '14px 12px', color: '#334155' },
  badge: { background: '#dbeafe', color: '#1d4ed8', padding: '4px 10px', borderRadius: '20px', fontWeight: 'bold', fontSize: '0.85rem' }
};

export default App;
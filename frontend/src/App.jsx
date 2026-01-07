import React, { useState, useEffect } from 'react';
import './index.css';

// API Base URL: Use Render backend in production, localhost for development
const API_BASE = import.meta.env.PROD
  ? 'https://reddit-news-scraper-api.onrender.com'
  : 'http://localhost:8000';

function App() {
  const [signals, setSignals] = useState([]);
  const [loading, setLoading] = useState(true);
  const [scanning, setScanning] = useState(false);
  const [topics, setTopics] = useState([]);
  const [newTopic, setNewTopic] = useState('');

  const fetchSignals = async () => {
    try {
      setLoading(true);
      const res = await fetch(`${API_BASE}/signals`);
      const data = await res.json();
      setSignals(data);
    } catch (err) {
      console.error("Failed to fetch signals", err);
    } finally {
      setLoading(false);
    }
  };

  const fetchConfig = async () => {
    try {
      const res = await fetch(`${API_BASE}/config`);
      const data = await res.json();
      setTopics(data.subreddits || []);
    } catch (err) {
      console.error("Failed to fetch config", err);
    }
  };

  const updateConfig = async (newTopics) => {
    try {
      await fetch(`${API_BASE}/config`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ subreddits: newTopics })
      });
      setTopics(newTopics);
    } catch (err) {
      alert("Failed to update topics");
    }
  };

  const handleScan = async () => {
    try {
      setScanning(true);
      // Ensure the backend uses the LATEST topics from our state
      await updateConfig(topics);
      const res = await fetch(`${API_BASE}/run-scan`, { method: 'POST' });
      if (res.ok) {
        await fetchSignals();
      } else {
        const err = await res.json();
        alert("Scan failed: " + err.detail);
      }
    } catch (err) {
      alert("Scan failed: " + err.message);
    } finally {
      setScanning(false);
    }
  };

  const addTopic = () => {
    if (newTopic && !topics.includes(newTopic)) {
      const updated = [...topics, newTopic];
      setTopics(updated);
      updateConfig(updated);
      setNewTopic('');
    }
  };

  const removeTopic = (topic) => {
    const updated = topics.filter(t => t !== topic);
    setTopics(updated);
    updateConfig(updated);
  };

  useEffect(() => {
    fetchSignals();
    fetchConfig();
  }, []);

  return (
    <div className="app-container">
      <aside className="sidebar">
        <div className="logo">
          <span>📡</span> SignalAgent
        </div>
        <nav className="nav-links">
          <div className="nav-link active">Dashboard</div>
        </nav>
        <div style={{ marginTop: 'auto', padding: '1rem', fontSize: '0.8rem', color: 'var(--text-dim)' }}>
          Popularity Filter: <strong>30+ Comments</strong>
        </div>
      </aside>

      <main className="main-content">
        <header className="header" style={{ alignItems: 'flex-start' }}>
          <div className="title-group">
            <h1>Morning Digest</h1>
            <p>High-signal, popular posts (30+ comments)</p>
          </div>
          <div style={{ display: 'flex', flexDirection: 'column', alignItems: 'flex-end', gap: '1rem' }}>
            <button
              className="btn-primary"
              onClick={handleScan}
              disabled={scanning}
              style={{ width: '160px' }}
            >
              {scanning ? 'Scanning...' : 'Scan Now'}
            </button>
          </div>
        </header>

        {/* Unified Topic Manager Section */}
        <section className="glass-card" style={{ padding: '1.5rem', marginBottom: '3rem' }}>
          <div style={{ display: 'flex', gap: '1rem', marginBottom: '1rem', alignItems: 'center' }}>
            <h3 style={{ fontSize: '1rem', color: 'var(--text-dim)', minWidth: '100px' }}>Active Topics:</h3>
            <div style={{ flex: 1, display: 'flex', flexWrap: 'wrap', gap: '0.5rem' }}>
              {topics.map(topic => (
                <div key={topic} className="subreddit-tag" style={{ display: 'flex', alignItems: 'center', gap: '0.4rem' }}>
                  r/{topic}
                  <span
                    style={{ cursor: 'pointer', opacity: 0.6, fontSize: '0.8rem' }}
                    onClick={() => removeTopic(topic)}
                  >
                    ✕
                  </span>
                </div>
              ))}
            </div>
          </div>
          <div style={{ display: 'flex', gap: '0.75rem' }}>
            <input
              type="text"
              value={newTopic}
              onChange={(e) => setNewTopic(e.target.value)}
              placeholder="Add subreddit (e.g. SideProject)"
              onKeyPress={(e) => e.key === 'Enter' && addTopic()}
              style={{
                flex: 1,
                padding: '0.6rem 1rem',
                borderRadius: '10px',
                border: '1px solid var(--border)',
                background: 'rgba(255,255,255,0.05)',
                color: 'white',
                fontSize: '0.9rem'
              }}
            />
            <button
              onClick={addTopic}
              style={{
                background: 'rgba(255,255,255,0.1)',
                border: '1px solid var(--border)',
                color: 'white',
                padding: '0.5rem 1rem',
                borderRadius: '10px',
                cursor: 'pointer',
                fontWeight: '600'
              }}
            >
              Add
            </button>
          </div>
        </section>

        {loading ? (
          <div className="signals-grid">
            {[1, 2, 3, 4, 5, 6].map(i => <div key={i} className="loading-pulse" />)}
          </div>
        ) : (
          <div className="signals-grid">
            {signals.map((signal, index) => (
              <div key={index} className="glass-card signal-card">
                <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                  <div className="subreddit-tag">r/{signal.subreddit}</div>
                  <div style={{ fontSize: '0.75rem', color: 'var(--accent)', fontWeight: '600' }}>
                    💬 {signal.num_comments} comments
                  </div>
                </div>
                <h3 className="signal-title">{signal.title}</h3>
                <div className="signal-content" dangerouslySetInnerHTML={{ __html: signal.content }} />
                <div className="signal-footer">
                  <span>By {signal.author}</span>
                  <a href={signal.link} target="_blank" rel="noopener noreferrer" className="read-more">View Post</a>
                </div>
              </div>
            ))}
            {signals.length === 0 && (
              <div style={{ textAlign: 'center', padding: '4rem', color: 'var(--text-dim)' }}>
                <p>No popular posts found with 30+ comments.</p>
                <p style={{ fontSize: '0.8rem', marginTop: '0.5rem' }}>Try adding more subreddits and running a scan.</p>
              </div>
            )}
          </div>
        )}
      </main>
    </div>
  );
}

export default App;

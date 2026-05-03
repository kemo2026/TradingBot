import React, { useState, useEffect } from 'react';

const styles = {
  app: {
    backgroundColor: '#0a0e1a',
    minHeight: '100vh',
    color: '#e0e0e0',
    fontFamily: "'Courier New', monospace",
    padding: '0',
    margin: '0',
  },
  header: {
    background: 'linear-gradient(90deg, #0a0e1a 0%, #1a1f35 50%, #0a0e1a 100%)',
    borderBottom: '1px solid #f0b90b',
    padding: '15px 30px',
    display: 'flex',
    justifyContent: 'space-between',
    alignItems: 'center',
  },
  logo: {
    color: '#f0b90b',
    fontSize: '24px',
    fontWeight: 'bold',
    letterSpacing: '3px',
  },
  liveIndicator: {
    display: 'flex',
    alignItems: 'center',
    gap: '8px',
    color: '#00ff88',
    fontSize: '12px',
  },
  liveDot: {
    width: '8px',
    height: '8px',
    borderRadius: '50%',
    backgroundColor: '#00ff88',
    animation: 'pulse 1s infinite',
  },
  mainGrid: {
    display: 'grid',
    gridTemplateColumns: '1fr 1fr 1fr',
    gap: '20px',
    padding: '20px',
  },
  card: {
    background: 'linear-gradient(135deg, #0d1117 0%, #161b22 100%)',
    border: '1px solid #30363d',
    borderRadius: '12px',
    padding: '20px',
  },
  priceCard: {
    background: 'linear-gradient(135deg, #0d1117 0%, #161b22 100%)',
    border: '1px solid #f0b90b',
    borderRadius: '12px',
    padding: '30px',
    textAlign: 'center',
    gridColumn: '1 / -1',
  },
  price: {
    fontSize: '72px',
    fontWeight: 'bold',
    color: '#f0b90b',
    textShadow: '0 0 30px rgba(240, 185, 11, 0.5)',
    letterSpacing: '2px',
  },
  signalCard: {
    borderRadius: '12px',
    padding: '30px',
    textAlign: 'center',
    gridColumn: '1 / -1',
    transition: 'all 0.3s ease',
  },
  signalText: {
    fontSize: '48px',
    fontWeight: 'bold',
    letterSpacing: '5px',
    textTransform: 'uppercase',
  },
  detailRow: {
    display: 'flex',
    justifyContent: 'space-between',
    padding: '12px 0',
    borderBottom: '1px solid #30363d',
    fontSize: '16px',
  },
  label: {
    color: '#8b949e',
    fontSize: '12px',
    letterSpacing: '2px',
    textTransform: 'uppercase',
    marginBottom: '5px',
  },
  value: {
    color: '#f0b90b',
    fontSize: '20px',
    fontWeight: 'bold',
  },
  capitalBtn: {
    padding: '12px 24px',
    borderRadius: '8px',
    border: '1px solid #30363d',
    backgroundColor: '#161b22',
    color: '#8b949e',
    fontSize: '16px',
    cursor: 'pointer',
    transition: 'all 0.2s ease',
    fontFamily: "'Courier New', monospace",
  },
  capitalBtnActive: {
    padding: '12px 24px',
    borderRadius: '8px',
    border: '1px solid #f0b90b',
    backgroundColor: '#f0b90b',
    color: '#000',
    fontSize: '16px',
    cursor: 'pointer',
    fontWeight: 'bold',
    fontFamily: "'Courier New', monospace",
  },
  refreshBtn: {
    width: '100%',
    padding: '15px',
    borderRadius: '8px',
    border: 'none',
    background: 'linear-gradient(90deg, #f0b90b, #ff9800)',
    color: '#000',
    fontSize: '16px',
    fontWeight: 'bold',
    cursor: 'pointer',
    letterSpacing: '2px',
    fontFamily: "'Courier New', monospace",
    marginTop: '20px',
  },
  statsGrid: {
    display: 'grid',
    gridTemplateColumns: '1fr 1fr',
    gap: '15px',
    marginTop: '20px',
  },
  statBox: {
    background: '#0d1117',
    border: '1px solid #30363d',
    borderRadius: '8px',
    padding: '15px',
    textAlign: 'center',
  },
  ticker: {
    background: '#050810',
    borderTop: '1px solid #f0b90b',
    borderBottom: '1px solid #f0b90b',
    padding: '8px 0',
    overflow: 'hidden',
    whiteSpace: 'nowrap',
  },
};

export default function App() {
  const [signal, setSignal] = useState(null);
  const [price, setPrice] = useState(null);
  const [capital, setCapital] = useState(20);
  const [loading, setLoading] = useState(true);
  const [lastUpdate, setLastUpdate] = useState('');
  const [countdown, setCountdown] = useState(60);

  const fetchSignal = async () => {
    try {
      const res = await fetch('http://localhost:8000/signal');
      const data = await res.json();
      setSignal(data);
      setPrice(data.price);
      setLoading(false);
      setLastUpdate(new Date().toLocaleTimeString());
      setCountdown(60);
    } catch (e) {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchSignal();
    const interval = setInterval(fetchSignal, 60000);
    return () => clearInterval(interval);
  }, []);

  useEffect(() => {
    const timer = setInterval(() => {
      setCountdown(prev => prev > 0 ? prev - 1 : 60);
    }, 1000);
    return () => clearInterval(timer);
  }, []);

  const getSignalColor = () => {
    if (!signal) return '#ff9800';
    if (signal.signal === 'LONG') return '#00c853';
    if (signal.signal === 'SHORT') return '#d50000';
    return '#ff9800';
  };

  const getSignalBg = () => {
    if (!signal) return 'rgba(255, 152, 0, 0.1)';
    if (signal.signal === 'LONG') return 'rgba(0, 200, 83, 0.1)';
    if (signal.signal === 'SHORT') return 'rgba(213, 0, 0, 0.1)';
    return 'rgba(255, 152, 0, 0.1)';
  };

  return (
    <div style={styles.app}>
      {/* Header */}
      <div style={styles.header}>
        <div style={styles.logo}>⚡ GOLDBOT PRO</div>
        <div style={{ color: '#8b949e', fontSize: '12px', letterSpacing: '2px' }}>
          XAU/USD PERPETUAL
        </div>
        <div style={styles.liveIndicator}>
          <div style={styles.liveDot}></div>
          LIVE
        </div>
      </div>

      {/* Ticker */}
      <div style={styles.ticker}>
        <span style={{ color: '#f0b90b', padding: '0 30px', fontSize: '12px', letterSpacing: '2px' }}>
          ⚡ XAU/USD: ${price || '...'} &nbsp;&nbsp;|&nbsp;&nbsp;
          SIGNAL: {signal?.signal || 'ANALYZING'} &nbsp;&nbsp;|&nbsp;&nbsp;
          LONG: {signal?.long_signals || 0} &nbsp;&nbsp;|&nbsp;&nbsp;
          SHORT: {signal?.short_signals || 0} &nbsp;&nbsp;|&nbsp;&nbsp;
          NEXT UPDATE: {countdown}s &nbsp;&nbsp;|&nbsp;&nbsp;
          SMC STRATEGY ACTIVE ⚡
        </span>
      </div>

      {loading ? (
        <div style={{ textAlign: 'center', padding: '100px', color: '#f0b90b', fontSize: '24px' }}>
          ⚡ CONNECTING TO BINANCE...
        </div>
      ) : (
        <div style={{ padding: '20px' }}>

          {/* Price */}
          <div style={styles.priceCard}>
            <div style={styles.label}>GOLD SPOT PRICE</div>
            <div style={styles.price}>${price}</div>
            <div style={{ color: '#8b949e', fontSize: '12px', marginTop: '10px', letterSpacing: '2px' }}>
              LAST UPDATE: {lastUpdate}
            </div>
          </div>

          {/* Signal */}
          <div style={{
            ...styles.signalCard,
            backgroundColor: getSignalBg(),
            border: `2px solid ${getSignalColor()}`,
            boxShadow: `0 0 30px ${getSignalColor()}33`,
            marginTop: '20px',
          }}>
            <div style={styles.label}>TRADING SIGNAL</div>
            <div style={{ ...styles.signalText, color: getSignalColor() }}>
              {signal?.signal === 'LONG' && '▲ LONG — BUY'}
              {signal?.signal === 'SHORT' && '▼ SHORT — SELL'}
              {signal?.signal === 'WAIT' && '⏸ WAIT — NO SIGNAL'}
            </div>
            <div style={{ color: '#8b949e', marginTop: '10px', fontSize: '12px', letterSpacing: '2px' }}>
              CONFIDENCE: {Math.max(signal?.long_signals || 0, signal?.short_signals || 0)}/10
            </div>
          </div>

          {/* Details Grid */}
          <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '20px', marginTop: '20px' }}>

            {/* Entry/SL/TP */}
            {signal?.signal !== 'WAIT' && (
              <div style={styles.card}>
                <div style={{ color: '#f0b90b', fontSize: '14px', letterSpacing: '3px', marginBottom: '15px' }}>
                  📊 TRADE DETAILS
                </div>
                <div style={styles.detailRow}>
                  <span style={{ color: '#8b949e' }}>ENTRY</span>
                  <span style={{ color: '#f0b90b', fontWeight: 'bold' }}>${signal?.entry}</span>
                </div>
                <div style={styles.detailRow}>
                  <span style={{ color: '#8b949e' }}>STOP LOSS</span>
                  <span style={{ color: '#ff4444', fontWeight: 'bold' }}>${signal?.sl}</span>
                </div>
                <div style={styles.detailRow}>
                  <span style={{ color: '#8b949e' }}>TAKE PROFIT 1</span>
                  <span style={{ color: '#00ff88', fontWeight: 'bold' }}>${signal?.tp1}</span>
                </div>
                <div style={styles.detailRow}>
                  <span style={{ color: '#8b949e' }}>TAKE PROFIT 2</span>
                  <span style={{ color: '#00ff88', fontWeight: 'bold' }}>${signal?.tp2}</span>
                </div>
                <div style={{ ...styles.detailRow, border: 'none' }}>
                  <span style={{ color: '#8b949e' }}>RISK/REWARD</span>
                  <span style={{ color: '#f0b90b', fontWeight: 'bold' }}>1:2 / 1:3</span>
                </div>
              </div>
            )}

            {/* Capital */}
            <div style={styles.card}>
              <div style={{ color: '#f0b90b', fontSize: '14px', letterSpacing: '3px', marginBottom: '15px' }}>
                💶 POSITION SIZE
              </div>
              <div style={{ display: 'flex', gap: '10px', marginBottom: '20px' }}>
                {[20, 50, 100, 200].map(cap => (
                  <button
                    key={cap}
                    onClick={() => setCapital(cap)}
                    style={capital === cap ? styles.capitalBtnActive : styles.capitalBtn}
                  >
                    {cap}€
                  </button>
                ))}
              </div>
              <div style={styles.statsGrid}>
                <div style={styles.statBox}>
                  <div style={styles.label}>MARGIN</div>
                  <div style={styles.value}>{capital}€</div>
                </div>
                <div style={styles.statBox}>
                  <div style={styles.label}>x5 POSITION</div>
                  <div style={styles.value}>{capital * 5}€</div>
                </div>
                <div style={styles.statBox}>
                  <div style={styles.label}>x10 POSITION</div>
                  <div style={styles.value}>{capital * 10}€</div>
                </div>
                <div style={styles.statBox}>
                  <div style={styles.label}>MAX LOSS</div>
                  <div style={{ ...styles.value, color: '#ff4444' }}>{(capital * 0.1).toFixed(0)}€</div>
                </div>
              </div>
            </div>
          </div>

          {/* Signals Analysis */}
          <div style={{ ...styles.card, marginTop: '20px' }}>
            <div style={{ color: '#f0b90b', fontSize: '14px', letterSpacing: '3px', marginBottom: '15px' }}>
              🧠 SMC ANALYSIS
            </div>
            <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '10px' }}>
              <div style={styles.statBox}>
                <div style={styles.label}>BULLISH SIGNALS</div>
                <div style={{ ...styles.value, color: '#00ff88', fontSize: '36px' }}>
                  {signal?.long_signals || 0}
                </div>
              </div>
              <div style={styles.statBox}>
                <div style={styles.label}>BEARISH SIGNALS</div>
                <div style={{ ...styles.value, color: '#ff4444', fontSize: '36px' }}>
                  {signal?.short_signals || 0}
                </div>
              </div>
            </div>
          </div>

          {/* Refresh */}
          <button onClick={fetchSignal} style={styles.refreshBtn}>
            ⚡ REFRESH SIGNALS — NEXT AUTO: {countdown}s
          </button>

        </div>
      )}
    </div>
  );
}
import React from 'react';
import { Terminal, Database, Trash2, Cpu, Activity } from 'lucide-react';
import './Sidebar.css';

const Sidebar = ({ totalQueries, escalationCount, onSelectQuery, onClearChat, activeTheme, onThemeChange }) => {
  const departments = [
    { name: 'HR', label: 'HR Agent', audience: 'Internal Staff', color: 'hr' },
    { name: 'IT Support', label: 'IT Support Agent', audience: 'Internal Staff', color: 'it' },
    { name: 'Customer Support', label: 'Customer Support Agent', audience: 'External User', color: 'cs' },
    { name: 'Product & Promotions', label: 'Promotion Agent', audience: 'External User', color: 'pp' },
  ];

  const suggestions = [
    'How many leave days do I get?',
    'I need to reset my VPN password',
    'What is your return policy?',
    'Any discounts available today?',
    "I'm angry. My order is missing!",
  ];

  const resolutionRate = totalQueries > 0 ? Math.round(((totalQueries - escalationCount) / totalQueries) * 100) : 100;

  return (
    <aside className="sidebar">
      <div className="sidebar-brand">
        <div className="brand-logo">
          <Cpu className="logo-icon" />
        </div>
        <div className="brand-text">
          <h2>Sujith AI Console</h2>
          <span>Agentic support router</span>
        </div>
      </div>

      <div className="sidebar-section">
        <h3 className="section-title">Theme</h3>
        <div className="theme-toggle">
          <button
            className={`theme-toggle-btn ${activeTheme === 'light' ? 'active' : ''}`}
            onClick={() => onThemeChange('light')}
            type="button"
          >
            Light
          </button>
          <button
            className={`theme-toggle-btn ${activeTheme === 'dark' ? 'active' : ''}`}
            onClick={() => onThemeChange('dark')}
            type="button"
          >
            Dark
          </button>
        </div>
      </div>

      <div className="sidebar-section">
        <h3 className="section-title">
          <Activity size={14} />
          Live Metrics
        </h3>
        <div className="stats-list">
          <div className="stat-row">
            <span className="stat-tag">Queries</span>
            <span className="stat-code-val">{totalQueries}</span>
          </div>
          <div className="stat-row">
            <span className="stat-tag">Escalations</span>
            <span className="stat-code-val text-red">{escalationCount}</span>
          </div>
          <div className="stat-row highlight-row">
            <span className="stat-tag">Resolution</span>
            <span className="stat-code-val text-cyan">{resolutionRate}%</span>
          </div>
        </div>
      </div>

      <div className="sidebar-section">
        <h3 className="section-title">
          <Database size={14} />
          Active Departments
        </h3>
        <div className="dept-list">
          {departments.map((dept) => (
            <div key={dept.name} className="dept-item">
              <div className="dept-header-info">
                <span className={`badge badge-${dept.color}`}>{dept.label}</span>
                <span className="dept-status-indicator"></span>
              </div>
              <span className="dept-audience">Audience: {dept.audience}</span>
            </div>
          ))}
        </div>
      </div>

      <div className="sidebar-section flex-grow">
        <h3 className="section-title">
          <Terminal size={14} />
          Quick Prompts
        </h3>
        <div className="suggestions-list">
          {suggestions.map((query, index) => (
            <button key={index} className="suggestion-btn" onClick={() => onSelectQuery(query)}>
              <span className="terminal-prompt-char">{index + 1}.</span>
              <span className="suggestion-text">{query}</span>
            </button>
          ))}
        </div>
      </div>

      <div className="sidebar-footer">
        <button className="btn-secondary clear-btn" onClick={onClearChat}>
          <Trash2 size={15} />
          <span>Clear Chat</span>
        </button>
      </div>
    </aside>
  );
};

export default Sidebar;

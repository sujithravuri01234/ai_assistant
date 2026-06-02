import React, { useState, useEffect } from 'react';
import Sidebar from './components/Sidebar';
import ChatWindow from './components/ChatWindow';

function App() {
  const [messages, setMessages] = useState([]);
  const [inputText, setInputText] = useState('');
  const [isLoading, setIsLoading] = useState(false);

  const [awaitingForm, setAwaitingForm] = useState(false);
  const [escalationQuery, setEscalationQuery] = useState('');
  const [isFormSubmitting, setIsFormSubmitting] = useState(false);

  const [totalQueries, setTotalQueries] = useState(0);
  const [escalationCount, setEscalationCount] = useState(0);

  const [theme, setTheme] = useState(null);

  useEffect(() => {
    fetch('/api/health')
      .then((res) => res.json())
      .then((data) => console.log('Backend Status:', data))
      .catch(() => {
        console.warn('FastAPI backend is offline. Run: python app/api.py');
      });
  }, []);

  useEffect(() => {
    if (!theme) {
      document.body.removeAttribute('data-theme');
      return;
    }

    document.body.setAttribute('data-theme', theme);
  }, [theme]);

  const handleThemeSelect = (selectedTheme) => {
    setTheme(selectedTheme);
  };

  const handleSendMessage = async (text) => {
    if (isLoading || awaitingForm) return;

    const newUserMessage = { role: 'user', content: text };
    setMessages((prev) => [...prev, newUserMessage]);
    setInputText('');
    setIsLoading(true);
    setTotalQueries((prev) => prev + 1);

    try {
      const response = await fetch('/api/chat', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ query: text }),
      });

      if (!response.ok) {
        throw new Error(`API error: ${response.statusText}`);
      }

      const data = await response.json();

      const newBotMessage = {
        role: 'assistant',
        content: data.response,
        department: data.department,
        route: data.route,
        sentiment: data.sentiment,
      };

      setMessages((prev) => [...prev, newBotMessage]);

      if (data.route === 'escalation') {
        setEscalationCount((prev) => prev + 1);
      }

      if (data.requires_form) {
        setAwaitingForm(true);
        setEscalationQuery(text);
      }
    } catch (error) {
      console.error('Chat error:', error);
      setMessages((prev) => [
        ...prev,
        {
          role: 'assistant',
          content:
            'Could not connect to the AI backend. Verify that the FastAPI server is running (`python app/api.py` on port 8000).',
          department: 'unknown',
          route: 'error',
        },
      ]);
    } finally {
      setIsLoading(false);
    }
  };

  const handleEscalateSubmit = async (formData) => {
    setIsFormSubmitting(true);
    try {
      const response = await fetch('/api/escalate', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(formData),
      });

      if (!response.ok) {
        throw new Error(`Escalation error: ${response.statusText}`);
      }

      const data = await response.json();

      setMessages((prev) => [
        ...prev,
        {
          role: 'assistant',
          content: data.response,
          department: data.department,
          route: 'escalation',
          sentiment: data.sentiment,
        },
      ]);

      setAwaitingForm(false);
      setEscalationQuery('');
    } catch (error) {
      console.error('Escalation submit error:', error);
      setMessages((prev) => [
        ...prev,
        {
          role: 'assistant',
          content: `Failed to submit escalation form: ${error.message}. Please try again.`,
          department: 'unknown',
          route: 'error',
        },
      ]);
    } finally {
      setIsFormSubmitting(false);
    }
  };

  const handleSelectQuery = (query) => {
    if (isLoading || awaitingForm) return;
    handleSendMessage(query);
  };

  const handleClearChat = () => {
    setMessages([]);
    setInputText('');
    setIsLoading(false);
    setAwaitingForm(false);
    setEscalationQuery('');
    setTotalQueries(0);
    setEscalationCount(0);
  };

  if (!theme) {
    return (
      <div className="theme-screen">
        <div className="theme-card">
          <h1>Choose your theme</h1>
          <p>Select how you want the app to look right now.</p>
          <div className="theme-actions">
            <button className="btn-primary theme-btn" onClick={() => handleThemeSelect('dark')}>
              Dark Theme
            </button>
            <button className="btn-secondary theme-btn" onClick={() => handleThemeSelect('light')}>
              Light Theme
            </button>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="app-container">
      <Sidebar
        totalQueries={totalQueries}
        escalationCount={escalationCount}
        onSelectQuery={handleSelectQuery}
        onClearChat={handleClearChat}
        activeTheme={theme}
        onThemeChange={handleThemeSelect}
      />
      <ChatWindow
        messages={messages}
        inputText={inputText}
        setInputText={setInputText}
        onSendMessage={handleSendMessage}
        onEscalateSubmit={handleEscalateSubmit}
        isLoading={isLoading}
        awaitingForm={awaitingForm}
        escalationQuery={escalationQuery}
        isFormSubmitting={isFormSubmitting}
      />
    </div>
  );
}

export default App;

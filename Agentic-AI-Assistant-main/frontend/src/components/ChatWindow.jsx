import React, { useRef, useEffect } from 'react';
import { Send, Bot } from 'lucide-react';
import EscalationForm from './EscalationForm';
import './ChatWindow.css';

const ChatWindow = ({
  messages,
  inputText,
  setInputText,
  onSendMessage,
  onEscalateSubmit,
  isLoading,
  awaitingForm,
  escalationQuery,
  isFormSubmitting,
}) => {
  const messagesEndRef = useRef(null);

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages, isLoading, awaitingForm]);

  const handleSubmit = (e) => {
    e.preventDefault();
    if (inputText.trim()) {
      onSendMessage(inputText.trim());
    }
  };

  const getDeptBadge = (dept, route) => {
    if (route === 'escalation') return <span className="badge badge-escalation">Escalated to Human</span>;

    switch (dept) {
      case 'HR':
        return <span className="badge badge-hr">HR</span>;
      case 'IT Support':
        return <span className="badge badge-it">IT Support</span>;
      case 'Customer Support':
        return <span className="badge badge-cs">Customer Support</span>;
      case 'Product & Promotions':
        return <span className="badge badge-pp">Promotions</span>;
      default:
        return <span className="badge badge-escalation">Unknown Route</span>;
    }
  };

  return (
    <div className="chat-window">
      <header className="chat-header">
        <div className="chat-header-title">
          <Bot className="header-bot-icon" size={20} />
          <div>
            <h1>Agentic AI Assistant</h1>
            <p>Powered by LangGraph routing, LLM reasoning, and vector search</p>
          </div>
        </div>
        <div className="header-status">
          <span className="status-dot"></span>
          <span>Online</span>
        </div>
      </header>

      <div className="chat-messages-container">
        {messages.length === 0 ? (
          <div className="welcome-screen fade-in">
            <h2>Ask anything related to HR, IT, customer support, or promotions.</h2>
            <p>
              The assistant routes your request to the right specialist agent and can escalate to a human when
              needed.
            </p>
            <div className="welcome-features-grid">
              <div className="feature-card">
                <span className="feature-tag">HR</span>
                <h4>People & Policies</h4>
                <p>Leaves, benefits, onboarding, and internal process questions.</p>
              </div>
              <div className="feature-card">
                <span className="feature-tag">IT</span>
                <h4>Tech Support</h4>
                <p>Password resets, VPN access, device setup, and software requests.</p>
              </div>
              <div className="feature-card">
                <span className="feature-tag">Support</span>
                <h4>Customer Help</h4>
                <p>Orders, delivery, returns, refunds, and issue handling.</p>
              </div>
              <div className="feature-card">
                <span className="feature-tag">Promotions</span>
                <h4>Deals & Offers</h4>
                <p>Coupons, active promotions, loyalty perks, and eligibility.</p>
              </div>
            </div>
          </div>
        ) : (
          <div className="messages-list">
            {messages.map((msg, index) => (
              <div key={index} className={`message-row ${msg.role === 'user' ? 'row-user' : 'row-bot'}`}>
                <div className="message-bubble-wrapper">
                  {msg.role === 'assistant' && (
                    <div className="message-meta">
                      {getDeptBadge(msg.department, msg.route)}
                      {msg.sentiment && <span className="sentiment-tag">Sentiment: {msg.sentiment}</span>}
                    </div>
                  )}

                  <div
                    className={`message-bubble ${msg.role === 'user' ? 'bubble-user' : 'bubble-bot'} ${msg.route === 'escalation' ? 'bubble-escalation' : ''}`}
                  >
                    <span className="msg-text-content">{msg.content}</span>
                  </div>
                </div>
              </div>
            ))}

            {isLoading && (
              <div className="message-row row-bot">
                <div className="message-bubble-wrapper">
                  <div className="message-bubble bubble-bot loader-bubble">
                    <span className="loader-text">Thinking and routing your request...</span>
                    <span className="blinking-caret">|</span>
                  </div>
                </div>
              </div>
            )}

            {awaitingForm && (
              <div className="message-row row-bot full-width-escalate">
                <div className="message-bubble-wrapper full-width-escalate">
                  <EscalationForm onSubmit={onEscalateSubmit} query={escalationQuery} isSubmitting={isFormSubmitting} />
                </div>
              </div>
            )}

            <div ref={messagesEndRef} />
          </div>
        )}
      </div>

      <footer className="chat-footer-input">
        <form onSubmit={handleSubmit} className="input-form">
          <input
            type="text"
            className="chat-input-field"
            placeholder={awaitingForm ? 'Complete the escalation form above to continue' : 'Type your question here...'}
            value={inputText}
            onChange={(e) => setInputText(e.target.value)}
            disabled={isLoading || awaitingForm}
          />
          <button type="submit" className="btn-primary send-btn" disabled={!inputText.trim() || isLoading || awaitingForm}>
            <span>Send</span>
            <Send size={14} />
          </button>
        </form>
      </footer>
    </div>
  );
};

export default ChatWindow;

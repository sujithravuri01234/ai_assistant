import React, { useState } from 'react';
import { ShieldAlert, AlertTriangle } from 'lucide-react';
import './EscalationForm.css';

const EscalationForm = ({ onSubmit, query, isSubmitting }) => {
  const [name, setName] = useState('');
  const [email, setEmail] = useState('');
  const [phone, setPhone] = useState('');
  const [error, setError] = useState('');

  const handleSubmit = (e) => {
    e.preventDefault();
    if (!name.trim() || !email.trim() || !phone.trim()) {
      setError('Please fill all required fields.');
      return;
    }

    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    if (!emailRegex.test(email)) {
      setError('Please enter a valid email address.');
      return;
    }

    setError('');
    onSubmit({
      query,
      user_name: name,
      user_email: email,
      user_phone: phone,
    });
  };

  return (
    <div className="escalation-form-card">
      <div className="form-header">
        <div className="form-icon-badge">
          <ShieldAlert size={20} className="alert-icon" />
        </div>
        <div className="form-info">
          <h4>Human Escalation Required</h4>
          <p>Share your contact details and our team will follow up directly.</p>
        </div>
      </div>

      <form onSubmit={handleSubmit} className="form-content">
        {error && (
          <div className="form-error-banner">
            <AlertTriangle size={14} className="error-warn-icon" />
            <span>{error}</span>
          </div>
        )}

        <div className="form-grid">
          <div className="input-group">
            <label htmlFor="user_name">Name</label>
            <div className="input-wrapper">
              <input
                id="user_name"
                type="text"
                placeholder="Jane Doe"
                value={name}
                onChange={(e) => setName(e.target.value)}
                disabled={isSubmitting}
                required
              />
            </div>
          </div>

          <div className="input-group">
            <label htmlFor="user_email">Email</label>
            <div className="input-wrapper">
              <input
                id="user_email"
                type="email"
                placeholder="jane@company.com"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                disabled={isSubmitting}
                required
              />
            </div>
          </div>

          <div className="input-group full-width">
            <label htmlFor="user_phone">Phone</label>
            <div className="input-wrapper">
              <input
                id="user_phone"
                type="tel"
                placeholder="+1 555 123 4567"
                value={phone}
                onChange={(e) => setPhone(e.target.value)}
                disabled={isSubmitting}
                required
              />
            </div>
          </div>
        </div>

        <button type="submit" className="btn-primary submit-form-btn" disabled={isSubmitting}>
          {isSubmitting ? 'Submitting request...' : 'Submit escalation'}
        </button>
      </form>
    </div>
  );
};

export default EscalationForm;

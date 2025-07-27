import React, { useState } from 'react';
import axios from 'axios';
import { User, Lock, Mail, Eye, EyeOff } from 'lucide-react';
import './Login.css';

const Login = ({ onLogin }) => {
  const [isRegister, setIsRegister] = useState(false);
  const [showPassword, setShowPassword] = useState(false);
  const [formData, setFormData] = useState({
    username: '',
    password: '',
    email: ''
  });
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);

  const handleChange = (e) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value
    });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');
    setLoading(true);

    try {
      const endpoint = isRegister ? '/api/register' : '/api/login';
      const response = await axios.post(endpoint, formData);
      
      onLogin(response.data.token, response.data.user);
    } catch (error) {
      setError(error.response?.data?.error || 'An error occurred');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="login-container">
      <div className="login-background">
        <div className="background-pattern"></div>
      </div>
      
      <div className="login-card">
        <div className="login-header">
          <h1>AI Chatbot Platform</h1>
          <p>{isRegister ? 'Create your account' : 'Welcome back'}</p>
        </div>

        <form onSubmit={handleSubmit} className="login-form">
          <div className="form-group">
            <div className="input-wrapper">
              <User className="input-icon" size={20} />
              <input
                type="text"
                name="username"
                placeholder="Username"
                value={formData.username}
                onChange={handleChange}
                required
                className="form-input"
              />
            </div>
          </div>

          {isRegister && (
            <div className="form-group">
              <div className="input-wrapper">
                <Mail className="input-icon" size={20} />
                <input
                  type="email"
                  name="email"
                  placeholder="Email"
                  value={formData.email}
                  onChange={handleChange}
                  required
                  className="form-input"
                />
              </div>
            </div>
          )}

          <div className="form-group">
            <div className="input-wrapper">
              <Lock className="input-icon" size={20} />
              <input
                type={showPassword ? "text" : "password"}
                name="password"
                placeholder="Password"
                value={formData.password}
                onChange={handleChange}
                required
                className="form-input"
              />
              <button
                type="button"
                className="password-toggle"
                onClick={() => setShowPassword(!showPassword)}
              >
                {showPassword ? <EyeOff size={20} /> : <Eye size={20} />}
              </button>
            </div>
          </div>

          {error && <div className="error-message">{error}</div>}

          <button 
            type="submit" 
            className="submit-button"
            disabled={loading}
          >
            {loading ? 'Loading...' : (isRegister ? 'Create Account' : 'Sign In')}
          </button>
        </form>

        <div className="login-footer">
          <p>
            {isRegister ? 'Already have an account?' : "Don't have an account?"}
            <button
              type="button"
              className="toggle-button"
              onClick={() => setIsRegister(!isRegister)}
            >
              {isRegister ? 'Sign In' : 'Sign Up'}
            </button>
          </p>
        </div>

        <div className="demo-credentials">
          <p><strong>Demo Credentials:</strong></p>
          <p>Username: admin | Password: admin123</p>
        </div>
      </div>
    </div>
  );
};

export default Login; 
import React, { useState, useEffect } from 'react';
import axios from 'axios';
import DataTable from './DataTable';
import ChatPanel from './ChatPanel';
import Header from './Header';
import './Dashboard.css';

const Dashboard = ({ user, onLogout }) => {
  const [data, setData] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  useEffect(() => {
    fetchData();
  }, []);

  const fetchData = async () => {
    try {
      const token = localStorage.getItem('token');
      console.log('Fetching data with token:', token ? `${token.substring(0, 20)}...` : 'No token');
      
      const response = await axios.get('/api/data', {
        headers: { Authorization: `Bearer ${token}` },
        timeout: 10000 // 10 second timeout
      });
      
      console.log('Data fetch successful:', response.data.length, 'records');
      setData(response.data);
      setError(''); // Clear any previous errors
      
    } catch (error) {
      console.error('Detailed error fetching data:', {
        message: error.message,
        status: error.response?.status,
        statusText: error.response?.statusText,
        data: error.response?.data,
        config: {
          url: error.config?.url,
          method: error.config?.method,
          headers: error.config?.headers
        }
      });
      
      let errorMessage = 'Failed to fetch data';
      
      if (error.response) {
        // Server responded with error status
        const status = error.response.status;
        if (status === 401) {
          errorMessage = 'Authentication failed. Please log in again.';
          // Optionally redirect to login
        } else if (status === 403) {
          errorMessage = 'Access denied. You don\'t have permission to view this data.';
        } else if (status === 500) {
          errorMessage = 'Server error. Please try again later.';
        } else {
          errorMessage = `Server error (${status}): ${error.response.data?.detail || error.response.statusText}`;
        }
      } else if (error.request) {
        // Request was made but no response received
        errorMessage = 'Unable to connect to server. Please check if the backend is running.';
      } else {
        // Something else happened
        errorMessage = `Request error: ${error.message}`;
      }
      
      setError(errorMessage);
    } finally {
      setLoading(false);
    }
  };

  const refreshData = () => {
    setLoading(true);
    fetchData();
  };

  if (loading) {
    return (
      <div className="loading-container">
        <div className="loading-spinner"></div>
        <p>Loading dashboard...</p>
      </div>
    );
  }

  return (
    <div className="dashboard">
      <Header user={user} onLogout={onLogout} onRefresh={refreshData} />
      
      <div className="dashboard-content">
        <div className="data-section">
          <div className="section-header">
            <h2>Transactions Overview</h2>
            <p>BSB: 123-456 Account Number: 12345678</p>
          </div>
          {error ? (
            <div className="error-container">
              <p className="error-message">{error}</p>
              <button onClick={refreshData} className="retry-button">
                Retry
              </button>
            </div>
          ) : (
            <DataTable data={data} onRefresh={refreshData} />
          )}
        </div>

        <div className="chat-section">
          <ChatPanel user={user} />
        </div>
      </div>
    </div>
  );
};

export default Dashboard; 
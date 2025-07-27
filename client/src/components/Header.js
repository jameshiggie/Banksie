import React from 'react';
import { LogOut, RefreshCw, User } from 'lucide-react';
import './Header.css';

const Header = ({ user, onLogout, onRefresh }) => {
  return (
    <header className="header">
      <div className="header-left">
        <h1 className="header-title">Bank</h1>
      </div>
      
      <div className="header-right">
        <button 
          onClick={onRefresh}
          className="header-button refresh-button"
          title="Refresh Data"
        >
          <RefreshCw size={18} />
        </button>
        
        <div className="user-info">
          <User size={18} />
          <span className="username">{user.username}</span>
        </div>
        
        <button 
          onClick={onLogout}
          className="header-button logout-button"
          title="Logout"
        >
          <LogOut size={18} />
        </button>
      </div>
    </header>
  );
};

export default Header; 
import React, { useState } from 'react';
import { Search, Filter, ChevronUp, ChevronDown } from 'lucide-react';
import './DataTable.css';

const DataTable = ({ data, onRefresh }) => {
  const [searchTerm, setSearchTerm] = useState('');
  const [sortField, setSortField] = useState('transaction_date');
  const [sortDirection, setSortDirection] = useState('desc');
  const [filterCategory, setFilterCategory] = useState('all');

  const handleSort = (field) => {
    if (sortField === field) {
      setSortDirection(sortDirection === 'asc' ? 'desc' : 'asc');
    } else {
      setSortField(field);
      setSortDirection('asc');
    }
  };

  const filteredAndSortedData = data
    .filter(item => {
      const matchesSearch = item.description.toLowerCase().includes(searchTerm.toLowerCase()) ||
                           item.category.toLowerCase().includes(searchTerm.toLowerCase()) ||
                           item.reference_number?.toLowerCase().includes(searchTerm.toLowerCase());
      const matchesCategory = filterCategory === 'all' || item.category.toLowerCase() === filterCategory.toLowerCase();
      return matchesSearch && matchesCategory;
    })
    .sort((a, b) => {
      let aValue = a[sortField];
      let bValue = b[sortField];
      
      if (typeof aValue === 'string') {
        aValue = aValue.toLowerCase();
        bValue = bValue.toLowerCase();
      }
      
      if (sortDirection === 'asc') {
        return aValue > bValue ? 1 : -1;
      } else {
        return aValue < bValue ? 1 : -1;
      }
    });

  const formatDate = (dateString) => {
    return new Date(dateString).toLocaleDateString('en-US', {
      year: 'numeric',
      month: 'short',
      day: 'numeric'
    });
  };

  const formatCurrency = (amount) => {
    const value = parseFloat(amount);
    return new Intl.NumberFormat('en-US', {
      style: 'currency',
      currency: 'USD'
    }).format(Math.abs(value));
  };

  const getTransactionTypeClass = (type, amount) => {
    return type === 'Credit' || amount > 0 ? 'credit' : 'debit';
  };

  const getCategoryBadgeClass = (category) => {
    const categoryMap = {
      'sales': 'sales',
      'inventory': 'inventory',
      'rent': 'rent',
      'utilities': 'utilities',
      'payroll': 'payroll',
      'insurance': 'insurance',
      'marketing': 'marketing',
      'professional services': 'professional-services',
      'office expenses': 'office-expenses',
      'interest': 'interest',
      'refunds': 'refunds',
      'capital': 'capital'
    };
    return categoryMap[category.toLowerCase()] || 'other';
  };

  // Get unique categories for filter dropdown
  const categories = ['all', ...new Set(data.map(item => item.category))];

  return (
    <div className="data-table-container">
      <div className="table-controls">
        <div className="search-container">
          <Search className="search-icon" size={16} />
          <input
            type="text"
            placeholder="Search transactions..."
            value={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value)}
            className="search-input"
          />
        </div>
        
        <div className="filter-container">
          <Filter className="filter-icon" size={16} />
          <select
            value={filterCategory}
            onChange={(e) => setFilterCategory(e.target.value)}
            className="filter-select"
          >
            {categories.map(category => (
              <option key={category} value={category}>
                {category === 'all' ? 'All Categories' : category}
              </option>
            ))}
          </select>
        </div>
      </div>

      <div className="table-wrapper">
        <table className="data-table">
          <thead>
            <tr>
              <th 
                className="sortable"
                onClick={() => handleSort('transaction_date')}
              >
                <div className="sortable">
                  Date
                  {sortField === 'transaction_date' && (
                    sortDirection === 'asc' ? <ChevronUp size={14} /> : <ChevronDown size={14} />
                  )}
                </div>
              </th>
              <th 
                className="sortable"
                onClick={() => handleSort('description')}
              >
                <div className="sortable">
                  Description
                  {sortField === 'description' && (
                    sortDirection === 'asc' ? <ChevronUp size={14} /> : <ChevronDown size={14} />
                  )}
                </div>
              </th>
              <th 
                className="sortable"
                onClick={() => handleSort('category')}
              >
                <div className="sortable">
                  Category
                  {sortField === 'category' && (
                    sortDirection === 'asc' ? <ChevronUp size={14} /> : <ChevronDown size={14} />
                  )}
                </div>
              </th>
              <th 
                className="sortable"
                onClick={() => handleSort('amount')}
              >
                <div className="sortable">
                  Amount
                  {sortField === 'amount' && (
                    sortDirection === 'asc' ? <ChevronUp size={14} /> : <ChevronDown size={14} />
                  )}
                </div>
              </th>
              <th 
                className="sortable"
                onClick={() => handleSort('balance')}
              >
                <div className="sortable">
                  Balance
                  {sortField === 'balance' && (
                    sortDirection === 'asc' ? <ChevronUp size={14} /> : <ChevronDown size={14} />
                  )}
                </div>
              </th>
              <th>Reference</th>
              <th>Status</th>
            </tr>
          </thead>
          <tbody>
            {filteredAndSortedData.length === 0 ? (
              <tr>
                <td colSpan="7" className="no-data">
                  No transactions found
                </td>
              </tr>
            ) : (
              filteredAndSortedData.map((transaction) => (
                <tr key={transaction.id} className="table-row">
                  <td className="date-cell">
                    {formatDate(transaction.transaction_date)}
                  </td>
                  <td className="description-cell">
                    {transaction.description}
                  </td>
                  <td>
                    <span className={`category-badge ${getCategoryBadgeClass(transaction.category)}`}>
                      {transaction.category}
                    </span>
                  </td>
                  <td className={`amount-cell ${getTransactionTypeClass(transaction.transaction_type, transaction.amount)}`}>
                    {transaction.transaction_type === 'Debit' || transaction.amount < 0 ? '-' : '+'}
                    {formatCurrency(transaction.amount)}
                  </td>
                  <td className="balance-cell">
                    {formatCurrency(transaction.balance)}
                  </td>
                  <td className="reference-cell">
                    {transaction.reference_number}
                  </td>
                  <td>
                    <span className={`status-badge ${transaction.status.toLowerCase()}`}>
                      {transaction.status}
                    </span>
                  </td>
                </tr>
              ))
            )}
          </tbody>
        </table>
      </div>

      <div className="table-footer">
        <p className="results-count">
          Showing {filteredAndSortedData.length} of {data.length} transactions
        </p>
      </div>
    </div>
  );
};

export default DataTable; 
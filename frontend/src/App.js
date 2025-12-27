import React, { useState } from 'react';
import './App.css';

function App() {
  const [isLogin, setIsLogin] = useState(true);
  const [formData, setFormData] = useState({});
  const [message, setMessage] = useState('');
  const [isLoggedIn, setIsLoggedIn] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      const loginData = { username: formData.username, password: formData.password };
      const registerData = formData;
      
      const url = isLogin ? '/api/login' : '/api/register';
      const data = isLogin ? loginData : registerData;
      
      const response = await fetch(`http://localhost:5000${url}`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        credentials: 'include',
        body: JSON.stringify(data)
      });
      const result = await response.json();
      setMessage(result.message);
      
      if (response.ok) {
        if (isLogin) {
          setIsLoggedIn(true);
          setMessage('Welcome to Dashboard! (Session active)');
        } else {
          setTimeout(() => {
            setIsLogin(true);
            setMessage('Registered! Please login');
          }, 1500);
        }
      }
    } catch (error) {
      setMessage('Network error');
    }
  };

  const handleChange = (e) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  if (isLoggedIn) {
    return (
      <div className="App">
        <div className="form-container">
          <h2>🏠 HOME DASHBOARD</h2>
          <p>✅ Logged in as: <strong>{formData.username}</strong></p>
          <p>🔐 Session active (10s timeout)</p>
          <button 
            onClick={() => {
              setIsLoggedIn(false);
              setIsLogin(true);
              setMessage('');
              setFormData({});
            }}
            style={{background: '#ff4757', color: 'white'}}
          >
            🚪 Logout
          </button>
        </div>
      </div>
    );
  }

  return (
    <div className="App">
      <div className="form-container">
        <h2>{isLogin ? '🔐 Login' : '📝 Register'}</h2>
        <form onSubmit={handleSubmit}>
          {!isLogin && (
            <>
              <input name="name" placeholder="Full Name" onChange={handleChange} required autoComplete="off" />
              <input name="email" type="email" placeholder="Email" onChange={handleChange} required autoComplete="off" />
            </>
          )}
          <input name="username" placeholder="Username" onChange={handleChange} required autoComplete="off" />
          <input name="password" type="password" placeholder="Password" onChange={handleChange} required autoComplete="off" />
          {!isLogin && (
            <>
              <input name="confirm_password" type="password" placeholder="Confirm Password" onChange={handleChange} required autoComplete="off" />
              <input name="phone" placeholder="Phone" onChange={handleChange} required autoComplete="off" />
            </>
          )}
          <button type="submit">{isLogin ? 'Login' : 'Register'}</button>
        </form>
        {message && <p style={{color: 'green'}}>{message}</p>}
        <p onClick={() => setIsLogin(!isLogin)} style={{cursor: 'pointer', color: '#667eea', textAlign: 'center'}}>
          {isLogin ? 'Need account? Register' : 'Have account? Login'}
        </p>
      </div>
    </div>
  );
}

export default App;

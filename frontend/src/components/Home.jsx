import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { useNavigate } from 'react-router-dom';

const Home = () => {
  const [user, setUser] = useState(null);
  const [message, setMessage] = useState('');
  const navigate = useNavigate();

  useEffect(() => {
    checkSession();
    const interval = setInterval(checkSession, 5000);
    return () => clearInterval(interval);
  }, []);

  const checkSession = async () => {
    try {
      const response = await axios.get('http://localhost:5000/api/check-session', 
        { withCredentials: true });
      if (!response.data.authenticated) {
        navigate('/login');
      } else {
        const homeResponse = await axios.get('http://localhost:5000/api/home', 
          { withCredentials: true });
        setUser(homeResponse.data.user);
      }
    } catch (error) {
      navigate('/login');
    }
  };

  const handleLogout = async () => {
    try {
      await axios.post('http://localhost:5000/api/logout', {}, { withCredentials: true });
      navigate('/login');
    } catch (error) {
      navigate('/login');
    }
  };

  return (
    <div className="home-container">
      <button onClick={handleLogout} className="logout-btn">Logout</button>
      <h2>Admin Dashboard</h2>
      {user ? (
        <div className="user-info">
          <h3>Welcome, {user.name}!</h3>
          <p><strong>Email:</strong> {user.email}</p>
          <p><strong>Phone:</strong> {user.phone}</p>
          <p><strong>Username:</strong> {user.username}</p>
          <p className="session-notice">🔄 Session active (10s inactivity timeout)</p>
        </div>
      ) : (
        <p>Loading user data...</p>
      )}
    </div>
  );
};

export default Home;

import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom'; // 👈 import this
import logo from '../img/logo.png';
import '../css/pages_styles.css';

const Admin_Login = () => {
    const [email, setEmail] = useState('');
    const [password, setPassword] = useState('');
    const [message, setMessage] = useState('');
    const [loading, setLoading] = useState(false);

    const navigate = useNavigate(); 

    const handleLogin = async () => {
        setLoading(true);
        setMessage('');

        await new Promise((resolve) => setTimeout(resolve, 800));

        const ADMIN_EMAIL = 'admin@gcuh.com';
        const ADMIN_PASSWORD = 'admin';

        if (email === ADMIN_EMAIL && password === ADMIN_PASSWORD) {
            setMessage('Login successful! Redirecting...');
            setTimeout(() => {
                navigate('/dashboard'); 
            }, 1200);
        } else {
            setMessage('Invalid email or password');
        }

        setLoading(false);
    };

    return (
        <>
            <div className="main-container">
                <header className="topbar">
                    <div className="logo-title">
                        <img src={logo} alt="Logo" className="logo" />
                        <h1 className="title">GC UNIVERSITY HYDERABAD</h1>
                    </div>
                </header>

                <div className="center-box">
                    <div className="login-card">
                        <h2 className="login-heading">Login to Dashboard</h2>
                        <div className="underline"></div>

                        <div className="inpt_area" id="inpt_area1">
                            <label className="label label_1">Your Email</label>
                            <input
                                className="input_text"
                                placeholder="Enter email"
                                value={email}
                                onChange={(e) => setEmail(e.target.value)}
                            />
                        </div>

                        <div className="inpt_area">
                            <label className="label_1">Your Password</label>
                            <input
                                type="password"
                                className="input_text"
                                placeholder="Enter password"
                                value={password}
                                onChange={(e) => setPassword(e.target.value)}
                            />
                        </div>

                        <div className="login-btn_area">
                            <button className="login-btn" onClick={handleLogin} disabled={loading}>
                                {loading ? 'Please wait...' : 'Login'}
                            </button>
                        </div>

                        {message && (
                            <p
                                style={{
                                    marginTop: '15px',
                                    textAlign: 'center',
                                    color: message.includes('') ? 'red' : 'green',
                                    fontWeight: 500,
                                }}
                            >
                                {message}
                            </p>
                        )}
                    </div>
                </div>

                <footer className="footer">
                    GC University Hyderabad, Kali Mori Hyderabad Sindh, Pakistan • Phone: 022-211995
                </footer>
            </div>
        </>
    );
};

export default Admin_Login;

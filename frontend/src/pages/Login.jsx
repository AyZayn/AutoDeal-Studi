import { useState } from "react";
import { useNavigate, Link } from "react-router-dom";
import { useAuth } from "../context/AuthContext";
import "./Auth.css";

function Login() {
    const navigate = useNavigate();
    const { login } = useAuth();
    const [form, setForm] = useState({ username: "", password: "" });
    const [error, setError] = useState("");

    const handleChange = (e) => setForm({ ...form, [e.target.name]: e.target.value });

    const handleSubmit = async (e) => {
        e.preventDefault();
        try {
            await login(form.username, form.password);
            navigate("/");
        } catch {
            setError("Identifiants incorrects");
        }
    };

    return (
        <div className="auth-page">
            <div className="auth-card">
                <h1 className="auth-title">Connexion</h1>
                <p className="auth-subtitle">Content de vous revoir !</p>
                {error && <p className="auth-error">{error}</p>}
                <form onSubmit={handleSubmit} className="auth-form">
                    <div className="auth-field">
                        <label>Nom d'utilisateur</label>
                        <input name="username" value={form.username} onChange={handleChange} required />
                    </div>
                    <div className="auth-field">
                        <label>Mot de passe</label>
                        <input name="password" type="password" value={form.password} onChange={handleChange} required />
                    </div>
                    <button type="submit" className="auth-btn">Se connecter</button>
                </form>
                <p className="auth-footer">Pas de compte ? <Link to="/register">S'inscrire</Link></p>
            </div>
        </div>
    );
}

export default Login;

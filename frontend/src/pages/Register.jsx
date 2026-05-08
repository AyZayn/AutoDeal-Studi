import { useState } from "react";
import { useNavigate, Link } from "react-router-dom";
import API from "../services/api";
import "./Auth.css";

function Register() {
    const navigate = useNavigate();
    const [form, setForm] = useState({ username: "", email: "", password: "", first_name: "", last_name: "", phone: "" });
    const [error, setError] = useState("");

    const handleChange = (e) => setForm({ ...form, [e.target.name]: e.target.value });

    const handleSubmit = async (e) => {
        e.preventDefault();
        try {
            await API.post("/register/", form);
            navigate("/login");
        } catch {
            setError("Erreur lors de l inscription");
        }
    };

    return (
        <div className="auth-page">
            <div className="auth-card">
                <h1 className="auth-title">Inscription</h1>
                <p className="auth-subtitle">Rejoignez AutoDeal</p>
                {error && <p className="auth-error">{error}</p>}
                <form onSubmit={handleSubmit} className="auth-form">
                    {[
                        { name: "first_name", label: "Prenom" },
                        { name: "last_name", label: "Nom" },
                        { name: "username", label: "Nom d utilisateur" },
                        { name: "email", label: "Email", type: "email" },
                        { name: "phone", label: "Telephone" },
                        { name: "password", label: "Mot de passe", type: "password" },
                    ].map((field) => (
                        <div key={field.name} className="auth-field">
                            <label>{field.label}</label>
                            <input name={field.name} type={field.type || "text"} value={form[field.name]} onChange={handleChange} required />
                        </div>
                    ))}
                    <button type="submit" className="auth-btn">Creer mon compte</button>
                </form>
                <p className="auth-footer">Deja un compte ? <Link to="/login">Se connecter</Link></p>
            </div>
        </div>
    );
}

export default Register;

import { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import API from "../services/api";
import { useAuth } from "../context/AuthContext";
import "./Profile.css";

function Profile() {
    const { token, logout } = useAuth();
    const navigate = useNavigate();
    const [user, setUser] = useState(null);
    const [form, setForm] = useState({});
    const [loading, setLoading] = useState(true);
    const [editing, setEditing] = useState(false);
    const [success, setSuccess] = useState(false);
    const [error, setError] = useState("");
    const [stats, setStats] = useState({ total: 0, sales: 0, rents: 0 });

    useEffect(() => {
        if (!token) { navigate("/login"); return; }
        Promise.all([
            API.get("/profile/"),
            API.get("/contracts/")
        ]).then(([profileRes, contractsRes]) => {
            setUser(profileRes.data);
            setForm(profileRes.data);
            const contracts = contractsRes.data;
            setStats({
                total: contracts.length,
                sales: contracts.filter(c => c.contract_type === "sale").length,
                rents: contracts.filter(c => c.contract_type === "rent").length,
            });
            setLoading(false);
        }).catch(() => setLoading(false));
    }, [token]);

    const handleChange = (e) => setForm({ ...form, [e.target.name]: e.target.value });

    const handleSubmit = async (e) => {
        e.preventDefault();
        try {
            const res = await API.patch("/profile/update/", {
                first_name: form.first_name,
                last_name: form.last_name,
                email: form.email,
                phone: form.phone,
                address: form.address,
                city: form.city,
            });
            setUser(res.data);
            setEditing(false);
            setSuccess(true);
            setTimeout(() => setSuccess(false), 3000);
        } catch {
            setError("Erreur lors de la mise a jour");
            setTimeout(() => setError(""), 3000);
        }
    };

    const handleLogout = () => {
        logout();
        navigate("/");
    };

    if (loading) return <div className="page-loading">Chargement...</div>;

    const initials = ((user?.first_name?.[0] || "") + (user?.last_name?.[0] || "")).toUpperCase() || user?.username?.[0]?.toUpperCase() || "U";

    return (
        <div className="profile-page">
            <div className="profile-container">
                <div className="profile-sidebar">
                    <div className="profile-avatar">{initials}</div>
                    <h2 className="profile-name">{user?.first_name} {user?.last_name}</h2>
                    <p className="profile-username">@{user?.username}</p>
                    <span className="profile-role">{user?.role === "admin" ? "Administrateur" : "Client"}</span>
                    <div className="profile-stats">
                        <div className="profile-stat">
                            <span className="profile-stat-number">{stats.total}</span>
                            <span className="profile-stat-label">Contrats</span>
                        </div>
                        <div className="profile-stat-divider"></div>
                        <div className="profile-stat">
                            <span className="profile-stat-number">{stats.sales}</span>
                            <span className="profile-stat-label">Achats</span>
                        </div>
                        <div className="profile-stat-divider"></div>
                        <div className="profile-stat">
                            <span className="profile-stat-number">{stats.rents}</span>
                            <span className="profile-stat-label">Locations</span>
                        </div>
                    </div>
                    <button onClick={() => navigate("/contracts")} className="profile-sidebar-btn">Voir mes contrats</button>
                    <button onClick={handleLogout} className="profile-logout-btn">Deconnexion</button>
                </div>

                <div className="profile-main">
                    <div className="profile-main-header">
                        <h1>Mon Profil</h1>
                        {!editing && (
                            <button onClick={() => setEditing(true)} className="profile-edit-btn">Modifier</button>
                        )}
                    </div>

                    {success && <div className="profile-success">Profil mis a jour avec succes !</div>}
                    {error && <div className="profile-error">{error}</div>}

                    {editing ? (
                        <form onSubmit={handleSubmit} className="profile-form">
                            <div className="profile-form-grid">
                                {[
                                    { name: "first_name", label: "Prenom" },
                                    { name: "last_name", label: "Nom" },
                                    { name: "email", label: "Email", type: "email" },
                                    { name: "phone", label: "Telephone" },
                                    { name: "city", label: "Ville" },
                                ].map((field) => (
                                    <div key={field.name} className="profile-field">
                                        <label>{field.label}</label>
                                        <input
                                            name={field.name}
                                            type={field.type || "text"}
                                            value={form[field.name] || ""}
                                            onChange={handleChange}
                                        />
                                    </div>
                                ))}
                                <div className="profile-field profile-field-full">
                                    <label>Adresse</label>
                                    <input name="address" value={form.address || ""} onChange={handleChange} />
                                </div>
                            </div>
                            <div className="profile-form-actions">
                                <button type="submit" className="profile-save-btn">Sauvegarder</button>
                                <button type="button" onClick={() => { setEditing(false); setForm(user); }} className="profile-cancel-btn">Annuler</button>
                            </div>
                        </form>
                    ) : (
                        <div className="profile-info-grid">
                            {[
                                { label: "Prenom", value: user?.first_name || "Non renseigne" },
                                { label: "Nom", value: user?.last_name || "Non renseigne" },
                                { label: "Email", value: user?.email || "Non renseigne" },
                                { label: "Telephone", value: user?.phone || "Non renseigne" },
                                { label: "Ville", value: user?.city || "Non renseignee" },
                                { label: "Adresse", value: user?.address || "Non renseignee" },
                            ].map((item) => (
                                <div key={item.label} className="profile-info-item">
                                    <span className="profile-info-label">{item.label}</span>
                                    <span className="profile-info-value">{item.value}</span>
                                </div>
                            ))}
                        </div>
                    )}
                </div>
            </div>
        </div>
    );
}

export default Profile;

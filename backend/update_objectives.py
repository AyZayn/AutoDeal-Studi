import os

base = os.path.join("..", "frontend", "src")

files = {}

files[os.path.join(base, "pages", "VehicleDetail.jsx")] = """import { useState, useEffect } from "react";
import { useParams, useNavigate } from "react-router-dom";
import API from "../services/api";
import { useAuth } from "../context/AuthContext";

function VehicleDetail() {
    const { id } = useParams();
    const navigate = useNavigate();
    const { token } = useAuth();
    const [vehicle, setVehicle] = useState(null);
    const [loading, setLoading] = useState(true);

    const fuelLabels = {
        gasoline: "Essence",
        diesel: "Diesel",
        electric: "Electrique",
        hybrid: "Hybride",
    };

    const transmissionLabels = {
        manual: "Manuelle",
        automatic: "Automatique",
    };

    useEffect(() => {
        API.get("/vehicles/" + id + "/")
            .then((res) => { setVehicle(res.data); setLoading(false); })
            .catch(() => setLoading(false));
    }, [id]);

    const handleDossier = (type) => {
        if (!token) {
            navigate("/register", { state: { message: "Inscrivez-vous pour deposer votre dossier", vehicleId: id, type } });
            return;
        }
        navigate("/dossier/new", { state: { vehicle, type } });
    };

    if (loading) return <div className="page-loading">Chargement...</div>;
    if (!vehicle) return <div className="page-loading">Vehicule introuvable</div>;

    return (
        <div className="vehicle-detail-page">
            <div className="vehicle-detail-container">
                <button onClick={() => navigate(-1)} className="back-btn">← Retour</button>
                <div className="vehicle-detail-card">
                    <div className="vehicle-detail-image">
                        {vehicle.image
                            ? <img src={vehicle.image} alt={vehicle.brand} />
                            : <div className="no-image">Pas de photo</div>}
                        <span className={"offer-badge " + vehicle.offer_type}>
                            {vehicle.offer_type === "sale" ? "Vente" : vehicle.offer_type === "rent" ? "Location" : "Vente & Location"}
                        </span>
                    </div>
                    <div className="vehicle-detail-info">
                        <h1>{vehicle.brand} {vehicle.model} <span>({vehicle.year})</span></h1>
                        <div className="vehicle-detail-grid">
                            {[
                                { label: "Kilometrage", value: vehicle.mileage + " km" },
                                { label: "Carburant", value: fuelLabels[vehicle.fuel] || vehicle.fuel },
                                { label: "Transmission", value: transmissionLabels[vehicle.transmission] || vehicle.transmission },
                                { label: "Places", value: vehicle.seats },
                                { label: "Couleur", value: vehicle.color },
                                { label: "Disponible", value: vehicle.is_available ? "Oui" : "Non" },
                            ].map((item) => (
                                <div key={item.label} className="vehicle-detail-item">
                                    <span className="vehicle-detail-label">{item.label}</span>
                                    <span className="vehicle-detail-value">{item.value}</span>
                                </div>
                            ))}
                        </div>
                        {vehicle.description && <p className="vehicle-detail-description">{vehicle.description}</p>}

                        {!token && (
                            <div className="vehicle-detail-cta">
                                <p className="vehicle-detail-cta-text">
                                    Vous etes interesse par ce vehicule ?
                                </p>
                                <p className="vehicle-detail-cta-sub">
                                    Inscrivez-vous ou connectez-vous pour deposer votre dossier d achat ou de location.
                                </p>
                                <div className="vehicle-detail-cta-actions">
                                    <button onClick={() => navigate("/register")} className="cta-btn-primary">
                                        Creer un compte
                                    </button>
                                    <button onClick={() => navigate("/login")} className="cta-btn-secondary">
                                        Se connecter
                                    </button>
                                </div>
                            </div>
                        )}

                        {token && (
                            <div className="vehicle-detail-actions">
                                {(vehicle.offer_type === "sale" || vehicle.offer_type === "both") && vehicle.sale_price && (
                                    <button onClick={() => handleDossier("sale")} className="btn-buy">
                                        Deposer un dossier d achat — {Number(vehicle.sale_price).toLocaleString("fr-FR")} EUR
                                    </button>
                                )}
                                {(vehicle.offer_type === "rent" || vehicle.offer_type === "both") && vehicle.rent_price && (
                                    <button onClick={() => handleDossier("rent")} className="btn-rent">
                                        Deposer un dossier de location — {Number(vehicle.rent_price).toLocaleString("fr-FR")} EUR/jour
                                    </button>
                                )}
                            </div>
                        )}
                    </div>
                </div>
            </div>
        </div>
    );
}

export default VehicleDetail;
"""

files[os.path.join(base, "pages", "VehicleDetail.css")] = """.vehicle-detail-page {
    min-height: calc(100vh - 68px);
    padding: 48px;
    background: #0a0a0f;
}

.vehicle-detail-container {
    max-width: 1000px;
    margin: 0 auto;
}

.back-btn {
    background: transparent;
    border: none;
    color: #6b7280;
    font-size: 15px;
    cursor: pointer;
    margin-bottom: 24px;
    padding: 0;
    transition: color 0.2s;
}

.back-btn:hover {
    color: white;
}

.vehicle-detail-card {
    background: rgba(255,255,255,0.03);
    border: 1px solid rgba(255,255,255,0.07);
    border-radius: 20px;
    overflow: hidden;
}

.vehicle-detail-image {
    position: relative;
    height: 380px;
    background: rgba(255,255,255,0.03);
    overflow: hidden;
}

.vehicle-detail-image img {
    width: 100%;
    height: 100%;
    object-fit: cover;
}

.vehicle-detail-image .no-image {
    height: 100%;
    display: flex;
    align-items: center;
    justify-content: center;
    color: #374151;
    font-size: 16px;
}

.vehicle-detail-image .offer-badge {
    position: absolute;
    top: 16px;
    left: 16px;
    padding: 6px 14px;
    border-radius: 8px;
    font-size: 12px;
    font-weight: 700;
    letter-spacing: 0.5px;
    text-transform: uppercase;
}

.offer-badge.sale { background: rgba(230,57,70,0.9); color: white; }
.offer-badge.rent { background: rgba(59,130,246,0.9); color: white; }
.offer-badge.both { background: rgba(139,92,246,0.9); color: white; }

.vehicle-detail-info {
    padding: 40px;
}

.vehicle-detail-info h1 {
    font-size: 30px;
    font-weight: 800;
    color: white;
    letter-spacing: -0.5px;
    margin-bottom: 28px;
}

.vehicle-detail-info h1 span {
    color: #6b7280;
    font-weight: 400;
    font-size: 22px;
}

.vehicle-detail-grid {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 12px;
    margin-bottom: 28px;
}

.vehicle-detail-item {
    background: rgba(255,255,255,0.03);
    border: 1px solid rgba(255,255,255,0.06);
    border-radius: 12px;
    padding: 14px 16px;
    display: flex;
    flex-direction: column;
    gap: 4px;
}

.vehicle-detail-label {
    font-size: 11px;
    color: #6b7280;
    text-transform: uppercase;
    letter-spacing: 0.5px;
    font-weight: 500;
}

.vehicle-detail-value {
    font-size: 15px;
    color: white;
    font-weight: 600;
}

.vehicle-detail-description {
    color: #9ca3af;
    line-height: 1.7;
    margin-bottom: 28px;
    font-size: 15px;
}

.vehicle-detail-cta {
    background: rgba(230,57,70,0.06);
    border: 1px solid rgba(230,57,70,0.15);
    border-radius: 16px;
    padding: 28px;
    text-align: center;
}

.vehicle-detail-cta-text {
    font-size: 18px;
    font-weight: 700;
    color: white;
    margin-bottom: 8px;
}

.vehicle-detail-cta-sub {
    color: #9ca3af;
    font-size: 14px;
    margin-bottom: 24px;
    line-height: 1.6;
}

.vehicle-detail-cta-actions {
    display: flex;
    gap: 12px;
    justify-content: center;
}

.cta-btn-primary {
    background: #e63946;
    color: white;
    border: none;
    padding: 12px 28px;
    border-radius: 10px;
    font-size: 15px;
    font-weight: 600;
    cursor: pointer;
    transition: background 0.2s;
}

.cta-btn-primary:hover {
    background: #c1121f;
}

.cta-btn-secondary {
    background: transparent;
    color: #d1d5db;
    border: 1px solid rgba(255,255,255,0.1);
    padding: 12px 28px;
    border-radius: 10px;
    font-size: 15px;
    font-weight: 500;
    cursor: pointer;
    transition: all 0.2s;
}

.cta-btn-secondary:hover {
    color: white;
    border-color: rgba(255,255,255,0.3);
}

.vehicle-detail-actions {
    display: flex;
    flex-direction: column;
    gap: 12px;
}

.btn-buy {
    width: 100%;
    background: #e63946;
    color: white;
    border: none;
    padding: 16px;
    border-radius: 12px;
    font-size: 16px;
    font-weight: 600;
    cursor: pointer;
    transition: background 0.2s, transform 0.1s;
}

.btn-buy:hover {
    background: #c1121f;
    transform: translateY(-1px);
}

.btn-rent {
    width: 100%;
    background: rgba(59,130,246,0.1);
    color: #3b82f6;
    border: 1px solid rgba(59,130,246,0.3);
    padding: 16px;
    border-radius: 12px;
    font-size: 16px;
    font-weight: 600;
    cursor: pointer;
    transition: all 0.2s;
}

.btn-rent:hover {
    background: rgba(59,130,246,0.2);
    transform: translateY(-1px);
}
"""

files[os.path.join(base, "pages", "NewDossier.jsx")] = """import { useState } from "react";
import { useLocation, useNavigate } from "react-router-dom";
import API from "../services/api";
import "./NewDossier.css";

function NewDossier() {
    const { state } = useLocation();
    const navigate = useNavigate();
    const vehicle = state?.vehicle;
    const type = state?.type;
    const [startDate, setStartDate] = useState("");
    const [endDate, setEndDate] = useState("");
    const [notes, setNotes] = useState("");
    const [error, setError] = useState("");
    const [success, setSuccess] = useState(false);

    if (!vehicle) { navigate("/vehicles"); return null; }

    const calculateTotal = () => {
        if (type === "sale") return Number(vehicle.sale_price);
        if (!startDate || !endDate) return 0;
        const days = Math.ceil((new Date(endDate) - new Date(startDate)) / (1000 * 60 * 60 * 24));
        return days > 0 ? (days * vehicle.rent_price).toFixed(2) : 0;
    };

    const handleSubmit = async (e) => {
        e.preventDefault();
        try {
            await API.post("/contracts/", {
                vehicle: vehicle.id,
                contract_type: type,
                start_date: startDate,
                end_date: type === "rent" ? endDate : null,
                total_price: calculateTotal(),
                notes: notes,
            });
            setSuccess(true);
            setTimeout(() => navigate("/dossiers"), 2000);
        } catch {
            setError("Erreur lors du depot du dossier");
        }
    };

    return (
        <div className="dossier-page">
            <div className="dossier-container">
                <button onClick={() => navigate(-1)} className="back-btn-d">← Retour</button>
                <h1 className="dossier-title">
                    Dossier de {type === "sale" ? "demande d achat" : "demande de location"}
                </h1>

                {success && <div className="dossier-success">Dossier depose avec succes ! Redirection...</div>}
                {error && <div className="dossier-error">{error}</div>}

                <div className="dossier-vehicle-recap">
                    <div className="dossier-vehicle-image">
                        {vehicle.image
                            ? <img src={vehicle.image} alt={vehicle.brand} />
                            : <div className="dossier-no-image">Pas de photo</div>}
                    </div>
                    <div className="dossier-vehicle-info">
                        <h2>{vehicle.brand} {vehicle.model} ({vehicle.year})</h2>
                        <p>{vehicle.mileage} km</p>
                        <p className="dossier-price">
                            {type === "sale"
                                ? Number(vehicle.sale_price).toLocaleString("fr-FR") + " EUR"
                                : Number(vehicle.rent_price).toLocaleString("fr-FR") + " EUR/jour"}
                        </p>
                    </div>
                </div>

                <div className="dossier-form-card">
                    <h3>Informations du dossier</h3>
                    <form onSubmit={handleSubmit} className="dossier-form">
                        <div className="dossier-form-row">
                            <div className="dossier-field">
                                <label>{type === "sale" ? "Date d achat souhaitee" : "Date de debut"}</label>
                                <input type="date" value={startDate} onChange={(e) => setStartDate(e.target.value)} required />
                            </div>
                            {type === "rent" && (
                                <div className="dossier-field">
                                    <label>Date de fin</label>
                                    <input type="date" value={endDate} onChange={(e) => setEndDate(e.target.value)} required />
                                </div>
                            )}
                        </div>
                        <div className="dossier-field">
                            <label>Message ou informations complementaires (optionnel)</label>
                            <textarea
                                value={notes}
                                onChange={(e) => setNotes(e.target.value)}
                                placeholder="Ex: Je suis disponible le matin, j ai deja un financement..."
                                rows={4}
                            />
                        </div>
                        {calculateTotal() > 0 && (
                            <div className="dossier-total">
                                <span>Total estimé</span>
                                <span className="dossier-total-price">
                                    {Number(calculateTotal()).toLocaleString("fr-FR")} EUR
                                    {type === "rent" && " (total location)"}
                                </span>
                            </div>
                        )}
                        <button type="submit" className="dossier-submit-btn">
                            Deposer mon dossier
                        </button>
                    </form>
                </div>
            </div>
        </div>
    );
}

export default NewDossier;
"""

files[os.path.join(base, "pages", "NewDossier.css")] = """.dossier-page {
    min-height: calc(100vh - 68px);
    padding: 48px;
    background: #0a0a0f;
}

.dossier-container {
    max-width: 700px;
    margin: 0 auto;
}

.back-btn-d {
    background: transparent;
    border: none;
    color: #6b7280;
    font-size: 15px;
    cursor: pointer;
    margin-bottom: 24px;
    padding: 0;
    transition: color 0.2s;
}

.back-btn-d:hover { color: white; }

.dossier-title {
    font-size: 28px;
    font-weight: 800;
    color: white;
    letter-spacing: -0.5px;
    margin-bottom: 32px;
    text-transform: capitalize;
}

.dossier-success {
    background: rgba(34,197,94,0.1);
    border: 1px solid rgba(34,197,94,0.2);
    color: #22c55e;
    padding: 14px 18px;
    border-radius: 10px;
    margin-bottom: 24px;
    font-size: 14px;
}

.dossier-error {
    background: rgba(230,57,70,0.1);
    border: 1px solid rgba(230,57,70,0.2);
    color: #e63946;
    padding: 14px 18px;
    border-radius: 10px;
    margin-bottom: 24px;
    font-size: 14px;
}

.dossier-vehicle-recap {
    display: flex;
    gap: 20px;
    background: rgba(255,255,255,0.03);
    border: 1px solid rgba(255,255,255,0.07);
    border-radius: 16px;
    padding: 20px;
    margin-bottom: 24px;
    align-items: center;
}

.dossier-vehicle-image {
    width: 120px;
    height: 80px;
    border-radius: 10px;
    overflow: hidden;
    background: rgba(255,255,255,0.05);
    flex-shrink: 0;
}

.dossier-vehicle-image img {
    width: 100%;
    height: 100%;
    object-fit: cover;
}

.dossier-no-image {
    width: 100%;
    height: 100%;
    display: flex;
    align-items: center;
    justify-content: center;
    color: #374151;
    font-size: 12px;
}

.dossier-vehicle-info h2 {
    font-size: 17px;
    font-weight: 700;
    color: white;
    margin-bottom: 4px;
}

.dossier-vehicle-info p {
    font-size: 13px;
    color: #6b7280;
    margin-bottom: 4px;
}

.dossier-price {
    color: #e63946 !important;
    font-weight: 700 !important;
    font-size: 16px !important;
}

.dossier-form-card {
    background: rgba(255,255,255,0.03);
    border: 1px solid rgba(255,255,255,0.07);
    border-radius: 16px;
    padding: 32px;
}

.dossier-form-card h3 {
    font-size: 18px;
    font-weight: 700;
    color: white;
    margin-bottom: 24px;
}

.dossier-form {
    display: flex;
    flex-direction: column;
    gap: 20px;
}

.dossier-form-row {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 16px;
}

.dossier-field label {
    display: block;
    color: #9ca3af;
    font-size: 13px;
    font-weight: 500;
    margin-bottom: 8px;
    text-transform: uppercase;
    letter-spacing: 0.5px;
}

.dossier-field input,
.dossier-field textarea {
    width: 100%;
    background: rgba(255,255,255,0.04);
    border: 1px solid rgba(255,255,255,0.08);
    color: white;
    padding: 12px 16px;
    border-radius: 10px;
    font-size: 15px;
    outline: none;
    transition: border 0.2s;
    box-sizing: border-box;
    font-family: inherit;
    resize: vertical;
}

.dossier-field input:focus,
.dossier-field textarea:focus {
    border-color: #e63946;
}

.dossier-total {
    display: flex;
    justify-content: space-between;
    align-items: center;
    background: rgba(230,57,70,0.06);
    border: 1px solid rgba(230,57,70,0.15);
    padding: 16px 20px;
    border-radius: 12px;
}

.dossier-total span {
    color: #9ca3af;
    font-size: 15px;
}

.dossier-total-price {
    color: #e63946 !important;
    font-weight: 700 !important;
    font-size: 22px !important;
}

.dossier-submit-btn {
    background: #e63946;
    color: white;
    border: none;
    padding: 16px;
    border-radius: 12px;
    font-size: 16px;
    font-weight: 600;
    cursor: pointer;
    transition: background 0.2s, transform 0.1s;
    width: 100%;
}

.dossier-submit-btn:hover {
    background: #c1121f;
    transform: translateY(-1px);
}
"""

files[os.path.join(base, "pages", "Dossiers.jsx")] = """import { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import API from "../services/api";
import { useAuth } from "../context/AuthContext";
import "./Dossiers.css";

function Dossiers() {
    const [dossiers, setDossiers] = useState([]);
    const [loading, setLoading] = useState(true);
    const [deleting, setDeleting] = useState(null);
    const { token } = useAuth();
    const navigate = useNavigate();

    useEffect(() => {
        if (!token) { navigate("/login"); return; }
        fetchDossiers();
    }, [token]);

    const fetchDossiers = () => {
        API.get("/contracts/")
            .then((res) => { setDossiers(res.data); setLoading(false); })
            .catch(() => setLoading(false));
    };

    const handleDelete = async (id) => {
        if (!window.confirm("Voulez-vous vraiment annuler ce dossier ?")) return;
        setDeleting(id);
        try {
            await API.delete("/contracts/" + id + "/");
            setDossiers(dossiers.filter(c => c.id !== id));
        } catch {
            alert("Erreur lors de l annulation");
        }
        setDeleting(null);
    };

    const statusConfig = {
        pending:   { label: "En attente",  color: "pending" },
        confirmed: { label: "Confirme",    color: "confirmed" },
        active:    { label: "En cours",    color: "active" },
        completed: { label: "Termine",     color: "completed" },
        cancelled: { label: "Annule",      color: "cancelled" },
    };

    if (loading) return <div className="page-loading">Chargement...</div>;

    return (
        <div className="dossiers-page">
            <div className="dossiers-header">
                <h1>Mes <span>Dossiers</span></h1>
                <p>Suivez vos demandes d achat et de location</p>
            </div>
            {dossiers.length === 0 ? (
                <div className="dossiers-empty">
                    <p>Vous n avez pas encore de dossiers</p>
                    <button onClick={() => navigate("/vehicles")} className="dossiers-browse-btn">
                        Voir les vehicules
                    </button>
                </div>
            ) : (
                <div className="dossiers-list">
                    {dossiers.map((dossier) => {
                        const status = statusConfig[dossier.status] || { label: dossier.status, color: "pending" };
                        const canDelete = dossier.status === "pending";
                        return (
                            <div key={dossier.id} className="dossier-card">
                                <div className="dossier-card-header">
                                    <div className="dossier-card-header-left">
                                        <span className="dossier-type">
                                            {dossier.contract_type === "sale" ? "Demande d achat" : "Demande de location"}
                                        </span>
                                        <span className={"dossier-status " + status.color}>
                                            {status.label}
                                        </span>
                                    </div>
                                    {canDelete && (
                                        <button
                                            onClick={() => handleDelete(dossier.id)}
                                            disabled={deleting === dossier.id}
                                            className="dossier-delete-btn"
                                        >
                                            {deleting === dossier.id ? "Annulation..." : "Annuler le dossier"}
                                        </button>
                                    )}
                                </div>
                                <div className="dossier-card-body">
                                    {dossier.vehicle_detail && (
                                        <div className="dossier-card-vehicle">
                                            {dossier.vehicle_detail.image && (
                                                <img src={dossier.vehicle_detail.image} alt={dossier.vehicle_detail.brand} />
                                            )}
                                            <div>
                                                <h2>{dossier.vehicle_detail.brand} {dossier.vehicle_detail.model} ({dossier.vehicle_detail.year})</h2>
                                                <p>{dossier.vehicle_detail.mileage} km</p>
                                            </div>
                                        </div>
                                    )}
                                    <div className="dossier-card-details">
                                        <div className="dossier-detail-item">
                                            <span>Date de debut</span>
                                            <span>{dossier.start_date}</span>
                                        </div>
                                        {dossier.end_date && (
                                            <div className="dossier-detail-item">
                                                <span>Date de fin</span>
                                                <span>{dossier.end_date}</span>
                                            </div>
                                        )}
                                        <div className="dossier-detail-item">
                                            <span>Montant total</span>
                                            <span className="dossier-card-price">{Number(dossier.total_price).toLocaleString("fr-FR")} EUR</span>
                                        </div>
                                    </div>
                                    {dossier.notes && (
                                        <p className="dossier-card-notes">"{dossier.notes}"</p>
                                    )}
                                </div>
                            </div>
                        );
                    })}
                </div>
            )}
        </div>
    );
}

export default Dossiers;
"""

files[os.path.join(base, "pages", "Dossiers.css")] = """.dossiers-page {
    min-height: calc(100vh - 68px);
    padding: 60px 48px;
    max-width: 900px;
    margin: 0 auto;
}

.dossiers-header {
    text-align: center;
    margin-bottom: 48px;
}

.dossiers-header h1 {
    font-size: 42px;
    font-weight: 800;
    letter-spacing: -1.5px;
    color: white;
    margin-bottom: 8px;
}

.dossiers-header h1 span { color: #e63946; }

.dossiers-header p {
    color: #6b7280;
    font-size: 16px;
}

.dossiers-empty {
    text-align: center;
    padding: 80px 24px;
}

.dossiers-empty p {
    color: #6b7280;
    font-size: 18px;
    margin-bottom: 24px;
}

.dossiers-browse-btn {
    background: #e63946;
    color: white;
    border: none;
    padding: 12px 28px;
    border-radius: 10px;
    font-size: 15px;
    font-weight: 600;
    cursor: pointer;
    transition: background 0.2s;
}

.dossiers-browse-btn:hover { background: #c1121f; }

.dossiers-list {
    display: flex;
    flex-direction: column;
    gap: 20px;
}

.dossier-card {
    background: rgba(255,255,255,0.03);
    border: 1px solid rgba(255,255,255,0.07);
    border-radius: 16px;
    overflow: hidden;
    transition: border-color 0.2s;
}

.dossier-card:hover { border-color: rgba(255,255,255,0.12); }

.dossier-card-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 16px 24px;
    background: rgba(255,255,255,0.02);
    border-bottom: 1px solid rgba(255,255,255,0.05);
}

.dossier-card-header-left {
    display: flex;
    align-items: center;
    gap: 12px;
}

.dossier-type {
    color: white;
    font-weight: 600;
    font-size: 15px;
}

.dossier-status {
    padding: 4px 12px;
    border-radius: 99px;
    font-size: 12px;
    font-weight: 600;
}

.dossier-status.pending   { background: rgba(234,179,8,0.15);   color: #eab308; }
.dossier-status.confirmed { background: rgba(59,130,246,0.15);  color: #3b82f6; }
.dossier-status.active    { background: rgba(34,197,94,0.15);   color: #22c55e; }
.dossier-status.completed { background: rgba(156,163,175,0.15); color: #9ca3af; }
.dossier-status.cancelled { background: rgba(230,57,70,0.15);   color: #e63946; }

.dossier-delete-btn {
    background: transparent;
    border: 1px solid rgba(230,57,70,0.3);
    color: #e63946;
    padding: 7px 16px;
    border-radius: 8px;
    font-size: 13px;
    font-weight: 500;
    cursor: pointer;
    transition: all 0.2s;
}

.dossier-delete-btn:hover {
    background: rgba(230,57,70,0.1);
    border-color: #e63946;
}

.dossier-delete-btn:disabled {
    opacity: 0.5;
    cursor: not-allowed;
}

.dossier-card-body { padding: 24px; }

.dossier-card-vehicle {
    display: flex;
    align-items: center;
    gap: 16px;
    margin-bottom: 20px;
}

.dossier-card-vehicle img {
    width: 100px;
    height: 68px;
    object-fit: cover;
    border-radius: 8px;
}

.dossier-card-vehicle h2 {
    font-size: 17px;
    font-weight: 700;
    color: white;
    margin-bottom: 4px;
}

.dossier-card-vehicle p {
    font-size: 13px;
    color: #6b7280;
}

.dossier-card-details {
    display: flex;
    flex-direction: column;
    gap: 8px;
    background: rgba(255,255,255,0.02);
    border-radius: 10px;
    padding: 16px;
}

.dossier-detail-item {
    display: flex;
    justify-content: space-between;
    align-items: center;
}

.dossier-detail-item span:first-child {
    color: #6b7280;
    font-size: 14px;
}

.dossier-detail-item span:last-child {
    color: white;
    font-size: 14px;
    font-weight: 500;
}

.dossier-card-price {
    color: #e63946 !important;
    font-weight: 700 !important;
    font-size: 16px !important;
}

.dossier-card-notes {
    color: #9ca3af;
    font-size: 14px;
    font-style: italic;
    margin-top: 16px;
    padding-top: 16px;
    border-top: 1px solid rgba(255,255,255,0.05);
}
"""

files[os.path.join(base, "components", "Navbar.jsx")] = """import { Link, useNavigate } from "react-router-dom";
import { useAuth } from "../context/AuthContext";
import "./Navbar.css";

function Navbar() {
    const { token, logout } = useAuth();
    const navigate = useNavigate();

    const handleLogout = () => {
        logout();
        navigate("/");
    };

    return (
        <nav className="navbar">
            <Link to="/" className="navbar-brand">
                Auto<span>Deal</span>
            </Link>
            <div className="navbar-links">
                <Link to="/vehicles" className="nav-link">Vehicules</Link>
                {token ? (
                    <>
                        <Link to="/dossiers" className="nav-link">Mes Dossiers</Link>
                        <Link to="/profile" className="nav-link">Mon Profil</Link>
                        <button onClick={handleLogout} className="btn-danger">Deconnexion</button>
                    </>
                ) : (
                    <>
                        <Link to="/login" className="nav-link">Connexion</Link>
                        <Link to="/register" className="btn-primary">Inscription</Link>
                    </>
                )}
            </div>
        </nav>
    );
}

export default Navbar;
"""

files[os.path.join(base, "App.jsx")] = """import { BrowserRouter, Routes, Route } from "react-router-dom";
import { AuthProvider } from "./context/AuthContext";
import Navbar from "./components/Navbar";
import Home from "./pages/Home";
import VehicleList from "./pages/VehicleList";
import VehicleDetail from "./pages/VehicleDetail";
import Login from "./pages/Login";
import Register from "./pages/Register";
import Dossiers from "./pages/Dossiers";
import NewDossier from "./pages/NewDossier";
import Profile from "./pages/Profile";

function App() {
    return (
        <AuthProvider>
            <BrowserRouter>
                <Navbar />
                <Routes>
                    <Route path="/" element={<Home />} />
                    <Route path="/vehicles" element={<VehicleList />} />
                    <Route path="/vehicles/:id" element={<VehicleDetail />} />
                    <Route path="/login" element={<Login />} />
                    <Route path="/register" element={<Register />} />
                    <Route path="/dossiers" element={<Dossiers />} />
                    <Route path="/dossier/new" element={<NewDossier />} />
                    <Route path="/profile" element={<Profile />} />
                </Routes>
            </BrowserRouter>
        </AuthProvider>
    );
}

export default App;
"""

for filepath, content in files.items():
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(content)
    print("OK " + filepath)

print("")
print("Mise a jour des objectifs terminee avec succes !")
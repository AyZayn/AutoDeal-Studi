import { useState } from "react";
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

import { useState, useEffect } from "react";
import { useParams, useNavigate } from "react-router-dom";
import API from "../services/api";
import { useAuth } from "../context/AuthContext";
import RentalOptions from "../components/RentalOptions";
import "./VehicleDetail.css";

function VehicleDetail() {
    const { id } = useParams();
    const navigate = useNavigate();
    const { token } = useAuth();
    const [vehicle, setVehicle] = useState(null);
    const [loading, setLoading] = useState(true);
    const [rentalOptions, setRentalOptions] = useState([]);

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
        API.get("/rental-options/")
            .then((res) => setRentalOptions(res.data))
            .catch(() => {});
    }, [id]);

    const handleDossier = (type) => {
        if (!token) {
            navigate("/register");
            return;
        }
        navigate("/dossier/new", { state: { vehicle, type } });
    };

    if (loading) return <div className="page-loading">Chargement...</div>;
    if (!vehicle) return <div className="page-loading">Vehicule introuvable</div>;

    const isRent = vehicle.offer_type === "rent" || vehicle.offer_type === "both";

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

                        {vehicle.description && (
                            <p className="vehicle-detail-description">{vehicle.description}</p>
                        )}

                        {rentalOptions.length > 0 && (
                            <RentalOptions
                                options={rentalOptions}
                                selectedOptions={[]}
                                onToggle={() => {}}
                                readOnly={true}
                                offerType={vehicle.offer_type} // "sale", "rent" ou "both"
                            />
                        )}

                        {!token && (
                            <div className="vehicle-detail-cta">
                                <p className="vehicle-detail-cta-text">
                                    Vous êtes interessé par ce vehicule ?
                                </p>
                                <p className="vehicle-detail-cta-sub">
                                    Inscrivez-vous ou connectez-vous pour déposer votre dossier.
                                </p>
                                <div className="vehicle-detail-cta-actions">
                                    <button onClick={() => navigate("/register")} className="cta-btn-primary">
                                        Créer un compte
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
                                        Déposer un dossier d'achat — {Number(vehicle.sale_price).toLocaleString("fr-FR")} EUR
                                    </button>
                                )}
                                {(vehicle.offer_type === "rent" || vehicle.offer_type === "both") && vehicle.rent_price && (
                                    <button onClick={() => handleDossier("rent")} className="btn-rent">
                                        Déposer un dossier de location — {Number(vehicle.rent_price).toLocaleString("fr-FR")} EUR/mois
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

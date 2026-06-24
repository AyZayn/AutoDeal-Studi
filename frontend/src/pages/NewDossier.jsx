import { useState, useEffect } from "react";
import { useLocation, useNavigate } from "react-router-dom";
import API from "../services/api";
import RentalOptions from "../components/RentalOptions";
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
    const [rentalOptions, setRentalOptions] = useState([]);
    const [selectedOptions, setSelectedOptions] = useState([]);

        useEffect(() => {
            API.get("/rental-options/")
                .then((res) => setRentalOptions(res.data))
                .catch(() => {});
        }, []); // Lancement au chargement de la page

    if (!vehicle) { navigate("/vehicles"); return null; }

    const calculateTotal = () => {
        let total = 0;
        let months = 1; // Par défaut 1 mois minimum pour la location

        if (type === "sale") {
            total = Number(vehicle.sale_price) || 0;
        } else {
            if (!startDate || !endDate) return 0;
            const days = Math.ceil((new Date(endDate) - new Date(startDate)) / (1000 * 60 * 60 * 24));
            if (days <= 0) return 0;
            
            months = Math.ceil(days / 30);
            total = months * Number(vehicle.rent_price);
        }

        selectedOptions.forEach(optionId => {
            
            const optionObj = rentalOptions.find(o => o.id === optionId);
            if (optionObj && optionObj.price) {
                const optionPrice = Number(optionObj.price);
                
                // Si c'est une option mensuelle ET qu'on est en location, on multiplie par le nombre de mois
                if (optionObj.billing_type?.toLowerCase() === "monthly" && type === "rent") {
                    total += optionPrice * months;
                } else {
                    // Sinon (forfait unique ou option d'achat), on l'ajoute une seule fois
                    total += optionPrice;
                }
            }
        });

        return total.toFixed(2);
    };

    const handleToggleOption = (optionId) => {
        setSelectedOptions(prev =>
            prev.includes(optionId)
                ? prev.filter(id => id !== optionId)
                : [...prev, optionId]
        );
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
                selected_options: selectedOptions,
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
                    Dossier de {type === "sale" ? "demande d'achat" : "demande de location"}
                </h1>

                {success && <div className="dossier-success">Dossier déposé avec succès ! Redirection...</div>}
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
                                : Number(vehicle.rent_price).toLocaleString("fr-FR") + " EUR/mois"}
                        </p>
                    </div>
                </div>

                <div className="dossier-form-card">
                    <h3>Informations du dossier</h3>
                    <form onSubmit={handleSubmit} className="dossier-form">
                        <div className="dossier-form-row">
                            <div className="dossier-field">
                                <label>{type === "sale" ? "Date d'achat souhaitée" : "Date de debut"}</label>
                                <input type="date" value={startDate} onChange={(e) => setStartDate(e.target.value)} required />
                            </div>
                            {type === "rent" && (
                                <div className="dossier-field">
                                    <label>Date de fin</label>
                                    <input type="date" value={endDate} onChange={(e) => setEndDate(e.target.value)} required />
                                </div>
                            )}
                        </div>

                    {rentalOptions.length > 0 && (
                        <RentalOptions
                            options={rentalOptions}
                            selectedOptions={selectedOptions}
                            onToggle={handleToggleOption}
                            readOnly={false}
                            offerType={type} 
                        />
                    )}

                        <div className="dossier-field">
                            <label>Message ou informations complémentaires (optionnel)</label>
                            <textarea
                                value={notes}
                                onChange={(e) => setNotes(e.target.value)}
                                placeholder="Ex: Je suis disponible le matin, j'ai deja un financement..."
                                rows={4}
                            />
                        </div>

                        {calculateTotal() > 0 && (
                            <div className="dossier-total">
                                <span>Total location estimé</span>
                                <span className="dossier-total-price">
                                    {Number(calculateTotal()).toLocaleString("fr-FR")} EUR
                                </span>
                            </div>
                        )}

                        {selectedOptions.length > 0 && (
                            <p className="dossier-options-note">
                                * Le prix des options sélectionnées sera défini par notre équipe après validation de votre dossier.
                            </p>
                        )}

                        <button type="submit" className="dossier-submit-btn">
                            Déposer mon dossier
                        </button>
                    </form>
                </div>
            </div>
        </div>
    );
}

export default NewDossier;

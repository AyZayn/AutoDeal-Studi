import { useState } from "react";
import { useLocation, useNavigate } from "react-router-dom";
import API from "../services/api";

function NewContract() {
    const { state } = useLocation();
    const navigate = useNavigate();
    const vehicle = state?.vehicle;
    const type = state?.type;
    const [startDate, setStartDate] = useState("");
    const [endDate, setEndDate] = useState("");
    const [error, setError] = useState("");
    const [success, setSuccess] = useState(false);

    if (!vehicle) { navigate("/vehicles"); return null; }

const calculateTotal = () => {
    if (type === "sale") return vehicle.sale_price;
    if (!startDate || !endDate) return 0;

    // 1. Calcul du nombre de jours réels
    const days = Math.ceil((new Date(endDate) - new Date(startDate)) / (1000 * 60 * 60 * 24));
    if (days <= 0) return 0;

    // 2. Conversion en mois (on divise par 30 jours en moyenne)
    // Math.ceil permet d'arrondir au mois supérieur (ex: 0.5 mois devient 1 mois, 1.2 mois devient 2 mois)
    const months = Math.ceil(days / 30);

    // 3. Calcul du prix total basé sur le prix par mois (rent_price)
    return (months * vehicle.rent_price).toFixed(2);
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
            });
            setSuccess(true);
            setTimeout(() => navigate("/contracts"), 2000);
        } catch {
            setError("Erreur lors de la creation du contrat");
        }
    };

    return (
        <div className="min-h-screen bg-gray-950 flex items-center justify-center px-4 py-12">
            <div className="w-full max-w-lg">
                <h1 className="text-3xl font-bold text-white mb-8">
                    {type === "sale" ? "Acheter" : "Louer"} — {vehicle.brand} {vehicle.model}
                </h1>
                {success && <p className="text-green-400 text-center mb-4 bg-green-500/10 py-3 rounded-xl">Contrat cree avec succes ! Redirection...</p>}
                {error && <p className="text-red-400 text-center mb-4 bg-red-500/10 py-3 rounded-xl">{error}</p>}
                <div className="bg-gray-900 rounded-2xl border border-gray-800 p-6 mb-6">
                    <div className="flex justify-between mb-2">
                        <span className="text-gray-400">Vehicule</span>
                        <span className="text-white font-semibold">{vehicle.brand} {vehicle.model} ({vehicle.year})</span>
                    </div>
                    <div className="flex justify-between mb-2">
                        <span className="text-gray-400">Kilométrage</span>
                        <span className="text-white">{vehicle.mileage} km</span>
                    </div>
                    <div className="flex justify-between">
                        <span className="text-gray-400">Prix</span>
                        <span className="text-red-400 font-bold">
                            {type === "sale" ? vehicle.sale_price + " EUR" : vehicle.rent_price + " EUR/jour"}
                        </span>
                    </div>
                </div>
                <form onSubmit={handleSubmit} className="bg-gray-900 rounded-2xl border border-gray-800 p-6 flex flex-col gap-4">
                    <div>
                        <label className="text-gray-400 text-sm block mb-2">{type === "sale" ? "Date d achat" : "Date de debut"}</label>
                        <input type="date" value={startDate} onChange={(e) => setStartDate(e.target.value)} className="w-full bg-gray-800 border border-gray-700 text-white px-4 py-3 rounded-xl focus:outline-none focus:border-red-500" required />
                    </div>
                    {type === "rent" && (
                        <div>
                            <label className="text-gray-400 text-sm block mb-2">Date de fin</label>
                            <input type="date" value={endDate} onChange={(e) => setEndDate(e.target.value)} className="w-full bg-gray-800 border border-gray-700 text-white px-4 py-3 rounded-xl focus:outline-none focus:border-red-500" required />
                        </div>
                    )}
                    {calculateTotal() > 0 && (
                        <div className="flex justify-between items-center bg-gray-800 px-4 py-3 rounded-xl">
                            <span className="text-gray-400">Total</span>
                            <span className="text-red-400 font-bold text-2xl">{calculateTotal()} EUR</span>
                        </div>
                    )}
                    <button type="submit" className="bg-red-500 hover:bg-red-600 text-white py-4 rounded-xl font-semibold text-lg transition">
                        Confirmer le contrat
                    </button>
                </form>
            </div>
        </div>
    );
}

export default NewContract;

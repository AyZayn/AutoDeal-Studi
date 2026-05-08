import { useState, useEffect } from "react";
import { Link } from "react-router-dom";
import API from "../services/api";
import "./VehicleList.css";

function VehicleList() {
    const [vehicles, setVehicles] = useState([]);
    const [loading, setLoading] = useState(true);
    const [filter, setFilter] = useState("all");
    const [search, setSearch] = useState("");

    useEffect(() => {
        API.get("/vehicles/")
            .then((res) => { setVehicles(res.data); setLoading(false); })
            .catch(() => setLoading(false));
    }, []);

    const fuelLabels = {
        gasoline: "Essence",
        diesel: "Diesel",
        electric: "Electrique",
        hybrid: "Hybride",
    };
    const filtered = vehicles.filter((v) => {
        const matchFilter = filter === "all" || v.offer_type === filter || v.offer_type === "both";
        const matchSearch = v.brand.toLowerCase().includes(search.toLowerCase()) || v.model.toLowerCase().includes(search.toLowerCase());
        return matchFilter && matchSearch;
    });

    if (loading) return <div className="page-loading">Chargement...</div>;

    return (
        <div className="vehicle-list-page">
            <div className="vehicle-list-header">
                <h1>Nos <span>Vehicules</span></h1>
                <p>Trouvez le vehicule parfait pour vous</p>
            </div>
            <div className="vehicle-list-controls">
                <input
                    type="text"
                    placeholder="Rechercher une marque ou modele..."
                    value={search}
                    onChange={(e) => setSearch(e.target.value)}
                    className="search-input"
                />
                <div className="filter-buttons">
                    {["all", "sale", "rent"].map((f) => (
                        <button
                            key={f}
                            onClick={() => setFilter(f)}
                            className={"filter-btn" + (filter === f ? " active" : "")}
                        >
                            {f === "all" ? "Tous" : f === "sale" ? "Achat" : "Location"}
                        </button>
                    ))}
                </div>
            </div>
            <div className="vehicle-grid">
                {filtered.map((vehicle) => (
                    <div key={vehicle.id} className="vehicle-card">
                        <div className="vehicle-card-image">
                            {vehicle.image
                                ? <img src={vehicle.image} alt={vehicle.brand} />
                                : <div className="no-image">Pas de photo</div>}
                            <span className={"offer-badge " + vehicle.offer_type}>
                                {vehicle.offer_type === "sale" ? "Vente" : vehicle.offer_type === "rent" ? "Location" : "Vente & Location"}
                            </span>
                        </div>
                        <div className="vehicle-card-body">
                            <h2>{vehicle.brand} {vehicle.model}</h2>
                            <p className="vehicle-meta">{vehicle.year} &bull; {vehicle.mileage} km &bull; {fuelLabels[vehicle.fuel] || vehicle.fuel}</p>
                            <div className="vehicle-prices">
    {vehicle.sale_price && (
        <div className="price-block">
            <span className="price-label">Achat</span>
            <span className="price-sale">{Number(vehicle.sale_price).toLocaleString("fr-FR")} EUR</span>
        </div>
    )}
    {vehicle.rent_price && (
        <div className="price-block">
            <span className="price-label">Location</span>
            <span className="price-rent">{Number(vehicle.rent_price).toLocaleString("fr-FR")} EUR/j</span>
        </div>
    )}
</div>
                            <Link to={"/vehicles/" + vehicle.id} className="vehicle-card-btn">Voir details →</Link>
                        </div>
                    </div>
                ))}
            </div>
            {filtered.length === 0 && <p className="empty-message">Aucun vehicule trouve</p>}
        </div>
    );
}

export default VehicleList;

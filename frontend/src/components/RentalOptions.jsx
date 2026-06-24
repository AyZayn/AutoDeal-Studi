import "./RentalOptions.css";

// On ajoute 'offerType' aux propriétés du composant
function RentalOptions({ options, selectedOptions, onToggle, readOnly, offerType }) {
    const included = options.filter(o => o.option_type === "included");
    const supplements = options.filter(o => o.option_type === "supplement");

    return (
        <div className="rental-options">
            {/* 1. Les options incluses s'affichent toujours */}
            {included.length > 0 && (
                <div className="options-section">
                    <h3 className="options-title">
                        <span className="options-badge included">Inclus</span>
                        Avantages inclus dans la location
                    </h3>
                    <div className="options-grid">
                        {included.map((option) => (
                            <div key={option.id} className="option-card included">
                                <div className="option-check">✓</div>
                                <div className="option-info">
                                    <p className="option-name">{option.name}</p>
                                    {option.description && <p className="option-desc">{option.description}</p>}
                                    <span className="option-price-tag">Gratuit</span>
                                </div>
                            </div>
                        ))}
                    </div>
                </div>
            )}

            {/* 2. Les suppléments s'affichent UNIQUEMENT si offerType vaut "sale" */}
            {supplements.length > 0 && offerType === "sale" && (
                <div className="options-section">
                    <h3 className="options-title">
                        <span className="options-badge supplement">Options</span>
                        Options supplémentaires si achat du véhicule
                    </h3>
                    <p className="options-subtitle">Prix définis après validation de votre dossier</p>
                    <div className="options-grid">
                        {supplements.map((option) => (
                            <div
                                key={option.id}
                                className={"option-card supplement " + (selectedOptions.includes(option.id) ? "selected" : "") + (readOnly ? " readonly" : "")}
                                onClick={() => !readOnly && onToggle(option.id)}
                            >
                                <div className="option-check">
                                    {selectedOptions.includes(option.id) ? "✓" : "+"}
                                </div>
                                <div className="option-info">
                                    <p className="option-name">{option.name}</p>
                                    {option.description && <p className="option-desc">{option.description}</p>}
                                    <span className="option-billing">
                                        {option.billing_type === "monthly" ? "Facturation mensuelle" : "Forfait unique"}
                                    </span>
                                </div>
                            </div>
                        ))}
                    </div>
                </div>
            )}
        </div>
    );
}

export default RentalOptions;

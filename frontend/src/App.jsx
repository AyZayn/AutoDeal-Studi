import { BrowserRouter, Routes, Route } from "react-router-dom";
import { AuthProvider } from "./context/AuthContext";
import ErrorBoundary from "./components/ErrorBoundary";
import Navbar from "./components/Navbar";
import Home from "./pages/Home";
import VehicleList from "./pages/VehicleList";
import VehicleDetail from "./pages/VehicleDetail";
import Login from "./pages/Login";
import Register from "./pages/Register";
import Dossiers from "./pages/Dossiers";
import DossierDetail from "./pages/DossierDetail";
import NewDossier from "./pages/NewDossier";
import Profile from "./pages/Profile";

function App() {
    return (
        <ErrorBoundary>
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
                        <Route path="/dossiers/:id" element={<DossierDetail />} />
                        <Route path="/dossier/new" element={<NewDossier />} />
                        <Route path="/profile" element={<Profile />} />
                    </Routes>
                </BrowserRouter>
            </AuthProvider>
        </ErrorBoundary>
    );
}

export default App;
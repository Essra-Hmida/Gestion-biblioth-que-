// src/pages/AdminDashboard.js  
import React from 'react';  
import { useNavigate } from 'react-router-dom';  
import { useUser } from '../context/UserContext'; // Import du contexte utilisateur

function AdminDashboard() {  
    const navigate = useNavigate();  
    const { userId } = useUser();  // Récupération de l'ID utilisateur depuis le contexte

    // Vérification si l'utilisateur est connecté et s'il a un rôle d'administrateur
    if (!userId) {
        // Redirige vers la page de connexion si l'utilisateur n'est pas connecté
        navigate('/signin');
        return null;  // Empêche le rendu du composant si l'utilisateur n'est pas connecté
    }

    const handleBookManagement = () => {  
        navigate('/admin/books'); // Redirige vers la page de gestion des livres  
    };  

    const handleMemberManagement = () => {  
        navigate('/admin/members'); // Redirige vers la page de gestion des membres  
    };  

    const handleBorrowReturnManagement = () => {  
        navigate('/admin/borrow-return'); // Redirige vers la page de gestion des emprunts et retours  
    };  

    return (  
        <div className="admin-dashboard">  
            <h2>Tableau de Bord Administrateur</h2>  
            <p>Choisissez une option :</p>  
            <button onClick={handleBookManagement}>Gérer les Livres</button>  
            <button onClick={handleMemberManagement}>Gérer les Membres</button>  
            <button onClick={handleBorrowReturnManagement}>Gérer Emprunts et Retours</button>  
        </div>  
    );  
}  

export default AdminDashboard;

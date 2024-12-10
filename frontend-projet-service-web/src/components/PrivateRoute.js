import React from 'react';
import { Navigate } from 'react-router-dom';

function PrivateRoute({ children, isAdminRoute }) {
  // Récupérer les informations d'authentification depuis localStorage
  const token = localStorage.getItem('token');
  const isAdmin = localStorage.getItem('is_admin') === 'true'; // Vérifiez si l'utilisateur est admin

  // Si l'utilisateur n'est pas authentifié
  if (!token) {
    return <Navigate to="/signin" />;
  }

  // Si la route est réservée aux administrateurs et que l'utilisateur n'est pas admin
  if (isAdminRoute && !isAdmin) {
    return <Navigate to="/booklist" />; // Redirigez vers la page utilisateur normal
  }

  // Sinon, autoriser l'accès
  return children;
}

export default PrivateRoute;

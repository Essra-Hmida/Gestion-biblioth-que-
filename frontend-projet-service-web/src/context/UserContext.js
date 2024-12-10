// UserContext.js
import React, { createContext, useContext, useState } from 'react';

// Création du contexte utilisateur
const UserContext = createContext();

// Hook personnalisé pour utiliser le contexte utilisateur
export const useUser = () => {
  return useContext(UserContext);
};

// Fournisseur du contexte utilisateur
export const UserProvider = ({ children }) => {
  const [user, setUser] = useState(null); // Initialement, aucun utilisateur connecté

  return (
    <UserContext.Provider value={{ user, setUser }}>
      {children}
    </UserContext.Provider>
  );
};

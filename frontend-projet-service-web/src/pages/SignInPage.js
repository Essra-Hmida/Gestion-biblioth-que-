import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { useUser } from '../context/UserContext'; // Importer le hook personnalisé
import '../styles/SignInPage.css';

function SignInPage() {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const { setUser } = useUser(); // Hook pour définir l'utilisateur global
  const navigate = useNavigate();

  const handleLogin = async () => {
    try {
      const response = await fetch(`http://127.0.0.1:8000/api/sign-in`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          username: email,
          password: password,
        }),
      });

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.message || 'Erreur réseau ou identifiants invalides');
      }

      const data = await response.json();

      if (data.utilisateur) {
        // Stocker l'utilisateur dans le contexte
        setUser(data.utilisateur);

        // Redirection basée sur le rôle
        if (data.utilisateur.is_admin) {
          navigate('/dashboard');
        } else {
          navigate('/booklist');
        }
      } else {
        alert('Erreur de connexion : ' + data.message);
      }
    } catch (error) {
      console.error('Erreur lors de la connexion : ', error);
      alert('Une erreur est survenue : ' + error.message);
    }
  };

  const handleSignUp = () => {
    navigate('/signup');
  };

  return (
    <div className="signin">
      <h2>Se connecter</h2>
      <input
        type="email"
        value={email}
        onChange={(e) => setEmail(e.target.value)}
        placeholder="Email"
      />
      <input
        type="password"
        value={password}
        onChange={(e) => setPassword(e.target.value)}
        placeholder="Mot de passe"
      />
      <button onClick={handleLogin}>Se connecter</button>
      <button onClick={handleSignUp}>S'inscrire</button>
    </div>
  );
}

export default SignInPage;

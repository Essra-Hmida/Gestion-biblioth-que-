import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import '../styles/SignUpPage.css';

function SignUpPage() {
  const [name, setName] = useState('');
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState(null); // Pour afficher des messages d'erreur
  const [success, setSuccess] = useState(false); // Pour afficher le succès
  const navigate = useNavigate();

  const handleSignUp = async () => {
    // Réinitialiser les messages d'erreur ou de succès
    setError(null);
    setSuccess(false);

    try {
      const response = await fetch('http://localhost:8000/api/sign-up', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          username: name,
          email: email,
          password: password,
        }),
      });

      if (!response.ok) {
        const errorData = await response.json();
        setError(errorData.error || 'Une erreur est survenue.');
        return;
      }

      const data = await response.json();
      console.log('Inscription réussie :', data);

      // Afficher un message de succès et rediriger
      setSuccess(true);
      setTimeout(() => navigate('/booklist'), 2000); // Redirection après 2 secondes
    } catch (err) {
      console.error('Erreur lors de la requête :', err);
      setError('Impossible de contacter le serveur.');
    }
  };

  return (
    <div className="signup">
      <h2>S'inscrire</h2>
      {error && <p style={{ color: 'red' }}>{error}</p>}
      {success && <p style={{ color: 'green' }}>Inscription réussie ! Redirection en cours...</p>}
      <input
        type="text"
        value={name}
        onChange={(e) => setName(e.target.value)}
        placeholder="Nom"
      />
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
      <button onClick={handleSignUp}>S'inscrire</button>
      <button onClick={() => navigate('/signin')}>Annuler</button>
    </div>
  );
}

export default SignUpPage;

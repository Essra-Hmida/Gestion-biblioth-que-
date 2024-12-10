import React, { useState, useEffect } from 'react';
import { FaUserCircle } from 'react-icons/fa'; // Icône utilisateur de react-icons
import { Link } from 'react-router-dom'; // Pour la redirection vers la page de profil
import '../styles/BookListPage.css'; // Inclure le fichier CSS

function BookListPage() {
  const [books, setBooks] = useState([]);
  const [searchTerm, setSearchTerm] = useState('');

  // Effectuer la requête GET pour récupérer les livres depuis l'API Django
  useEffect(() => {
    fetch('http://localhost:8000/api/livres') // L'URL de votre API Django
      .then((response) => response.json()) // Convertir la réponse en JSON
      .then((data) => setBooks(data)) // Mettre à jour l'état avec les livres récupérés
      .catch((error) => console.error('Erreur lors de la récupération des livres:', error));
  }, []);

  const handleSearch = (event) => {
    setSearchTerm(event.target.value);
  };

  const handleBorrow = (livreId) => {
    // Fonction pour calculer la date de retour
    const calculateReturnDate = (startDate, daysToAdd) => {
      const resultDate = new Date(startDate);
      resultDate.setDate(resultDate.getDate() + daysToAdd);
      return resultDate.toISOString().slice(0, 10); // Retourne la date au format YYYY-MM-DD
    };

    // Date actuelle
    const today = new Date().toISOString().slice(0, 10);
    const returnDate = calculateReturnDate(today, 14); // Ajoute 14 jours
    fetch('http://127.0.0.1:8000/api/emprunts/add', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        livre: livreId,
        utilisateur: 5, // Remplacez par l'ID de l'utilisateur actuel
        date_emprunt: today, // Date actuelle
        date_retour: returnDate, // Date de retour calculée
      }),
    })
      .then((response) => {
        if (!response.ok) {
          // Si la réponse n'est pas "200 OK"
          return response.json().then((errorData) => {
            throw new Error(errorData.error || 'Erreur inconnue');
          });
        }
        return response.json();
      })
      .then((data) => {
        alert(`Emprunt effectué avec succès : ${data.livre}`);
      })
      .catch((error) => {
        alert(`Erreur lors de l'emprunt : ${error.message}`);
      });
  };

  return (
    <div className="booklist-container">
      <div className="top-nav">
        <h2>Catalogue des livres</h2>
        <Link to="/user-profile">
          <FaUserCircle size={40} color="black" />
        </Link>
      </div>

      <input
        type="text"
        placeholder="Recherche par titre"
        value={searchTerm}
        onChange={handleSearch}
        className="search-bar"
      />

      <div className="book-cards">
        {books
          .filter((book) => book.titre.toLowerCase().includes(searchTerm.toLowerCase()))
          .map((book) => (
            <div className="book-card" key={book.id}>
              <h3>{book.titre}</h3>
              <p><strong>Auteur:</strong> {book.auteur}</p>
              <p><strong>ISBN:</strong> {book.isbn}</p>
              <p><strong>Genre:</strong> {book.genre}</p>
              <p><strong>Emplacement:</strong> {book.emplacement}</p>
              <p className={`availability ${book.disponible ? 'available' : 'unavailable'}`}>
                {book.disponible ? 'Disponible' : 'Indisponible'}
              </p>
              {book.disponible ? (
                <button className="borrow-btn" onClick={() => handleBorrow(book.id)}>
                  Emprunter
                </button>
              ) : (
                <p>Indisponible</p>
              )}
            </div>
          ))}
      </div>
    </div>
  );
}

export default BookListPage;

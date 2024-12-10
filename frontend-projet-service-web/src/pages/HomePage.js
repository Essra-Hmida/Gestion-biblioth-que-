import React from 'react';  
import { Link } from 'react-router-dom';  
import '../styles/HomePage.css';  
import homeImage from '../assets/image_home.png';  // Importer l'image
function HomePage() {  
  return (  
    <div className="home">  
      <div className="text-container">  
        <h1>Bienvenue à notre Bibliothèque</h1>  
        <p>Explorez notre catalogue de livres et gérez vos emprunts</p>  
        <Link to="/signin">  
          <button>Se connecter / S'inscrire</button>  
        </Link>  
      </div>  
      <img src={homeImage} alt="Bibliothèque" className="hero-image" />  {/* Utiliser l'image importée */}  
    </div>  
  );  
}  

export default HomePage;
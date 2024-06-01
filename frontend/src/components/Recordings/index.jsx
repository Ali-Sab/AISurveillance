import Card from "./Card.jsx";
import { useState, useEffect } from 'react';
import axios from 'axios'; //js lib api that helps w asynch HTTPS requests
import './Modal.css';

function Recordings() {
const [images, setImages] = useState([]);
const [view, setView] = useState(false);
const [selectedImage, setSelectedImage] = useState(null); // State to store selected image


const toggleView = () => {
  setView(!view);
  console.log("toggled!");
}


// Fetch images from Flask server and set images
useEffect(() => {
  axios.get('http://localhost:5000/live')
    .then(response => {
      setImages(response.data);
    })
    .catch(error => {
      console.error('Error fetching images:', error);
    });
}, []);

  return (
    <>
    <div>
      <h1>Recordings</h1>
    </div>
      <ul className="grid gap-4 grid-cols-3">     
        {images.map((image, index) => (
          <Card key={index} img={image.filepath} date={new Date(selectedImage.datetime * 1000).toLocaleString()} toggleView={ () => {
            setSelectedImage(image);
            toggleView();
          }} />
        ))}
      
      </ul>
      <div>
          {view && selectedImage &&
            (<div className="view">
            <div className="overlay" onClick={toggleView}></div>
                <div className="modal-box">
                  <figure><img src={selectedImage.filepath} alt="img" /></figure>
                  <h3 className="font-bold text-lg">Date: {new Date(selectedImage.datetime * 1000).toLocaleString()}</h3>
                  <p className="py-4">Path: {selectedImage.filepath}</p>
                  <div className="modal-action">
                    <form method="dialog">
                      <button className="btn" onClick={toggleView}>Close</button>
                    </form>
                  </div>
                </div>
            </div>) 
          }
        </div>
    </>
  );
}

export default Recordings;
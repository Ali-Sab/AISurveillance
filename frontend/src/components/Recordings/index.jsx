import Card from "./Card.jsx";
import { useState, useEffect } from 'react';
import axios from 'axios'; //js lib api that helps w asynch HTTPS requests

function Recordings() {
const [currentPage, setCurrentPage] = useState([1]);
const [images, setImages] = useState([]);

const Forward=()=>{
  setCurrentPage(); //trying to implement page function
};

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
          <Card key={index} img={image.filepath} />
        ))}
      
      </ul>
      <div className="join">
        <button className="join-item btn" onClick="Back">«</button>
        <button className="join-item btn">Page 22</button>
        <button className="join-item btn" onClick="Forward">»</button>
      </div>
    </>
  );
}

export default Recordings;
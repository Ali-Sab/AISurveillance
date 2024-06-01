import React, {useState} from 'react';


function Card({img,date,toggleView}){
    return(
        <div>
          <div className="card card-compact w-96 bg-base-100 shadow-xl">
            <figure><img src={img} alt="img" /></figure>
            <div className="card-body">
              <h2 className="card-title">{date}</h2>
              <div className="card-actions justify-end">
                <button className="btn btn-primary" onClick={toggleView}>View</button>
              </div>
            </div>
          </div>
        </div>
    );
}
export default Card;

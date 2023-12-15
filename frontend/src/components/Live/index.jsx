import Slider from '@mui/material/Slider';
import Image from 'react-bootstrap/Image';
import { useState, useEffect, useRef } from 'react';
import { sendRequestWithoutAuth } from '../../NetworkUtils';

let marks = [
    {
        value: 10,
        label: '10°C',
    },
    {
        value: 20,
        label: '20°C',
    },
    {
        value: 37,
        label: '37°C',
    },
    {
        value: 60,
        label: '60°C',
    },
];

function valuetext(value) {
    return 'no';
}

function Live(props) {
    const [imagePath, setImagePath] = useState([]);
    const [images, setImages] = useState([]);
    let waitingForResponse = useRef(0);

    useEffect(() => {
        const getImages = async () => {
            waitingForResponse.current = 1;

            let url = "http://localhost:5000/live"
            try {
                let responseJson = await sendRequestWithoutAuth(url);
                for (let item of responseJson) {
                    item.value = item.datetime
                }
                let dNow = new Date(responseJson[0].datetime * 1000)
                let date = ( (dNow.getMonth() + 1).toString().padStart(2, '0') ) + '/' + dNow.getDate().toString().padStart(2, '0') + '/' + dNow.getFullYear() + ' ' + dNow.getHours().toString().padStart(2, '0') + ':' + dNow.getMinutes().toString().padStart(2, '0') + ':' + dNow.getSeconds().toString().padStart(2, '0');
                responseJson[0].label = date;
                dNow = new Date(responseJson[responseJson.length - 1].datetime * 1000)
                date = ( (dNow.getMonth() + 1).toString().padStart(2, '0') ) + '/' + dNow.getDate().toString().padStart(2, '0') + '/' + dNow.getFullYear() + ' ' + dNow.getHours().toString().padStart(2, '0') + ':' + dNow.getMinutes().toString().padStart(2, '0') + ':' + dNow.getSeconds().toString().padStart(2, '0');
                responseJson[responseJson.length - 1].label = date;

                setImages(responseJson);
              } catch (error) {
                let errorJson = JSON.parse(error.message);
                console.log(errorJson)
                return
              }
        }

        if (waitingForResponse.current === 0) {
            getImages().catch(error => console.log(error)).finally(() => waitingForResponse.current = 0);
        }
    }, [setImages]);

    function valueLabelFormat(value) {
        if (value > 0) {
            let dNow = new Date(value * 1000)
            let date = ( (dNow.getMonth() + 1).toString().padStart(2, '0') ) + '/' + dNow.getDate().toString().padStart(2, '0') + '/' + dNow.getFullYear() + ' ' + dNow.getHours().toString().padStart(2, '0') + ':' + dNow.getMinutes().toString().padStart(2, '0') + ':' + dNow.getSeconds().toString().padStart(2, '0');
            return date;
        }
        return '0';
    }

    function updateImage(value) {
        setImagePath(images[images.findIndex((image) => image.value === value.target.value)]['filepath']);
    }

    function addImageTest() {
        setImages([... images, {value: 45, label: 'hello?????'}])
        marks = [...marks, {value: 45, label: '45 degrees'}]
    }

    return <div>
        <Image src={imagePath} alt={imagePath} fluid />
        <div>Something: {imagePath}</div>
        <Slider
            aria-label="Restricted values"
            defaultValue={
                images.length > 0
                    ? images[0]['datetime']
                    : 1702324827
            }
            valueLabelFormat={valueLabelFormat}
            getAriaValueText={valuetext}
            step={null}
            valueLabelDisplay="auto"
            marks={images}
            onChange={updateImage}
            min={
                images.length > 0
                    ? images[0].value
                    : 0
            }
            max={
                images.length > 0
                    ? images[images.length - 1].value
                    : 100
            }
            track={false}
        />
        <button onClick={addImageTest} >hello</button>
    </div>
}

export default Live
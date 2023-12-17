import Slider from '@mui/material/Slider';
import Image from 'react-bootstrap/Image';
import { useState, useEffect, useRef } from 'react';
import { sendRequestWithoutAuth } from '../../NetworkUtils';
import { Button, Checkbox, FormControlLabel } from '@mui/material';
import { socket } from '../../socket';

function Live(props) {
    const [imagePath, setImagePath] = useState("");
    const [currImageIndex, setCurrImageIndex] = useState(0);
    const [images, setImages] = useState([]);
    const [sliderValue, setSliderValue] = useState(1);
    const [followLatest, setFollowLatest] = useState(true);
    let waitingForResponse = useRef(0);

    useEffect(() => {
        let imageInterval;
        clearInterval(imageInterval);
        imageInterval = setInterval(() => {
            if (socket.connected) {
                console.log("it's me, ", images.length)
                if (images.length === 0)
                    socket.timeout(2500).emit("getImage", 0);
                else
                    socket.timeout(2500).emit("getImage", images[images.length - 1].datetime);
            }
        }, 3000);

        return () => {
            clearInterval(imageInterval);
        }
    }, [images]);

    useEffect(() => {
        function onFilepath(value) {
            value.value = value.datetime;
            let new_images = images
            if (new_images.length > 1)
                delete new_images[new_images.length - 1]['label']
            let dNow = new Date(value.datetime * 1000)
            let date = ((dNow.getMonth() + 1).toString().padStart(2, '0')) + '/' + dNow.getDate().toString().padStart(2, '0') + '/' + dNow.getFullYear() + ' ' + dNow.getHours().toString().padStart(2, '0') + ':' + dNow.getMinutes().toString().padStart(2, '0') + ':' + dNow.getSeconds().toString().padStart(2, '0');
            value.label = date;
            new_images = [...new_images, value];
            console.log(new_images);
            setImages(new_images);
            if (imagePath.length === 0) {
                setImagePath(value.filepath)
            } else if (followLatest) {
                setImagePath(value.filepath);
                setCurrImageIndex(new_images.length - 1);
                setSliderValue(value.value)
            }
        }

        socket.on('filepath', onFilepath);
        console.log('passing')

        return () => {
            socket.off('filepath', onFilepath);
        }
    }, [images, imagePath, followLatest]);

    useEffect(() => {
        var success = 0;

        const getImages = async () => {
            waitingForResponse.current = 1;

            let url = "http://localhost:5000/live"
            try {
                let responseJson = await sendRequestWithoutAuth(url);
                if (responseJson.length === 0) {
                    success = 1;
                    setSliderValue(50);
                    return;
                }
                for (let item of responseJson) {
                    item.value = item.datetime
                }
                let dNow = new Date(responseJson[0].datetime * 1000)
                let date = ((dNow.getMonth() + 1).toString().padStart(2, '0')) + '/' + dNow.getDate().toString().padStart(2, '0') + '/' + dNow.getFullYear() + ' ' + dNow.getHours().toString().padStart(2, '0') + ':' + dNow.getMinutes().toString().padStart(2, '0') + ':' + dNow.getSeconds().toString().padStart(2, '0');
                responseJson[0].label = date;
                dNow = new Date(responseJson[responseJson.length - 1].datetime * 1000)
                date = ((dNow.getMonth() + 1).toString().padStart(2, '0')) + '/' + dNow.getDate().toString().padStart(2, '0') + '/' + dNow.getFullYear() + ' ' + dNow.getHours().toString().padStart(2, '0') + ':' + dNow.getMinutes().toString().padStart(2, '0') + ':' + dNow.getSeconds().toString().padStart(2, '0');
                responseJson[responseJson.length - 1].label = date;

                setImages(responseJson);
                setCurrImageIndex(0);
                setImagePath(responseJson[0]['filepath'])
                setSliderValue(responseJson[0]['datetime']);
                success = 1;
            } catch (error) {
                let errorJson = JSON.parse(error.message);
                console.log(errorJson)
                return;
            }
        }

        if (waitingForResponse.current === 0) {
            getImages().catch(error => console.log(error)).finally(() => {
                waitingForResponse.current = 0;
                if (success) {
                    socket.connect();
                    console.log(socket.conected)
                }
            });
        }

        return () => {
            socket.timeout(5000).emit("connection_closed")
            socket.close();
        }
    }, [setImages, setImagePath, setCurrImageIndex, setSliderValue]);

    function valueLabelFormat(value) {
        if (value > 0) {
            let dNow = new Date(value * 1000)
            let date = ((dNow.getMonth() + 1).toString().padStart(2, '0')) + '/' + dNow.getDate().toString().padStart(2, '0') + '/' + dNow.getFullYear() + ' ' + dNow.getHours().toString().padStart(2, '0') + ':' + dNow.getMinutes().toString().padStart(2, '0') + ':' + dNow.getSeconds().toString().padStart(2, '0');
            return date;
        }
        return '0';
    }

    function updateImage(value) {
        if (images.length > 0) {
            let index = images.findIndex((image) => image.value === value.target.value);
            setCurrImageIndex(index);
            setImagePath(images[index]['filepath']);
            setSliderValue(images[index]['datetime']);
        }
    }

    function prevImage() {
        if (currImageIndex > 0) {
            let index = currImageIndex - 1;
            setCurrImageIndex(index);
            setImagePath(images[index]['filepath'])
            setSliderValue(images[index]['datetime']);
        }
    }

    function nextImage() {
        if (currImageIndex < images.length - 1) {
            let index = currImageIndex + 1;
            setCurrImageIndex(index);
            setImagePath(images[index]['filepath']);
            setSliderValue(images[index]['datetime']);
        }
    }

    function toggleLive(value) {
        setFollowLatest(value.target.checked);
    }

    function valuetext(value, i) {
        if (images.length > 0)
            return images[i].label;
        return "0";
    }

    return <div>
        <div className='d-flex flex-row justify-content-center'>
            <div className='d-flex flex-column'>
                <Image src={imagePath} alt={imagePath} fluid />
                <h6>Filepath: {imagePath}</h6>
            </div>
        </div>
        <Slider
            aria-label="Restricted values"
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
            value={sliderValue}
        />
        <div className='d-flex flex-row justify-content-center'>
            <Button className="m-2" onClick={prevImage} variant='contained'>Previous Image</Button>
            <Button className="m-2" onClick={nextImage} variant='contained'>Next Image</Button>
        </div>
        <FormControlLabel control={
            <Checkbox onChange={toggleLive} defaultChecked />
        } label="Auto-select newest image" />
    </div>
}

export default Live
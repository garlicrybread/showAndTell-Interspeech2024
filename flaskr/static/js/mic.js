// collect DOMs
const display = document.querySelector('.display');
const State = ['Initial', 'Record', 'StopRecord']
let stateIndex = 0;
let mediaRecorders = []; // Array to store multiple media recorders
let chunks = []; // Array to store chunks for each recorder
let audioURLs = []; // Array to store multiple audio URLs
let recordingIndex = 0; // Counter for recording index
let isRecording = false;

const toggleRecording = (index) => {
    isRecording = !isRecording;
    const button = document.getElementById(`recordButton${index}`);
    if (isRecording && mediaRecorders[recordingIndex] == null) {
        startRecording();
        button.textContent = 'Stop Recording';
    } else {
        stopRecording();
        addNewAudioBar();
        button.textContent = 'Record';
    }
};

const startRecording = () => {
    
    navigator.mediaDevices.getUserMedia({
        audio: true
    }).then(stream => {
        mediaRecorders[recordingIndex] = new MediaRecorder(stream);

        mediaRecorders[recordingIndex].ondataavailable = (e) => {
            chunks.push(e.data);
        };

        mediaRecorders[recordingIndex].start();
        stateIndex = 1;
    }).catch(error => {
        console.log('Following error has occurred: ', error);
    });
};

const stopRecording = () => {
    
    mediaRecorders[recordingIndex].stop();
    if (mediaRecorders[recordingIndex]) {
        mediaRecorders[recordingIndex].onstop = () => {
            const blob = new Blob(chunks, { 'type': 'audio/ogg; codecs=opus' });
            chunks = [];
            audioURLs[recordingIndex] = window.URL.createObjectURL(blob);
            application(stateIndex);
        };
    } else {
        console.error('mediaRecorders[recordingIndex] is undefined');
    }

    stateIndex = 2;
    
};


const addNewAudioBar = () => {
    if (audioURLs[recordingIndex]) {
        const audioContainer = document.createElement('div');
        audioContainer.classList.add('audio-container');

        const audioElement = document.createElement('audio');
        audioElement.controls = true;
        audioElement.src = audioURLs[recordingIndex];
        audioContainer.appendChild(audioElement);

        const containerId = `audioContainer${recordingIndex}`;
        document.getElementById(containerId).appendChild(audioContainer);
        toggleRecording(recordingIndex);
        recordingIndex++;
    }
};



const addMessage = (text) => {
    const msg = document.createElement('p');
    msg.textContent = text;
    display.append(msg);
};

const clearDisplay = () => {
    display.textContent = '';
};

const addButton = (id, funString, text) => {
    const btn = document.createElement('button');
    btn.id = id;
    btn.setAttribute('onclick', funString);
    btn.textContent = text;
    display.append(btn);
};

const application = (index) => {
    clearDisplay();
    switch (State[index]) {
        case 'Initial':
            addButton('record', '', 'Record');
            break;

        case 'Record':
            addButton('stop', 'toggleRecording()', 'Stop Recording');
            break;

        case 'StopRecord':
            stopRecording(); // Assuming stopRecording function handles stopping the recording
            addNewAudioBar(); // Assuming addNewAudioBar function handles creating a new audio bar
            addButton('record', 'toggleRecording()', 'Record');
            break;

        default:
            addMessage('Your browser does not support mediaDevices');
            break;
    }
};


application(stateIndex);

const video = document.getElementById('video');
const emotionElement = document.getElementById('emotion');
const songOptionsDiv = document.getElementById('song-options');
const songButtonsDiv = document.getElementById('song-buttons');
const songPlayer = document.getElementById('song-player');
const songSource = document.getElementById('song-source');

// Start the webcam
navigator.mediaDevices.getUserMedia({ video: true })
  .then(stream => { video.srcObject = stream; })
  .catch(err => { alert('Could not access webcam: ' + err); });

// Capture image every 1 second
let captureInterval = setInterval(() => {
  const canvas = document.createElement('canvas');
  canvas.width = video.videoWidth;
  canvas.height = video.videoHeight;
  const context = canvas.getContext('2d');
  context.drawImage(video, 0, 0, canvas.width, canvas.height);

  const imageData = canvas.toDataURL('image/jpeg');
  emotionElement.innerHTML = 'Detecting emotion...';

  // Send image to backend
  $.ajax({
    url: '/detect_emotion',
    method: 'POST',
    contentType: 'application/json',
    data: JSON.stringify({ image: imageData }),
    success: (response) => {
      if (response.error) {
        emotionElement.innerHTML = 'Error: ' + response.error;
      } else {
        emotionElement.innerHTML = `Emotion Detected: ${response.emotion}`;
        
        // Stop capturing once detected
        clearInterval(captureInterval);
        video.srcObject.getTracks().forEach(track => track.stop());

        songOptionsDiv.style.display = 'block';
        songButtonsDiv.innerHTML = '';

        response.songs.forEach(song => {
          const button = document.createElement('button');
          button.classList.add('song-button');
          button.textContent = song;
          button.onclick = () => {
            songPlayer.pause();
            songPlayer.currentTime = 0;
            songSource.src = `/static/music/${song}`;
            songPlayer.style.display = 'block';
            songPlayer.load();
            songPlayer.play();
          };
          songButtonsDiv.appendChild(button);
        });
      }
    },
    error: () => { emotionElement.innerHTML = 'Error communicating with backend.'; }
  });
}, 1000);

// JavaScript for handling automatic audio recording and sends audio to backend 

let mediaRecorder;
let audioChunks = [];

function startRecording(roundId, teamId) {
    navigator.mediaDevices.getUserMedia({ audio: true })
        .then(stream => {
            mediaRecorder = new MediaRecorder(stream);
            audioChunks = [];

            mediaRecorder.addEventListener("dataavailable", event => {
                audioChunks.push(event.data);
            });

            mediaRecorder.addEventListener("stop", () => {
                const audioBlob = new Blob(audioChunks, { type: 'audio/wav' });
                const formData = new FormData();
                formData.append("audio", audioBlob);

                fetch(`/singing/${roundId}/${teamId}/`, {
                    method: "POST",
                    body: formData,
                })
                .then(response => {
                    if(response.ok){
                        alert("Audio processed and points awarded!");
                        location.reload();
                    } else {
                        alert("Error processing audio");
                    }
                });
            });

            mediaRecorder.start();

            // Stop recording automatically after 10 seconds
            setTimeout(() => {
                if(mediaRecorder.state !== "inactive") mediaRecorder.stop();
            }, 10000); 
        })
        .catch(error => {
            console.error("Error accessing microphone:", error);
            alert("Microphone access denied or unavailable.");
        });
}

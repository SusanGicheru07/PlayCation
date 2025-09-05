// JavaScript for handling game interactions like hints display and team shuffling
function showHint(roundId) {
    const hintElement = document.getElementById(`hint-${roundId}`);
    hintElement.style.display = "block";
}

function shuffleTeams() {
    fetch("/shuffle-teams/")
        .then(res => res.json())
        .then(data => {
            alert("Teams shuffled!");
            location.reload();
        });
}

// Optional: Live timer for rounds
function startTimer(roundId, duration = 60) {
    let timer = duration;
    const timerEl = document.getElementById(`timer-${roundId}`);
    const interval = setInterval(() => {
        timerEl.innerText = `Time left: ${timer}s`;
        timer--;
        if(timer < 0) clearInterval(interval);
    }, 1000);
}

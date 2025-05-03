// base/static/base/js/clock.js
function updateClock() {
    const now = new Date();
    const timeElement = document.querySelector('.digital-clock');
    const dateElement = document.querySelector('.current-date');
    
    const timeString = now.toLocaleTimeString('en-US', {hour12: false});
    const options = { weekday: 'long', year: 'numeric', month: 'long', day: 'numeric' };
    const dateString = now.toLocaleDateString('en-US', options);
    
    if(timeElement) timeElement.textContent = timeString;
    if(dateElement) dateElement.textContent = dateString;
}

updateClock();
setInterval(updateClock, 1000);
document.addEventListener('DOMContentLoaded', function() {
    // Configuration - set your event dates here
    const eventDates = [14, 17, 18, 19]; // Dates to highlight
    const currentMonth = 4; // May (0-indexed)
    const currentYear = 2023;
    
    // Get first day of month and total days in month
    const firstDay = new Date(currentYear, currentMonth, 1).getDay();
    const daysInMonth = new Date(currentYear, currentMonth + 1, 0).getDate();
    
    // Create calendar days
    const calendarGrid = document.querySelector('.calendar-grid');
    
    // Add empty cells for days before the first day of the month
    for (let i = 0; i < firstDay; i++) {
        const emptyCell = document.createElement('div');
        emptyCell.className = 'day empty';
        calendarGrid.appendChild(emptyCell);
    }
    
    // Add cells for each day of the month
    for (let day = 1; day <= daysInMonth; day++) {
        const dayCell = document.createElement('div');
        dayCell.className = 'day';
        
        const dayNumber = document.createElement('div');
        dayNumber.className = 'day-number';
        dayNumber.textContent = day;
        dayCell.appendChild(dayNumber);
        
        // Check if this is an event day
        if (eventDates.includes(day)) {
            dayCell.classList.add('highlighted');
        }
        
        calendarGrid.appendChild(dayCell);
    }
    
    // Highlight event days in the morning section
    const morningEventDays = document.querySelectorAll('.events-section:nth-of-type(1) .event-day');
    morningEventDays.forEach((day, index) => {
        if (eventDates.includes(14 + index)) { // Starting from 14.05
            day.classList.add('highlighted');
        }
    });
});

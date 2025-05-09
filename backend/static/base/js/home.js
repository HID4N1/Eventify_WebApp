
 // Simple animation for features cards on scroll
 const featureCards = document.querySelectorAll('.feature-card');
        
 const observer = new IntersectionObserver((entries) => {
     entries.forEach(entry => {
         if (entry.isIntersecting) {
             entry.target.style.opacity = 1;
             entry.target.style.transform = 'translateY(0)';
         }
     });
 }, { threshold: 0.1 });

 featureCards.forEach(card => {
     card.style.opacity = 0;
     card.style.transform = 'translateY(20px)';
     card.style.transition = 'opacity 0.6s, transform 0.6s';
     observer.observe(card);
 });

 // Smooth scrolling for navigation
 document.querySelectorAll('nav a').forEach(anchor => {
     anchor.addEventListener('click', function(e) {
         e.preventDefault();
         document.querySelector(this.getAttribute('href')).scrollIntoView({
             behavior: 'smooth'
         });
     });
 });
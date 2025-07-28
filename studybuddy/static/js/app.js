// studybuddy/static/js/app.js
document.querySelectorAll('form').forEach(form => {
    form.addEventListener('submit', () => {
        form.querySelector('button').innerHTML = 'Loading...';
    });
});
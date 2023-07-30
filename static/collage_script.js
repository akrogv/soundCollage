//Term buttons - event listeners
document.getElementById('short_Term').addEventListener('click', function() {
    window.location.href = '/collage?time_range=short_term';
});

document.getElementById('mid_Term').addEventListener('click', function() {
    window.location.href = '/collage?time_range=medium_term';
});

document.getElementById('long_Term').addEventListener('click', function() {
    window.location.href = '/collage?time_range=long_term';
});


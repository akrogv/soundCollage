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

document.getElementById('dwnld-btn').addEventListener('click', function() {
    convertCollageToImage();
});


//convert collage class into image
function convertCollageToImage() {
    var collageDiv = document.getElementById('collage');
    var collageCanvas = document.createElement('canvas');
    var context = collageCanvas.getContext('2d');

    // Set the canvas size to match the collage container size
    collageCanvas.width = collageDiv.offsetWidth;
    collageCanvas.height = collageDiv.offsetHeight;

    // Draw the entire collage onto the canvas
    var images = collageDiv.getElementsByTagName('img');
    var x = 0;
    var y = 0;
    var maxRowHeight = 0;

    for (var i = 0; i < images.length; i++) {
        var image = images[i];
        context.drawImage(image, x, y, image.width, image.height);
        x += image.width;
        maxRowHeight = Math.max(maxRowHeight, image.height);

        if (x + image.width > collageCanvas.width) {
            x = 0;
            y += maxRowHeight;
            maxRowHeight = 0;
        }
    }

    // Open the collage image in a new window
    window.open(collageCanvas.toDataURL());
}




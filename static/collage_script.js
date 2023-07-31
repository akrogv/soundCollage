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
    drawCollage2();
});

function drawCollage2() {
    var images = document.querySelectorAll('.collage img'); //nodelist of img
    var element = document.getElementById('collageContainer');//collage class
    var ctx = canvas.getContext('2d');
    images.forEach(function (image) {
        element.appendChild(image);
        console.log(element);
    });
    html2canvas(element).then(function (canvas) {
        canvas.toBlob(function (blob) {
            window.saveAs(blob, "here's the collage.png");
        });
    });
};

// Function to convert multiple images into a single one:
function drawCollage() {
    var collageContainer = document.getElementById('collageContainer');
    var canvas = document.createElement('canvas');
    var context = canvas.getContext('2d');
    canvas.width = collageContainer.offsetWidth;
    canvas.height = collageContainer.offsetHeight;

    var images = collageContainer.querySelectorAll("img");
    var x = 0;
    var y = 0;
    var maxRowHeight = 0;

    images.forEach(function (image) {
        context.drawImage(image, x, y, image.width, image.height);
        x += image.width;
        maxRowHeight = Math.max(maxRowHeight, image.height);

        if (x + image.width > canvas.width) {
            x = 0;
            y += maxRowHeight;
            maxRowHeight = 0;
        }
    });
    collageContainer.appendChild(canvas);
};

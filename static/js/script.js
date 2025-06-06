document.addEventListener('DOMContentLoaded', function() {
    const dropArea = document.getElementById('drop-area');
    const fileInput = document.getElementById('file-input');
    const preview = document.getElementById('preview');
    const previewImage = document.getElementById('preview-image');
    const submitBtn = document.getElementById('submit-btn');
    const uploadForm = document.getElementById('upload-form');

    // Handle click to upload
    dropArea.addEventListener('click', () => fileInput.click());

    // Handle drag and drop events
    ['dragenter', 'dragover', 'dragleave', 'drop'].forEach(eventName => {
        dropArea.addEventListener(eventName, preventDefaults);
        document.body.addEventListener(eventName, preventDefaults);
    });

    ['dragenter', 'dragover'].forEach(eventName => {
        dropArea.addEventListener(eventName, highlight);
    });

    ['dragleave', 'drop'].forEach(eventName => {
        dropArea.addEventListener(eventName, unhighlight);
    });

    function preventDefaults(e) {
        e.preventDefault();
        e.stopPropagation();
    }

    function highlight() {
        dropArea.classList.add('highlight');
    }

    function unhighlight() {
        dropArea.classList.remove('highlight');
    }

    // Handle dropped files
    dropArea.addEventListener('drop', handleDrop);


    // Handle selected files
    fileInput.addEventListener('change', function() {
        handleFiles(this.files);
    });

    function handleFiles(files) {
    const file = files[0];
    if (file && file.type.startsWith('image/')) {
        const reader = new FileReader();
        reader.onload = function(e) {
            previewImage.src = e.target.result;
            preview.style.display = 'block';
            dropArea.classList.add('preview-active');
            submitBtn.style.display = 'inline-block';
        }
        reader.readAsDataURL(file);
        
        // Create a new DataTransfer object and add the file
        const dataTransfer = new DataTransfer();
        dataTransfer.items.add(file);
        fileInput.files = dataTransfer.files;
    }
}


    uploadForm.addEventListener('submit', function(e) {
    e.preventDefault();
    
    if (!fileInput.files || !fileInput.files[0]) {
        alert('Please select an image first');
        return;
    }

    // Show loading state
    const submitBtn = document.getElementById('submit-btn');
    submitBtn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Analyzing...';
    submitBtn.disabled = true;

    const formData = new FormData();
    formData.append('image', fileInput.files[0]);
    formData.append('csrfmiddlewaretoken', document.querySelector('[name=csrfmiddlewaretoken]').value);

    fetch('', {
        method: 'POST',
        body: formData
    })
    .then(response => response.json())  // Changed from text() to json()
    .then(data => {
        // Create results section if it doesn't exist
        let resultsSection = document.getElementById('results-section');
        if (!resultsSection) {
            resultsSection = document.createElement('div');
            resultsSection.id = 'results-section';
            document.querySelector('.container').appendChild(resultsSection);
        }

        // Display results
        let resultsHtml = '<h2>Nutrition Results</h2>';
        data.results.forEach(item => {
            resultsHtml += `
                <div class="result-item">
                    <h3>${item.label} (${(item.confidence * 100).toFixed(1)}%)</h3>
                    ${item.nutrition ? `
                        <div class="nutrition-list">
                            <h4>${item.nutrition.name}</h4>
                            <ul>
                                ${item.nutrition.nutrients.map(nutrient => 
                                    `<li>${nutrient.nutrientName}: ${nutrient.value} ${nutrient.unitName}</li>`
                                ).join('')}
                            </ul>
                        </div>
                    ` : ''}
                </div>
            `;
        });

        resultsSection.innerHTML = resultsHtml;

        // Reset button state
        submitBtn.innerHTML = 'Analyze Food <i class="fas fa-arrow-right"></i>';
        submitBtn.disabled = false;

        // Scroll to results
        resultsSection.scrollIntoView({ behavior: 'smooth' });
        })
        .catch(error => {
            console.error('Error:', error);
            alert('Error analyzing image');
            submitBtn.innerHTML = 'Analyze Food <i class="fas fa-arrow-right"></i>';
            submitBtn.disabled = false;
        });
    });

    // Back to top functionality
    const backToTop = document.getElementById('backToTop');
    
    window.addEventListener('scroll', () => {
        if (window.pageYOffset > 300) {
            backToTop.style.display = 'flex';
            backToTop.classList.add('visible');
        } else {
            backToTop.classList.remove('visible');
            setTimeout(() => {
                if (!backToTop.classList.contains('visible')) {
                    backToTop.style.display = 'none';
                }
            }, 300);
        }
    });

    backToTop.addEventListener('click', (e) => {
        e.preventDefault();
        window.scrollTo({
            top: 0,
            behavior: 'smooth'
        });
    });


    function handleDrop(e) {
        const dt = e.dataTransfer;
        
        // Handle URLs (dragged images from the internet)
        if (dt.types.includes('text/uri-list')) {
            e.preventDefault();
            const url = dt.getData('URL');
            
            // Show loading state
            dropArea.classList.add('loading');
            
            // Fetch the image from URL
            fetch(url)
                .then(response => response.blob())
                .then(blob => {
                    // Create a File object from the blob
                    const file = new File([blob], 'dragged-image.jpg', { type: blob.type });
                    handleFiles([file]);
                    dropArea.classList.remove('loading');
                })
                .catch(error => {
                    console.error('Error fetching image:', error);
                    alert('Could not load image from URL. Please try downloading it first.');
                    dropArea.classList.remove('loading');
                });
        }
        // Handle files (dragged from computer)
        else if (dt.files && dt.files.length > 0) {
            handleFiles(dt.files);
        }
    }
    

});
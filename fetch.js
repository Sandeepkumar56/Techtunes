// 
document.getElementById('bookingForm').addEventListener('submit', function(event) {
    event.preventDefault();

    // Fetch form data
    const formData = new FormData(this);
    const formDataObject = {};
    formData.forEach((value, key) => {
        formDataObject[key] = value;
    });

    // Format data into the desired JSON format
    const bookingData = {
        Name: formDataObject.name,
        email: formDataObject.email,
        phone_num: formDataObject.phone,
        date: formDataObject.date,
        time: formDataObject.time,
        services: formDataObject.services
    };

    // Make API request with formatted data
    fetch('http://localhost:8000/booking', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(bookingData)
    })
    .then(response => response.json())
    .then(data => {
        console.log('API Response:', data);
        // Handle response as needed
    })
    .catch(error => {
        console.error('Error:', error);
        // Handle error as needed
    });
});

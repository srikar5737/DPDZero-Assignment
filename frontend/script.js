// Function to handle user registration
function registerUser() {
    const username = document.getElementById('username').value;
    const email = document.getElementById('email').value;
    const password = document.getElementById('password').value;
    const full_name = document.getElementById('full_name').value;
    const age = document.getElementById('age').value;
    const gender = document.getElementById('gender').value;

    const userData = {
        username: username,
        email: email,
        password: password,
        full_name: full_name,
        age: age,
        gender: gender
    };

    // Send the user registration data to the Flask backend
    fetch('/api/register', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(userData)
    })
    .then(response => response.json())
    .then(data => {
        // Handle the response
        if (data.status === 'success') {
            alert('User successfully registered!');
        } else {
            alert('Error: ' + data.message);
        }
    })
    .catch(error => {
        console.error('Error:', error);
    });
}

// Function to handle token generation
function generateToken() {
    const username = document.getElementById('username_token').value;
    const password = document.getElementById('password_token').value;

    const userData = {
        username: username,
        password: password
    };

    // Send the user authentication data to the Flask backend
    fetch('/api/token', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(userData)
    })
    .then(response => response.json())
    .then(data => {
        // Handle the response
        if (data.status === 'success') {
            alert('Token generated successfully! Access Token: ' + data.data.access_token);
        } else {
            alert('Error: ' + data.message);
        }
    })
    .catch(error => {
        console.error('Error:', error);
    });
}

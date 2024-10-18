document.addEventListener('DOMContentLoaded', () => {
    const registerForm = document.getElementById('registerForm');
    if (registerForm) {
        registerForm.addEventListener('submit', async (e) => {
            e.preventDefault();
            const username = document.getElementById('registerUsername').value;
            const password = document.getElementById('registerPassword').value;

            const response = await fetch('/register', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ username, password }),
            });

            const data = await response.json();
            alert(data.message || 'Registration failed!');
        });
    }

    const loginForm = document.getElementById('loginForm');
    if (loginForm) {
        loginForm.addEventListener('submit', async (e) => {
            e.preventDefault();
            const username = document.getElementById('loginUsername').value;
            const password = document.getElementById('loginPassword').value;

            const response = await fetch('/login', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ username, password }),
            });

            const data = await response.json();
            if (response.ok) {
                alert(data.message || 'Login successful!');
            } else {
                alert(data.detail || 'Login failed!');
            }
        });
    }

    const spendingForm = document.getElementById('spendingForm');
    if (spendingForm) {
        spendingForm.addEventListener('submit', async (e) => {
            e.preventDefault();

            const description = document.getElementById('description').value;
            const amount = parseFloat(document.getElementById('amount').value);
            const date = new Date(document.getElementById('date').value).toISOString();
            const currency = document.getElementById('currency').value;
            const category = document.getElementById('category').value;

            console.log({ description, amount, date, currency, category });

            const response = await fetch('/spendings/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ description, amount, date, currency, category }),
            });

            const data = await response.json();
            console.log(data);

            if (response.ok) {
                alert('Spending added successfully!');
                spendingForm.reset();
            } else {
                alert(data.detail || 'Failed to add spending!');
            }
        });
    }
});

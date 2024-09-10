document.getElementById('register-form').addEventListener('submit', function(event) {
    event.preventDefault();
    
    const formData = new FormData(this);
    
    fetch('/cadastro', {
        method: 'POST',
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        alert(data.message);
        if (data.message === 'Cadastro realizado com sucesso') {
            window.location.href = 'login.html'; // Redireciona para a página de login
        }
    })
    .catch(error => console.error('Erro:', error));
});

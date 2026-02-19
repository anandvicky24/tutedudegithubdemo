document.getElementById('todoForm').addEventListener('submit', function(e) {
    e.preventDefault();
    
    const itemName = document.getElementById('itemName').value.trim();
    const itemDescription = document.getElementById('itemDescription').value.trim();
    
    if (!itemName || !itemDescription) {
        showMessage('Please fill in all fields', 'error');
        return;
    }
    
    // Send data to backend
    fetch('/submittodoitem', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            itemName: itemName,
            itemDescription: itemDescription
        })
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            showMessage('To-Do item added successfully!', 'success');
            document.getElementById('todoForm').reset();
            addItemToList(itemName, itemDescription);
        } else {
            showMessage(data.message || 'Error adding item', 'error');
        }
    })
    .catch(error => {
        console.error('Error:', error);
        showMessage('Error connecting to server', 'error');
    });
});

function showMessage(message, type) {
    const responseDiv = document.getElementById('responseMessage');
    responseDiv.textContent = message;
    responseDiv.className = 'response-message ' + type;
    
    setTimeout(() => {
        responseDiv.className = 'response-message';
    }, 4000);
}

function addItemToList(name, description) {
    const todoList = document.getElementById('todoList');
    
    // Remove "No items yet" message if present
    if (todoList.children.length === 1 && todoList.children[0].classList.contains('empty')) {
        todoList.innerHTML = '';
    }
    
    const listItem = document.createElement('li');
    listItem.innerHTML = `<strong>${escapeHtml(name)}</strong><br><small>${escapeHtml(description)}</small>`;
    todoList.appendChild(listItem);
}

function escapeHtml(text) {
    const map = {
        '&': '&amp;',
        '<': '&lt;',
        '>': '&gt;',
        '"': '&quot;',
        "'": '&#039;'
    };
    return text.replace(/[&<>"']/g, m => map[m]);
}
const engine = document.getElementById('id_engine')
const operations = document.getElementById('id_operation')

engine?.addEventListener('change', function(event) {
    event.preventDefault()
    let engineId = engine.value;
    fetch('/get_operations_by_engine/', {
        method: 'POST',
        headers: {
            'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value,
        },
        body: JSON.stringify({'engine': engineId})
    })
    .then(response => response.json())
    .then(data => {
        if (data.operations && data.operations.length > 2) {
            const operationsArray = JSON.parse(data.operations)
            operations.innerHTML = ''
            operationsArray.forEach(operation => {
                let option = document.createElement('option')
                option.value = operation.pk
                option.text = operation.fields.title;
                if (operation.fields.selected) {
                    option.selected = true
                }
                
                operations.appendChild(option);
            });
        } else {
            alert('Операций для данной модели двигателя нет :(')
        }
    })
    .catch(error => {
        console.error('Ошибка:', error)
    })
});

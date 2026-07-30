document.addEventListener('DOMContentLoaded', function() {
    const historyList = document.getElementById('history-list');
    const historyEmpty = document.getElementById('history-empty');

    loadHistory();

    async function loadHistory() {
        try {
            const response = await fetch('/api/history');
            const data = await response.json();
            renderHistory(data.items || []);
        } catch (error) {
            renderHistory([]);
        }
    }

    function renderHistory(items) {
        historyList.innerHTML = '';

        if (items.length === 0) {
            historyEmpty.style.display = 'block';
            return;
        }

        historyEmpty.style.display = 'none';

        items.forEach(function(item) {
            const li = document.createElement('li');
            li.className = 'queue-item';

            const header = document.createElement('div');
            header.className = 'queue-item-header';

            const titleLink = document.createElement('a');
            titleLink.className = 'queue-item-title queue-item-title-link';
            titleLink.href = item.url;
            titleLink.target = '_blank';
            titleLink.rel = 'noopener noreferrer';
            titleLink.textContent = item.title;

            header.appendChild(titleLink);
            li.appendChild(header);

            const dateEl = document.createElement('p');
            dateEl.className = 'queue-item-report';
            dateEl.textContent = new Date(item.added_at).toLocaleString('zh-TW');
            li.appendChild(dateEl);

            historyList.appendChild(li);
        });
    }
});

document.addEventListener('DOMContentLoaded', function() {
    const urlInput = document.getElementById('youtube-url');
    const generateBtn = document.getElementById('generate-btn');
    const statusDiv = document.getElementById('status');
    const queueList = document.getElementById('queue-list');
    const queueEmpty = document.getElementById('queue-empty');

    loadQueue();

    generateBtn.addEventListener('click', function() {
        const url = urlInput.value.trim();

        if (!url) {
            showStatus('請輸入 YouTube 網址', 'error');
            return;
        }

        addToQueue(url);
    });

    urlInput.addEventListener('keypress', function(event) {
        if (event.key === 'Enter') {
            generateBtn.click();
        }
    });

    async function addToQueue(url) {
        setLoading(true);
        showStatus('正在取得影片資訊...', 'info');

        try {
            const response = await fetch('/api/queue', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ url }),
            });

            const data = await response.json();

            if (!response.ok) {
                showStatus(data.detail || '發生錯誤', 'error');
                return;
            }

            showStatus('已加入 Queue', 'success');
            urlInput.value = '';
            await loadQueue();
        } catch (error) {
            showStatus('網路連線失敗', 'error');
        } finally {
            setLoading(false);
        }
    }

    async function loadQueue() {
        try {
            const response = await fetch('/api/queue');
            const data = await response.json();
            renderQueue(data.items || []);
        } catch (error) {
            renderQueue([]);
        }
    }

    async function removeFromQueue(videoId) {
        try {
            await fetch('/api/queue/' + encodeURIComponent(videoId), {
                method: 'DELETE',
            });
            await loadQueue();
        } catch (error) {
            showStatus('刪除失敗', 'error');
        }
    }

    function renderQueue(items) {
        queueList.innerHTML = '';

        if (items.length === 0) {
            queueEmpty.style.display = 'block';
            return;
        }

        queueEmpty.style.display = 'none';

        items.forEach(function(item) {
            const li = document.createElement('li');
            li.className = 'queue-item';

            const info = document.createElement('div');
            info.className = 'queue-item-info';

            const title = document.createElement('span');
            title.className = 'queue-item-title';
            title.textContent = item.title;

            const status = document.createElement('span');
            status.className = 'queue-item-status';
            status.textContent = item.status;

            info.appendChild(title);
            info.appendChild(status);

            const removeBtn = document.createElement('button');
            removeBtn.className = 'queue-item-remove';
            removeBtn.textContent = '移除';
            removeBtn.addEventListener('click', function() {
                removeFromQueue(item.video_id);
            });

            li.appendChild(info);
            li.appendChild(removeBtn);
            queueList.appendChild(li);
        });
    }

    function setLoading(isLoading) {
        generateBtn.disabled = isLoading;
    }

    function showStatus(message, type) {
        statusDiv.textContent = message;
        statusDiv.className = 'status ' + type;
    }
});

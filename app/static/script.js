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

    async function generateTranscript(videoId, button) {
        button.disabled = true;
        button.textContent = '產生中...';

        try {
            const response = await fetch('/api/queue/' + encodeURIComponent(videoId) + '/transcript', {
                method: 'POST',
            });
            const data = await response.json();

            if (!response.ok) {
                showStatus(data.detail || 'Transcript 產生失敗', 'error');
                await loadQueue();
                return;
            }

            showStatus('Transcript 已產生', 'success');
            await loadQueue();
            showTranscriptPreview(videoId, data.transcript);
        } catch (error) {
            showStatus('網路連線失敗', 'error');
            await loadQueue();
        }
    }

    async function generateStudyNote(videoId, button) {
        button.disabled = true;
        button.textContent = '產生中...';

        try {
            const response = await fetch('/api/queue/' + encodeURIComponent(videoId) + '/study-note', {
                method: 'POST',
            });
            const data = await response.json();

            if (!response.ok) {
                showStatus(data.detail || 'Study Note 產生失敗', 'error');
                await loadQueue();
                return;
            }

            showStatus('Study Note 已產生', 'success');
            await loadQueue();
            showPreview(videoId, 'study-note', data.study_note);
        } catch (error) {
            showStatus('網路連線失敗', 'error');
            await loadQueue();
        }
    }

    function showTranscriptPreview(videoId, text) {
        showPreview(videoId, 'transcript', text);
    }

    function showPreview(videoId, kind, text) {
        const existing = document.querySelector('[data-preview-for="' + videoId + '-' + kind + '"]');
        if (existing) {
            existing.remove();
        }

        const li = document.querySelector('[data-video-id="' + videoId + '"]');
        if (!li) {
            return;
        }

        const pre = document.createElement('pre');
        pre.className = 'transcript-preview';
        pre.setAttribute('data-preview-for', videoId + '-' + kind);
        pre.textContent = text;
        li.appendChild(pre);
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
            li.setAttribute('data-video-id', item.video_id);

            const row = document.createElement('div');
            row.className = 'queue-item-row';

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

            const actions = document.createElement('div');
            actions.className = 'queue-item-actions';

            const hasTranscript = Boolean(item.transcript_path);
            const hasStudyNote = Boolean(item.study_note_path);

            const transcriptBtn = document.createElement('button');
            transcriptBtn.className = 'queue-item-transcript';
            transcriptBtn.textContent = hasTranscript ? '重新產生 Transcript' : '產生 Transcript';
            transcriptBtn.addEventListener('click', function() {
                generateTranscript(item.video_id, transcriptBtn);
            });
            actions.appendChild(transcriptBtn);

            if (hasTranscript) {
                const downloadTranscriptLink = document.createElement('a');
                downloadTranscriptLink.className = 'queue-item-download';
                downloadTranscriptLink.textContent = '下載 Transcript';
                downloadTranscriptLink.href = '/api/queue/' + encodeURIComponent(item.video_id) + '/transcript/download';
                actions.appendChild(downloadTranscriptLink);

                const studyNoteBtn = document.createElement('button');
                studyNoteBtn.className = 'queue-item-study-note';
                studyNoteBtn.textContent = hasStudyNote ? '重新產生 Study Note' : '產生 Study Note';
                studyNoteBtn.addEventListener('click', function() {
                    generateStudyNote(item.video_id, studyNoteBtn);
                });
                actions.appendChild(studyNoteBtn);
            }

            if (hasStudyNote) {
                const downloadStudyNoteLink = document.createElement('a');
                downloadStudyNoteLink.className = 'queue-item-download';
                downloadStudyNoteLink.textContent = '下載 Study Note';
                downloadStudyNoteLink.href = '/api/queue/' + encodeURIComponent(item.video_id) + '/study-note/download';
                actions.appendChild(downloadStudyNoteLink);
            }

            const removeBtn = document.createElement('button');
            removeBtn.className = 'queue-item-remove';
            removeBtn.textContent = '移除';
            removeBtn.addEventListener('click', function() {
                removeFromQueue(item.video_id);
            });
            actions.appendChild(removeBtn);

            row.appendChild(info);
            row.appendChild(actions);
            li.appendChild(row);
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

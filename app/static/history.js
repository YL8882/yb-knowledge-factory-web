document.addEventListener('DOMContentLoaded', function() {
    const historyList = document.getElementById('history-list');
    const historyEmpty = document.getElementById('history-empty');
    const historyStatus = document.getElementById('history-status');
    const exportAllBtn = document.getElementById('export-all-history-btn');

    loadHistory();

    if (exportAllBtn) {
        exportAllBtn.addEventListener('click', exportAllHistoryPackages);
    }

    function showStatus(message, type) {
        const icon = type === 'success' ? '✓' : type === 'error' ? '⚠' : 'ⓘ';
        historyStatus.innerHTML =
            '<span class="status-icon" aria-hidden="true">' + icon + '</span>' +
            '<span>' + message + '</span>';
        historyStatus.className = 'status-box ' + type;
    }

    function parseFilename(disposition) {
        if (!disposition) {
            return null;
        }

        const extended = disposition.match(/filename\*=[^']*''([^;]+)/i);
        if (extended) {
            try {
                return decodeURIComponent(extended[1]);
            } catch (error) {
                // fall through to the plain form below
            }
        }

        const plain = disposition.match(/filename="?([^";]+)"?/i);
        return plain ? plain[1].trim() : null;
    }

    // History Bulk Export (Sprint 5, Task 4): mirrors script.js's
    // exportAllPackages(), but hits /api/history/export-all — disk-verified
    // via history_store + find_cached_*, independent of queue_store.
    async function exportAllHistoryPackages() {
        try {
            const response = await fetch('/api/history/export-all');
            if (!response.ok) {
                const data = await response.json().catch(function() { return {}; });
                showStatus(data.detail || '匯出知識包失敗', 'error');
                return;
            }

            const filename = parseFilename(response.headers.get('Content-Disposition')) || 'YB_Knowledge_Packages.zip';
            const blob = await response.blob();
            const objectUrl = URL.createObjectURL(blob);
            const link = document.createElement('a');
            link.href = objectUrl;
            link.download = filename;
            document.body.appendChild(link);
            link.click();
            link.remove();
            URL.revokeObjectURL(objectUrl);
        } catch (error) {
            showStatus('網路連線失敗', 'error');
        }
    }

    async function loadHistory() {
        try {
            const response = await fetch('/api/history');
            const data = await response.json();
            renderHistory(data.items || []);
        } catch (error) {
            renderHistory([]);
        }
    }

    // Knowledge Package status (Sprint 5, Task 3) is derived, not stored —
    // complete only when both Transcript and Study Note files still exist on
    // disk (history_store.py itself only ever tracks video_id/title/url/date).
    function buildStatusBadge(label, exists) {
        const li = document.createElement('li');
        li.className = 'library-status-row';

        const labelEl = document.createElement('span');
        labelEl.className = 'library-status-label';
        labelEl.textContent = label;

        const badge = document.createElement('span');
        badge.className = 'queue-item-badge ' + (exists ? 'is-done' : 'is-error');
        badge.textContent = exists ? '✓ 已產生' : '⚠ 缺失';

        li.appendChild(labelEl);
        li.appendChild(badge);
        return li;
    }

    function renderHistory(items) {
        historyList.innerHTML = '';

        if (items.length === 0) {
            historyEmpty.style.display = 'block';
            return;
        }

        historyEmpty.style.display = 'none';

        items.forEach(function(item) {
            const hasTranscript = Boolean(item.transcript_exists);
            const hasStudyNote = Boolean(item.study_note_exists);
            const isComplete = hasTranscript && hasStudyNote;

            const card = document.createElement('div');
            card.className = 'library-card';

            const header = document.createElement('div');
            header.className = 'library-card-header';

            const titleLink = document.createElement('a');
            titleLink.className = 'library-card-title';
            titleLink.href = item.url;
            titleLink.target = '_blank';
            titleLink.rel = 'noopener noreferrer';
            titleLink.textContent = item.title;
            header.appendChild(titleLink);

            const dateEl = document.createElement('span');
            dateEl.className = 'library-card-date';
            dateEl.textContent = new Date(item.added_at).toLocaleDateString('zh-TW');
            header.appendChild(dateEl);

            card.appendChild(header);

            const statusList = document.createElement('ul');
            statusList.className = 'library-status-list';
            statusList.appendChild(buildStatusBadge('Transcript', hasTranscript));
            statusList.appendChild(buildStatusBadge('Study Note', hasStudyNote));
            statusList.appendChild(buildStatusBadge('Knowledge Package', isComplete));
            card.appendChild(statusList);

            // Primary action: Knowledge Package download — the main reason to
            // visit this page, so it gets its own visually prominent row,
            // separate from the secondary "open" actions below.
            if (isComplete) {
                const primaryRow = document.createElement('div');
                primaryRow.className = 'library-primary-action';

                const downloadBtn = document.createElement('a');
                downloadBtn.className = 'btn-primary library-download-btn';
                downloadBtn.href = '/api/history/' + encodeURIComponent(item.video_id) + '/export';
                downloadBtn.innerHTML = '<span aria-hidden="true">📦</span> 下載知識包';
                primaryRow.appendChild(downloadBtn);

                card.appendChild(primaryRow);
            }

            // Secondary actions: viewing individual files / going back to the
            // source video. Kept visually separate from the primary download
            // button so it doesn't compete for attention.
            const secondaryRow = document.createElement('div');
            secondaryRow.className = 'library-secondary-actions';

            if (hasTranscript) {
                const openTranscript = document.createElement('a');
                openTranscript.className = 'btn-text-link';
                openTranscript.href = '/api/history/' + encodeURIComponent(item.video_id) + '/transcript';
                openTranscript.target = '_blank';
                openTranscript.rel = 'noopener noreferrer';
                openTranscript.innerHTML = '<span aria-hidden="true">📄</span> Transcript';
                secondaryRow.appendChild(openTranscript);
            }

            if (hasStudyNote) {
                const openStudyNote = document.createElement('a');
                openStudyNote.className = 'btn-text-link';
                openStudyNote.href = '/api/history/' + encodeURIComponent(item.video_id) + '/study-note';
                openStudyNote.target = '_blank';
                openStudyNote.rel = 'noopener noreferrer';
                openStudyNote.innerHTML = '<span aria-hidden="true">🧠</span> Study Note';
                secondaryRow.appendChild(openStudyNote);
            }

            const backToYoutube = document.createElement('a');
            backToYoutube.className = 'btn-text-link';
            backToYoutube.href = item.url;
            backToYoutube.target = '_blank';
            backToYoutube.rel = 'noopener noreferrer';
            backToYoutube.innerHTML = '<span aria-hidden="true">▶</span> YouTube';
            secondaryRow.appendChild(backToYoutube);

            card.appendChild(secondaryRow);

            historyList.appendChild(card);
        });
    }
});

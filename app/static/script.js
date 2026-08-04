document.addEventListener('DOMContentLoaded', function() {
    const urlInput = document.getElementById('youtube-url');
    const generateBtn = document.getElementById('generate-btn');
    const statusDiv = document.getElementById('status');
    const queueList = document.getElementById('queue-list');
    const queueEmpty = document.getElementById('queue-empty');
    const chooseFolderBtn = document.getElementById('choose-folder-btn');
    const exportAllBtn = document.getElementById('export-all-btn');
    const downloadFolderLabel = document.getElementById('download-folder-label');
    const processingPanel = document.getElementById('processing-panel');
    const processingStagesEl = document.getElementById('processing-stages');
    const processingResultEl = document.getElementById('processing-result');
    const studyNoteDisplay = document.getElementById('study-note-display');
    const studyNoteContentEl = document.getElementById('study-note-content');
    const studyNoteDownloadBtn = document.getElementById('study-note-download-btn');

    // The video_id the processing panel is currently showing — the one most recently
    // added via the Generate button. Only one panel, so only one video is tracked.
    let trackedVideoId = null;

    // video_id whose Study Note is currently shown in the panel — guards against
    // re-fetching the same file on every poll tick while other items are busy.
    let displayedStudyNoteVideoId = null;

    // Remembered download folder (File System Access API, Chrome/Edge only). The handle
    // itself is persisted in IndexedDB so it survives a page reload; autoDownload() writes
    // straight into it once permission is confirmed, instead of prompting on every download.
    let downloadDirHandle = null;

    // Tracks which video_ids have already been auto-saved this session, so renderQueue()
    // (which re-runs on every poll tick) triggers the actual file write exactly once per
    // item instead of re-saving on every re-render.
    const autoSavedTranscripts = new Set();
    const autoSavedStudyNotes = new Set();

    const FOLDER_DB_NAME = 'ybkf-settings';
    const FOLDER_STORE_NAME = 'handles';
    const FOLDER_HANDLE_KEY = 'downloadDir';

    function openFolderDB() {
        return new Promise(function(resolve, reject) {
            const request = indexedDB.open(FOLDER_DB_NAME, 1);
            request.onupgradeneeded = function() {
                request.result.createObjectStore(FOLDER_STORE_NAME);
            };
            request.onsuccess = function() { resolve(request.result); };
            request.onerror = function() { reject(request.error); };
        });
    }

    async function saveDirHandle(handle) {
        const db = await openFolderDB();
        return new Promise(function(resolve, reject) {
            const tx = db.transaction(FOLDER_STORE_NAME, 'readwrite');
            tx.objectStore(FOLDER_STORE_NAME).put(handle, FOLDER_HANDLE_KEY);
            tx.oncomplete = resolve;
            tx.onerror = function() { reject(tx.error); };
        });
    }

    async function loadDirHandle() {
        const db = await openFolderDB();
        return new Promise(function(resolve, reject) {
            const tx = db.transaction(FOLDER_STORE_NAME, 'readonly');
            const req = tx.objectStore(FOLDER_STORE_NAME).get(FOLDER_HANDLE_KEY);
            req.onsuccess = function() { resolve(req.result || null); };
            req.onerror = function() { reject(req.error); };
        });
    }

    function updateFolderLabel() {
        downloadFolderLabel.textContent = downloadDirHandle
            ? '目前下載資料夾：' + downloadDirHandle.name
            : '';
        chooseFolderBtn.textContent = downloadDirHandle
            ? '📁 變更下載資料夾'
            : '📁 設定下載資料夾';
    }

    async function ensureDirPermission(handle) {
        const opts = { mode: 'readwrite' };
        if ((await handle.queryPermission(opts)) === 'granted') {
            return true;
        }
        return (await handle.requestPermission(opts)) === 'granted';
    }

    async function chooseDownloadFolder() {
        if (!window.showDirectoryPicker) {
            showStatus('此瀏覽器不支援選擇下載資料夾（請改用 Chrome 或 Edge）', 'error');
            return;
        }
        try {
            const handle = await window.showDirectoryPicker();
            downloadDirHandle = handle;
            await saveDirHandle(handle);
            updateFolderLabel();
            showStatus('已設定下載資料夾：' + handle.name, 'success');
        } catch (error) {
            if (!(error && error.name === 'AbortError')) {
                showStatus('設定下載資料夾失敗', 'error');
            }
        }
    }

    chooseFolderBtn.addEventListener('click', chooseDownloadFolder);
    exportAllBtn.addEventListener('click', exportAllPackages);

    // Best-effort restore on page load: only reuse a remembered folder if permission is
    // still silently granted (queryPermission doesn't prompt); otherwise the user just
    // picks again via the button, no worse than before this feature existed.
    (async function restoreDownloadFolder() {
        try {
            const handle = await loadDirHandle();
            if (handle && (await handle.queryPermission({ mode: 'readwrite' })) === 'granted') {
                downloadDirHandle = handle;
                updateFolderLabel();
            }
        } catch (error) {
            // IndexedDB unavailable or handle no longer valid — ignore, nothing to restore.
        }
    })();

    // Auto-starts Transcript download when arriving from the "YB Learn" Chrome
    // extension (?url=... on the page load), which opens this page right after
    // capturing the current YouTube video — no further click needed, matching
    // the YouTube -> YB Learn -> Transcript flow. Manual paste into the input
    // still requires the explicit "加入暫存區" click, unchanged.
    (function autoStartFromExtension() {
        const capturedUrl = new URLSearchParams(window.location.search).get('url');
        if (capturedUrl) {
            urlInput.value = capturedUrl;
            addToQueue(capturedUrl);
        }
    })();

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

            // Auto-start: the backend immediately joins this item to its single
            // sequential pipeline queue (see main.py _enqueue_for_processing). If
            // other items are still ahead of it, it just waits its turn — no click
            // needed either way.
            showStatus('已加入暫存區，將依序自動產生 Transcript、Study Note 並下載...', 'success');
            urlInput.value = '';
            trackedVideoId = data.video_id;
            displayedStudyNoteVideoId = null;
            studyNoteDisplay.classList.add('is-hidden');
            studyNoteContentEl.textContent = '';
            await loadQueue();
            pollPipelineProgress(data.video_id);
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
            const items = data.items || [];
            renderQueue(items);
            renderProcessingPanel(items);
            return items;
        } catch (error) {
            renderQueue([]);
            renderProcessingPanel([]);
            return [];
        }
    }

    // True while the fully-automatic backend pipeline (Downloading -> Transcribing ->
    // Transcript Ready -> Generating) still has real work in flight, or hasn't
    // started yet but hasn't failed either. False once it reaches a terminal state
    // (Study Note Ready, or a failure recorded via last_error — nothing
    // auto-retries a failure, so polling forever on a failed "Queued" item would
    // be wasted work).
    //
    // "Transcript Ready" is included here even though the backend normally
    // passes through it near-instantly on its way to "Generating"
    // (or straight to "Study Note Ready" on a cache hit) — without it, a poll tick
    // that happens to land exactly on that transitional status would stop polling
    // one step early via clearInterval() in pollPipelineProgress(), before Study
    // Note Ready is ever observed, leaving the UI stuck showing "Generating Study
    // Note" forever with nothing left to refresh it.
    function isPipelineActive(item) {
        if (item.status === 'Downloading' || item.status === 'Transcribing'
            || item.status === 'Transcript Ready' || item.status === 'Generating') {
            return true;
        }
        return item.status === 'Queued' && !item.last_error;
    }

    // The backend auto-runs the whole Transcript -> Study Note pipeline as a single
    // background task right after a video is added — this just keeps the queue
    // polling/re-rendering live until that specific item reaches a terminal state.
    function pollPipelineProgress(videoId) {
        const timer = setInterval(async function() {
            const items = await loadQueue();
            const item = items.find(function(i) { return i.video_id === videoId; });
            if (!item || !isPipelineActive(item)) {
                clearInterval(timer);
            }
        }, 1500);
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

    // Recovery action for a failed item — resumes from wherever it actually left
    // off (the backend figures out whether to redo Transcript or just Study Note),
    // using the video's already-known URL. No need to paste it again.
    async function retryProcessing(videoId) {
        try {
            const response = await fetch('/api/queue/' + encodeURIComponent(videoId) + '/retry', {
                method: 'POST',
            });
            if (!response.ok) {
                showStatus('重試失敗', 'error');
                return;
            }
            showStatus('正在重試...', 'info');
            await loadQueue();
            pollPipelineProgress(videoId);
        } catch (error) {
            showStatus('網路連線失敗', 'error');
        }
    }

    // Parses a Content-Disposition header, preferring the RFC 5987 extended form
    // (filename*=UTF-8''%E4%BD%A0...) that FastAPI/Starlette sends for non-ASCII
    // filenames (e.g. Chinese video titles) over the plain filename="..." form.
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

    // Unconditionally downloads a file the moment it's ready — no button, no click.
    // If a folder has been remembered (chooseDownloadFolder()), it writes straight
    // into it silently. Otherwise it falls back to a normal browser download
    // (triggers the browser's own "ask where to save" prompt if the user has that
    // setting on; no interactive save-picker is attempted here since there is no
    // user click backing this call to satisfy that API's gesture requirement).
    async function autoDownload(url, fallbackName) {
        let response;
        try {
            response = await fetch(url);
        } catch (error) {
            return false;
        }

        if (!response.ok) {
            return false;
        }

        const filename = parseFilename(response.headers.get('Content-Disposition')) || fallbackName;
        const blob = await response.blob();

        if (downloadDirHandle) {
            try {
                if (await ensureDirPermission(downloadDirHandle)) {
                    const fileHandle = await downloadDirHandle.getFileHandle(filename, { create: true });
                    const writable = await fileHandle.createWritable();
                    await writable.write(blob);
                    await writable.close();
                    return true;
                }
            } catch (error) {
                // Remembered folder no longer usable (revoked, deleted, etc.) — fall
                // through to the plain browser download below.
            }
        }

        const objectUrl = URL.createObjectURL(blob);
        const link = document.createElement('a');
        link.href = objectUrl;
        link.download = filename;
        document.body.appendChild(link);
        link.click();
        link.remove();
        URL.revokeObjectURL(objectUrl);
        return true;
    }

    // Bulk Knowledge Package Export (Sprint 5, Task 2): unlike autoDownload()
    // above (best-effort, silent failure), this surfaces a clear message via
    // showStatus() on failure — e.g. no completed items yet, or the backend
    // refused because a candidate item's Transcript.md / Study_Note.md turned
    // out to be missing on disk (all-or-nothing, no partial zip produced).
    async function exportAllPackages() {
        try {
            const response = await fetch('/api/queue/export-all');
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

    // Maps the backend's queue status string to per-step checklist states,
    // mirroring the Processing screen's step-by-step workflow indicator.
    function stepStates(status) {
        switch (status) {
            case 'Downloading':
            case 'Transcribing':
                return { transcript: 'active', studyNote: 'pending' };
            case 'Transcript Ready':
                return { transcript: 'done', studyNote: 'pending' };
            case 'Generating':
                return { transcript: 'done', studyNote: 'active' };
            case 'Study Note Ready':
                return { transcript: 'done', studyNote: 'done' };
            default:
                return { transcript: 'pending', studyNote: 'pending' };
        }
    }

    function stepIcon(state) {
        if (state === 'done') return '✓';
        if (state === 'active') return '⏳';
        return '○';
    }

    // Progress bar for the active step. When the backend has a real percentage
    // (long videos: yt-dlp download progress, or Whisper segment position against
    // total audio duration for transcription) it renders a determinate fill and an
    // ETA line under it. Otherwise (e.g. Study Note generation, a single Gemini
    // call with no sub-progress) it falls back to the honest indeterminate "working"
    // animation rather than inventing a percentage that isn't real.
    function buildProgressBar(percent, etaSeconds) {
        const wrap = document.createElement('div');

        const bar = document.createElement('div');
        bar.className = 'progress-bar';
        const fill = document.createElement('div');
        fill.className = 'progress-bar-fill';

        if (typeof percent === 'number') {
            bar.classList.add('is-determinate');
            fill.style.width = Math.max(0, Math.min(100, percent)) + '%';
        }

        bar.appendChild(fill);
        wrap.appendChild(bar);

        if (typeof percent === 'number') {
            const label = document.createElement('p');
            label.className = 'progress-eta';
            const etaText = formatEta(etaSeconds);
            label.textContent = percent + '%' + (etaText ? '，預估剩餘 ' + etaText : '');
            wrap.appendChild(label);
        }

        return wrap;
    }

    // Renders a seconds count as a short human-readable duration, or '' when the
    // backend doesn't have enough data yet to estimate one (e.g. the very first
    // progress tick, before any elapsed-time-per-fraction-done ratio exists).
    function formatEta(etaSeconds) {
        if (typeof etaSeconds !== 'number' || !isFinite(etaSeconds) || etaSeconds < 0) {
            return '';
        }
        const total = Math.round(etaSeconds);
        if (total < 60) {
            return total + ' 秒';
        }
        const minutes = Math.floor(total / 60);
        const seconds = total % 60;
        return seconds === 0 ? minutes + ' 分' : minutes + ' 分 ' + seconds + ' 秒';
    }

    function buildStepChecklist(status) {
        const states = stepStates(status);
        const list = document.createElement('ol');
        list.className = 'step-checklist';

        [
            { key: 'transcript', label: 'Transcript' },
            { key: 'studyNote', label: 'Study Note' },
        ].forEach(function(step) {
            const state = states[step.key];
            const li = document.createElement('li');
            li.className = 'step is-' + state;

            const icon = document.createElement('span');
            icon.className = 'step-icon';
            icon.textContent = stepIcon(state);

            li.appendChild(icon);
            li.appendChild(document.createTextNode(step.label));
            list.appendChild(li);
        });

        return list;
    }

    // Display State Mapping: the backend's internal status strings
    // (queue_store / main.py) are untouched — this is a UI-only presentation
    // layer translating them into the Job State vocabulary the Queue UI shows.
    // Backend Internal State -> Display State:
    //   Queued           -> Waiting
    //   Downloading      -> Processing
    //   Transcribing     -> Processing
    //   Transcript Ready -> Generating Study Note
    //   Generating       -> Generating Study Note
    //   Study Note Ready -> Completed
    //   (last_error set) -> Error
    const DISPLAY_STATE_MAP = {
        'Queued': 'Waiting',
        'Downloading': 'Processing',
        'Transcribing': 'Processing',
        'Transcript Ready': 'Generating Study Note',
        'Generating': 'Generating Study Note',
        'Study Note Ready': 'Completed',
    };

    function displayState(item) {
        if (item.last_error) {
            return 'Error';
        }
        return DISPLAY_STATE_MAP[item.status] || item.status;
    }

    // Human-readable label for last_error_stage, used in the per-item completion /
    // failure report line.
    const STAGE_REPORT_LABELS = {
        download: '下載 YouTube 影片',
        transcript: '產生逐字稿',
        studynote: '產生 Study Note',
    };

    function buildReportLine(item, hasTranscript, hasStudyNote) {
        const p = document.createElement('p');

        if (item.last_error) {
            const stageLabel = STAGE_REPORT_LABELS[item.last_error_stage] || '處理';
            p.className = 'queue-item-report is-error';
            p.textContent = '❌ 【' + stageLabel + '】失敗：' + item.last_error;
            return p;
        }

        if (hasStudyNote) {
            p.className = 'queue-item-report is-success';
            p.textContent = '✅ 已完成：Transcript、Study Note 已自動下載，可以刪除釋放暫存區空間';
            return p;
        }

        if (hasTranscript) {
            // Transient state — Study Note generation auto-follows Transcript
            // (see main.py _auto_generate_transcript), so this only shows briefly.
            p.className = 'queue-item-report';
            p.textContent = '✓ Transcript 已完成並下載，Study Note 產生中...';
            return p;
        }

        return null;
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

            const header = document.createElement('div');
            header.className = 'queue-item-header';

            const title = document.createElement('a');
            title.className = 'queue-item-title queue-item-title-link';
            title.href = item.url;
            title.target = '_blank';
            title.rel = 'noopener noreferrer';
            title.textContent = item.title;

            const hasTranscript = Boolean(item.transcript_path);
            const isWaitingInLine = item.status === 'Queued' && !hasTranscript && !item.last_error;

            // Everything now starts automatically on add (see main.py
            // _enqueue_for_processing) and runs through one sequential pipeline, so
            // "Waiting" just means "waiting its turn" — a plain status label, not a
            // call to action. Badge text uses the Display State Mapping above;
            // badge color/class is still driven by the underlying backend status.
            const badge = document.createElement('span');
            badge.className = 'queue-item-badge';
            if (item.last_error) {
                badge.classList.add('is-error');
            } else if (isWaitingInLine) {
                badge.classList.add('is-waiting');
            } else if (item.status === 'Downloading' || item.status === 'Transcribing' || item.status === 'Generating') {
                badge.classList.add('is-active');
            } else if (item.status === 'Transcript Ready' || item.status === 'Study Note Ready') {
                badge.classList.add('is-done');
            }
            badge.textContent = displayState(item);

            const removeBtn = document.createElement('button');
            removeBtn.className = 'queue-item-remove';
            removeBtn.type = 'button';
            removeBtn.innerHTML = '<span aria-hidden="true">✕</span>';
            removeBtn.setAttribute('aria-label', '刪除');
            removeBtn.title = '刪除';
            removeBtn.addEventListener('click', function() {
                removeFromQueue(item.video_id);
            });

            header.appendChild(title);
            header.appendChild(badge);
            header.appendChild(removeBtn);

            li.appendChild(header);

            if (item.summary) {
                const summaryEl = document.createElement('p');
                summaryEl.className = 'queue-item-summary';
                summaryEl.textContent = item.summary;
                li.appendChild(summaryEl);
            }

            const hasStudyNote = Boolean(item.study_note_path);
            // Export button eligibility (Sprint 5, Task 5): disk-verified via
            // transcript_exists/study_note_exists, separate from hasTranscript/
            // hasStudyNote above (which reflect queue_store's pipeline-progress
            // path fields and drive the status badge/checklist/report line —
            // untouched here since that's workflow display, not export gating).
            const canExportPackage = Boolean(item.transcript_exists) && Boolean(item.study_note_exists);
            const isBusy = item.status === 'Downloading' || item.status === 'Transcribing' || item.status === 'Generating';

            if (isBusy) {
                li.appendChild(buildProgressBar(item.progress_percent, item.eta_seconds));
            }

            li.appendChild(buildStepChecklist(item.status));

            const reportLine = buildReportLine(item, hasTranscript, hasStudyNote);
            if (reportLine) {
                li.appendChild(reportLine);
            }

            if (item.last_error) {
                const retryBtn = document.createElement('button');
                retryBtn.className = 'queue-item-retry';
                retryBtn.type = 'button';
                retryBtn.innerHTML = '<span aria-hidden="true">🔄</span> 重試';
                retryBtn.addEventListener('click', function() {
                    retryProcessing(item.video_id);
                });
                li.appendChild(retryBtn);
            }

            // Knowledge Package Export (Sprint 5, Task 1): manual, separate from the
            // auto-download of the individual Transcript.md / Study_Note.md files
            // below — zips both into one <Video Title>/ package on click. Gated on
            // canExportPackage (Task 5), not hasStudyNote, so the button doesn't
            // appear for a stale queue_store record whose file is gone from disk.
            if (canExportPackage) {
                const exportBtn = document.createElement('a');
                exportBtn.className = 'queue-item-export';
                exportBtn.href = '/api/queue/' + encodeURIComponent(item.video_id) + '/export';
                exportBtn.innerHTML = '<span aria-hidden="true">📦</span> 下載知識包';
                li.appendChild(exportBtn);
            }

            queueList.appendChild(li);

            // Unconditional auto-download the moment each file is ready — no button,
            // no click. autoSavedTranscripts/autoSavedStudyNotes make sure this only
            // actually fires once per item per session, even though renderQueue()
            // re-runs on every poll tick while other items are still processing.
            if (hasTranscript && !autoSavedTranscripts.has(item.video_id)) {
                autoSavedTranscripts.add(item.video_id);
                const transcriptDownloadUrl = '/api/queue/' + encodeURIComponent(item.video_id) + '/transcript/download';
                const transcriptFilename = 'TN_' + item.title + '_' + item.video_id + '.md';
                autoDownload(transcriptDownloadUrl, transcriptFilename).then(function(ok) {
                    if (!ok) autoSavedTranscripts.delete(item.video_id);
                });
            }

            if (hasStudyNote && !autoSavedStudyNotes.has(item.video_id)) {
                autoSavedStudyNotes.add(item.video_id);
                const studyNoteDownloadUrl = '/api/queue/' + encodeURIComponent(item.video_id) + '/study-note/download';
                const studyNoteFilename = 'SN_' + item.title + '_' + item.video_id + '.md';
                autoDownload(studyNoteDownloadUrl, studyNoteFilename).then(function(ok) {
                    if (!ok) autoSavedStudyNotes.delete(item.video_id);
                });
            }
        });
    }

    const PROCESSING_STAGES = [
        { key: 'download', icon: '📥', label: '正在下載 YouTube 影片' },
        { key: 'transcript', icon: '🎤', label: '正在產生逐字稿' },
        { key: 'studynote', icon: '🧠', label: '正在產生 Study Note' },
        { key: 'prepare', icon: '📄', label: '正在準備下載檔案' },
    ];

    // Derives each stage's state purely from real backend fields (status /
    // transcript_path / study_note_path / last_error / last_error_stage) — no
    // fabricated percentages, no timers. "download" and "transcript" are genuinely
    // distinct statuses the backend now reports; "prepare" has no separate async
    // step of its own (the file write is instant, part of reaching a "Ready" status),
    // so it simply reflects "done" once that Ready status is reached.
    function computeStageStates(item) {
        const hasTranscript = Boolean(item.transcript_path);
        const hasStudyNote = Boolean(item.study_note_path);
        const failedStage = item.last_error ? item.last_error_stage : '';

        return {
            download: failedStage === 'download' ? 'failed'
                : item.status === 'Downloading' ? 'active'
                : (hasTranscript || item.status === 'Transcribing') ? 'done'
                : 'pending',
            transcript: failedStage === 'transcript' ? 'failed'
                : item.status === 'Transcribing' ? 'active'
                : hasTranscript ? 'done'
                : 'pending',
            studynote: failedStage === 'studynote' ? 'failed'
                : item.status === 'Generating' ? 'active'
                : hasStudyNote ? 'done'
                : 'pending',
            prepare: (item.status === 'Transcript Ready' || item.status === 'Study Note Ready') ? 'done' : 'pending',
        };
    }

    // Fetches and shows the Study Note body inline once it's ready, and points the
    // download button at the same file. Guarded by displayedStudyNoteVideoId so it
    // only fetches once per item, even though renderProcessingPanel() re-runs on
    // every poll tick. The file is already auto-downloaded separately (see
    // autoDownload() in renderQueue) — this is just for on-page display.
    //
    // Workspace previews Study Note only — Transcript is an intermediate
    // product, still auto-downloaded as Transcript.md but not shown.
    async function maybeDisplayStudyNote(item) {
        if (!item.study_note_path || displayedStudyNoteVideoId === item.video_id) {
            return;
        }
        displayedStudyNoteVideoId = item.video_id;

        // Reads the already-generated Study_Note.md file straight off disk via
        // the existing download endpoint — never calls Gemini or regenerates
        // anything, this is display-only.
        const downloadUrl = '/api/queue/' + encodeURIComponent(item.video_id) + '/study-note/download';
        try {
            const response = await fetch(downloadUrl);
            if (!response.ok) {
                // Reset the guard on failure so the next poll tick retries
                // instead of giving up on this video_id forever — previously
                // this returned without resetting displayedStudyNoteVideoId, so
                // a single transient failure (e.g. the file briefly not
                // readable) permanently blocked the Preview from ever showing,
                // even once the file was fine.
                displayedStudyNoteVideoId = null;
                return;
            }
            studyNoteContentEl.textContent = await response.text();
            studyNoteDownloadBtn.href = downloadUrl;
            studyNoteDisplay.classList.remove('is-hidden');
        } catch (error) {
            // Same reasoning as above — network hiccup shouldn't permanently
            // block the Preview from ever retrying.
            displayedStudyNoteVideoId = null;
        }
    }

    function renderProcessingPanel(items) {
        const item = trackedVideoId ? items.find(function(i) { return i.video_id === trackedVideoId; }) : null;

        if (!item) {
            processingPanel.classList.add('is-hidden');
            return;
        }

        processingPanel.classList.remove('is-hidden');
        processingStagesEl.innerHTML = '';
        maybeDisplayStudyNote(item);

        const states = computeStageStates(item);
        let hasActive = false;
        let hasFailed = false;
        let failedStageConfig = null;

        PROCESSING_STAGES.forEach(function(stage) {
            const state = states[stage.key];
            if (state === 'active') hasActive = true;
            if (state === 'failed') { hasFailed = true; failedStageConfig = stage; }

            const li = document.createElement('li');
            li.className = 'processing-stage is-' + state;

            const icon = document.createElement('span');
            icon.className = 'processing-stage-icon';
            icon.setAttribute('aria-hidden', 'true');
            icon.textContent = stage.icon;

            const label = document.createElement('span');
            label.className = 'processing-stage-label';
            label.textContent = stage.label;

            const statusEl = document.createElement('span');
            statusEl.className = 'processing-stage-status';
            if (state === 'done') {
                statusEl.innerHTML = '<span aria-hidden="true">✓</span>';
            } else if (state === 'active') {
                statusEl.innerHTML = '<span class="processing-spinner" aria-hidden="true"></span>';
            } else if (state === 'failed') {
                statusEl.innerHTML = '<span aria-hidden="true">✕</span>';
            }

            li.appendChild(icon);
            li.appendChild(label);
            li.appendChild(statusEl);
            processingStagesEl.appendChild(li);
        });

        if (hasFailed) {
            processingResultEl.textContent = '❌ 【' + failedStageConfig.label + '】失敗：' + (item.last_error || '未知錯誤');
            processingResultEl.className = 'processing-result is-error';
        } else if (!hasActive && states.studynote === 'done') {
            processingResultEl.textContent = '✓ 完成：Transcript、Study Note 已產生並自動下載';
            processingResultEl.className = 'processing-result is-success';
        } else if (hasActive && typeof item.progress_percent === 'number') {
            // Real percentage from the backend (download bytes, or Whisper segment
            // position against total audio duration) — a long video processes in
            // visible chunks instead of sitting at an unexplained spinner.
            const etaText = formatEta(item.eta_seconds);
            processingResultEl.textContent = item.progress_percent + '%' + (etaText ? '，預估剩餘 ' + etaText : '');
            processingResultEl.className = 'processing-result';
        } else {
            processingResultEl.textContent = '';
            processingResultEl.className = 'processing-result';
        }
    }

    function setLoading(isLoading) {
        generateBtn.disabled = isLoading;
    }

    function showStatus(message, type) {
        const icon = type === 'success' ? '✓' : type === 'error' ? '⚠' : 'ⓘ';
        statusDiv.innerHTML =
            '<span class="status-icon" aria-hidden="true">' + icon + '</span>' +
            '<span>' + message + '</span>';
        statusDiv.className = 'status-box ' + type;
    }
});

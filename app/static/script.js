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

    // Rapid Learning Engine (Sprint 7, Task 1): One Sentence + Knowledge Outline
    // text keyed by video_id, populated once fetched/generated. renderQueue()
    // rebuilds every <li> from scratch on each poll tick, so a per-card DOM
    // reference can't survive across renders — this cache is what lets a card
    // render its expanded content synchronously instead of re-fetching (or
    // losing) it on every re-render.
    const knowledgeOutlineCache = new Map();

    // Guards fetchKnowledgeOutlineIntoCache() so an item whose knowledge_outline_path
    // is already set (generated in an earlier session, not yet in this session's
    // cache) doesn't get re-fetched on every poll tick while the first fetch is
    // still in flight.
    const knowledgeOutlineFetchInFlight = new Set();

    // Quick Learn Layer (Sprint 7, Task 2): video_ids whose full Knowledge
    // Outline is currently expanded — a pure UI-state set (no fetch behind
    // it), consulted on every renderQueue() rebuild so the toggle survives a
    // re-render triggered by an unrelated action elsewhere in the list.
    const expandedKnowledgeOutlineCards = new Set();

    // Learning Blueprint Engine (Sprint 7, Task 3): raw Learning Blueprint
    // text keyed by video_id. Independent of knowledgeOutlineCache above —
    // this is a separate, additive artifact, not a replacement (that switch
    // is Task 4's job). Same cache-across-renders reasoning as Task 1.
    const learningBlueprintCache = new Map();

    // Guards fetchLearningBlueprintIntoCache() the same way
    // knowledgeOutlineFetchInFlight guards its Knowledge Outline counterpart.
    const learningBlueprintFetchInFlight = new Set();

    // Teach Back (Sprint 7, Task 5): structured Teach Back JSON keyed by
    // video_id. Same cache-across-renders reasoning as learningBlueprintCache.
    const teachBackCache = new Map();

    // Guards fetchTeachBackIntoCache() the same way learningBlueprintFetchInFlight
    // guards its Learning Blueprint counterpart.
    const teachBackFetchInFlight = new Set();

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

            // Rapid Learning Engine (Sprint 7, Task 1): per-card, not a shared
            // page-level panel — appears once Study Note is ready (Queue stays
            // a pure inbox; this is where "learning" starts), expands in place
            // on this same card, never navigates elsewhere on the page.
            if (hasStudyNote) {
                if (knowledgeOutlineCache.has(item.video_id)) {
                    li.appendChild(buildRapidLearningSection(item.video_id, knowledgeOutlineCache.get(item.video_id)));
                } else if (item.knowledge_outline_path) {
                    fetchKnowledgeOutlineIntoCache(item.video_id);
                } else {
                    const rapidLearningBtn = document.createElement('button');
                    rapidLearningBtn.className = 'queue-item-rapid-learning';
                    rapidLearningBtn.type = 'button';
                    rapidLearningBtn.innerHTML = '<span aria-hidden="true">🧠</span> 開始快速學習';
                    rapidLearningBtn.addEventListener('click', function() {
                        startRapidLearning(item.video_id, rapidLearningBtn);
                    });
                    li.appendChild(rapidLearningBtn);
                }
            }

            // Learning Blueprint Engine (Sprint 7, Task 3): independent
            // additive button, same hasStudyNote gate as Rapid Learning above
            // but its own trigger — doesn't require Knowledge Outline to
            // already exist. MVP display only (raw text block); UI/reading
            // experience polish is Task 4's job.
            if (hasStudyNote) {
                if (learningBlueprintCache.has(item.video_id)) {
                    li.appendChild(buildLearningBlueprintSection(item.video_id, learningBlueprintCache.get(item.video_id)));
                } else if (item.learning_blueprint_path) {
                    fetchLearningBlueprintIntoCache(item.video_id);
                } else {
                    const blueprintBtn = document.createElement('button');
                    blueprintBtn.className = 'queue-item-rapid-learning';
                    blueprintBtn.type = 'button';
                    blueprintBtn.innerHTML = '<span aria-hidden="true">🗺️</span> 建立知識架構';
                    blueprintBtn.addEventListener('click', function() {
                        startLearningBlueprint(item.video_id, blueprintBtn);
                    });
                    li.appendChild(blueprintBtn);
                }
            }

            // Teach Back (Sprint 7, Task 5): second Knowledge Structure Engine
            // Output, generated FROM the Learning Blueprint — button only
            // appears once a Learning Blueprint exists (cached client-side or
            // already on disk), mirroring the hasStudyNote gate pattern above.
            const hasLearningBlueprint = learningBlueprintCache.has(item.video_id) || Boolean(item.learning_blueprint_path);
            if (hasLearningBlueprint) {
                if (teachBackCache.has(item.video_id)) {
                    li.appendChild(buildTeachBackSection(item.video_id, teachBackCache.get(item.video_id)));
                } else if (item.teach_back_path) {
                    fetchTeachBackIntoCache(item.video_id);
                } else {
                    const teachBackBtn = document.createElement('button');
                    teachBackBtn.className = 'queue-item-rapid-learning';
                    teachBackBtn.type = 'button';
                    teachBackBtn.innerHTML = '<span aria-hidden="true">📝</span> 開始 Teach Back';
                    teachBackBtn.addEventListener('click', function() {
                        startTeachBack(item.video_id, teachBackBtn);
                    });
                    li.appendChild(teachBackBtn);
                }
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

    // Rapid Learning Engine (Sprint 7, Task 1): splits the single Markdown blob
    // the backend returns (# One Sentence + # Knowledge Outline headers) into
    // the two sections, so each can be rendered as its own labeled block on
    // the card instead of one undifferentiated text dump.
    function parseKnowledgeOutline(rawText) {
        const oneSentenceMatch = rawText.match(/#\s*One Sentence\s*\n+([\s\S]*?)(?=\n#\s*Knowledge Outline|$)/i);
        const outlineMatch = rawText.match(/#\s*Knowledge Outline\s*\n+([\s\S]*)/i);
        return {
            oneSentence: oneSentenceMatch ? oneSentenceMatch[1].trim() : rawText.trim(),
            knowledgeOutline: outlineMatch ? outlineMatch[1].trim() : '',
        };
    }

    // Manual, opt-in trigger for One Sentence + Knowledge Outline — bound to
    // one specific card's button. Deliberately NOT automatic on Queue
    // completion (Queue is a pure inbox, "learning" only starts on click).
    // Caches the result by video_id and re-renders the whole Queue list on
    // success — cards are rebuilt from scratch on every render, so there's no
    // stable per-card DOM node to patch directly once the fetch resolves.
    async function startRapidLearning(videoId, button) {
        button.disabled = true;
        try {
            const response = await fetch(
                '/api/queue/' + encodeURIComponent(videoId) + '/knowledge-outline',
                { method: 'POST' }
            );
            const data = await response.json();
            if (!response.ok) {
                showStatus(data.detail || '產生知識輪廓失敗', 'error');
                button.disabled = false;
                return;
            }
            knowledgeOutlineCache.set(videoId, data.knowledge_outline);
            await loadQueue();
        } catch (error) {
            showStatus('網路連線失敗', 'error');
            button.disabled = false;
        }
    }

    // Revisiting an item whose Knowledge Outline was already generated in an
    // earlier session (knowledge_outline_path set, but not yet in this
    // session's client-side cache) — fetches it once (server-side cache hit
    // via find_cached_knowledge_outline(), no Gemini call) and re-renders.
    async function fetchKnowledgeOutlineIntoCache(videoId) {
        if (knowledgeOutlineFetchInFlight.has(videoId)) {
            return;
        }
        knowledgeOutlineFetchInFlight.add(videoId);
        try {
            const response = await fetch(
                '/api/queue/' + encodeURIComponent(videoId) + '/knowledge-outline',
                { method: 'POST' }
            );
            if (!response.ok) {
                return;
            }
            const data = await response.json();
            knowledgeOutlineCache.set(videoId, data.knowledge_outline);
            await loadQueue();
        } catch (error) {
            // Silent — next poll tick (or manual refresh) retries naturally,
            // same reasoning as the other cache-miss fetches in this file.
        } finally {
            knowledgeOutlineFetchInFlight.delete(videoId);
        }
    }

    // Learning Blueprint Engine (Sprint 7, Task 3): manual, opt-in trigger —
    // mirrors startRapidLearning()'s shape but hits the separate
    // /learning-blueprint endpoint and its own cache.
    async function startLearningBlueprint(videoId, button) {
        button.disabled = true;
        try {
            const response = await fetch(
                '/api/queue/' + encodeURIComponent(videoId) + '/learning-blueprint',
                { method: 'POST' }
            );
            const data = await response.json();
            if (!response.ok) {
                showStatus(data.detail || '產生 Learning Blueprint 失敗', 'error');
                button.disabled = false;
                return;
            }
            learningBlueprintCache.set(videoId, data.learning_blueprint);
            await loadQueue();
        } catch (error) {
            showStatus('網路連線失敗', 'error');
            button.disabled = false;
        }
    }

    // Revisiting an item whose Learning Blueprint was already generated in an
    // earlier session — same reasoning as fetchKnowledgeOutlineIntoCache().
    async function fetchLearningBlueprintIntoCache(videoId) {
        if (learningBlueprintFetchInFlight.has(videoId)) {
            return;
        }
        learningBlueprintFetchInFlight.add(videoId);
        try {
            const response = await fetch(
                '/api/queue/' + encodeURIComponent(videoId) + '/learning-blueprint',
                { method: 'POST' }
            );
            if (!response.ok) {
                return;
            }
            const data = await response.json();
            learningBlueprintCache.set(videoId, data.learning_blueprint);
            await loadQueue();
        } catch (error) {
            // Silent — next poll tick (or manual refresh) retries naturally.
        } finally {
            learningBlueprintFetchInFlight.delete(videoId);
        }
    }

    // Learning Blueprint Renderer (Sprint 7, Task 4): dispatches on
    // structure_type to a shape-specific layout instead of dumping raw JSON
    // (Task 3's MVP display). Pure presentation — consumes the same Knowledge
    // JSON Task 3 already produces/caches, never calls Gemini, never mutates
    // data. All AI-generated text goes through textContent (never innerHTML)
    // since it's untrusted model output.
    const KNOWLEDGE_STRUCTURE_RENDERERS = {
        flow: renderFlowStructure,
        cause_effect: renderCauseEffectStructure,
        classification: renderClassificationStructure,
        decision: renderDecisionStructure,
        comparison: renderComparisonStructure,
        timeline: renderTimelineStructure,
        problem_solution: renderProblemSolutionStructure,
        generic: renderGenericStructure,
    };

    function renderFlowStructure(content) {
        const el = document.createElement('div');
        el.className = 'kse-flow';
        (content.steps || []).forEach(function(step, index) {
            if (index > 0) {
                const arrow = document.createElement('div');
                arrow.className = 'kse-flow-arrow';
                arrow.textContent = '↓';
                el.appendChild(arrow);
            }
            const stepEl = document.createElement('div');
            stepEl.className = 'kse-flow-step';

            const num = document.createElement('div');
            num.className = 'kse-flow-step-num';
            num.textContent = step.step || (index + 1);
            stepEl.appendChild(num);

            const body = document.createElement('div');
            body.className = 'kse-flow-step-body';
            const action = document.createElement('div');
            action.className = 'kse-flow-step-action';
            action.textContent = step.action || '';
            body.appendChild(action);
            if (step.purpose) {
                const purpose = document.createElement('div');
                purpose.className = 'kse-flow-step-purpose';
                purpose.textContent = step.purpose;
                body.appendChild(purpose);
            }
            stepEl.appendChild(body);

            el.appendChild(stepEl);
        });
        return el;
    }

    function renderCauseEffectStructure(content) {
        const el = document.createElement('div');
        el.className = 'kse-cause-effect';
        (content.chain || []).forEach(function(link) {
            const item = document.createElement('div');
            item.className = 'kse-ce-item';

            const row = document.createElement('div');
            row.className = 'kse-ce-row';
            const cause = document.createElement('span');
            cause.className = 'kse-ce-cause';
            cause.textContent = link.cause || '';
            const arrow = document.createElement('span');
            arrow.className = 'kse-ce-arrow';
            arrow.textContent = '→';
            const effect = document.createElement('span');
            effect.className = 'kse-ce-effect';
            effect.textContent = link.effect || '';
            row.appendChild(cause);
            row.appendChild(arrow);
            row.appendChild(effect);
            item.appendChild(row);

            if (link.because) {
                const because = document.createElement('div');
                because.className = 'kse-ce-because';
                because.textContent = link.because;
                item.appendChild(because);
            }
            el.appendChild(item);
        });
        return el;
    }

    function renderClassificationStructure(content) {
        const el = document.createElement('div');
        el.className = 'kse-classification';
        (content.categories || []).forEach(function(cat) {
            const catEl = document.createElement('div');
            catEl.className = 'kse-category';

            const name = document.createElement('div');
            name.className = 'kse-category-name';
            name.textContent = cat.trait ? (cat.category + '（' + cat.trait + '）') : (cat.category || '');
            catEl.appendChild(name);

            const list = document.createElement('ul');
            list.className = 'kse-category-items';
            (cat.items || []).forEach(function(item) {
                const li = document.createElement('li');
                li.textContent = item;
                list.appendChild(li);
            });
            catEl.appendChild(list);

            el.appendChild(catEl);
        });
        return el;
    }

    function renderDecisionStructure(content) {
        const el = document.createElement('div');
        el.className = 'kse-decision';

        if (content.condition) {
            const condition = document.createElement('div');
            condition.className = 'kse-decision-condition';
            condition.textContent = '條件：' + content.condition;
            el.appendChild(condition);
        }

        const list = document.createElement('ul');
        list.className = 'kse-decision-options';
        (content.options || []).forEach(function(option) {
            const li = document.createElement('li');
            const choice = document.createElement('span');
            choice.className = 'kse-decision-choice';
            choice.textContent = option.choice || '';
            const arrow = document.createElement('span');
            arrow.className = 'kse-decision-arrow';
            arrow.textContent = ' → ';
            const outcome = document.createElement('span');
            outcome.className = 'kse-decision-outcome';
            outcome.textContent = option.outcome || '';
            li.appendChild(choice);
            li.appendChild(arrow);
            li.appendChild(outcome);
            list.appendChild(li);
        });
        el.appendChild(list);
        return el;
    }

    function renderComparisonStructure(content) {
        const table = document.createElement('table');
        table.className = 'kse-comparison';

        const thead = document.createElement('thead');
        const headRow = document.createElement('tr');
        ['維度', content.option_a_label || 'A', content.option_b_label || 'B'].forEach(function(text) {
            const th = document.createElement('th');
            th.textContent = text;
            headRow.appendChild(th);
        });
        thead.appendChild(headRow);
        table.appendChild(thead);

        const tbody = document.createElement('tbody');
        (content.dimensions || []).forEach(function(dim) {
            const row = document.createElement('tr');
            [dim.dimension, dim.option_a, dim.option_b].forEach(function(text) {
                const td = document.createElement('td');
                td.textContent = text || '';
                row.appendChild(td);
            });
            tbody.appendChild(row);
        });
        table.appendChild(tbody);

        return table;
    }

    function renderTimelineStructure(content) {
        const el = document.createElement('div');
        el.className = 'kse-timeline';
        (content.events || []).forEach(function(event) {
            const item = document.createElement('div');
            item.className = 'kse-timeline-event';

            const time = document.createElement('div');
            time.className = 'kse-timeline-time';
            time.textContent = event.time || '';
            item.appendChild(time);

            const body = document.createElement('div');
            body.className = 'kse-timeline-body';
            const eventText = document.createElement('div');
            eventText.className = 'kse-timeline-event-text';
            eventText.textContent = event.event || '';
            body.appendChild(eventText);
            if (event.significance) {
                const significance = document.createElement('div');
                significance.className = 'kse-timeline-significance';
                significance.textContent = event.significance;
                body.appendChild(significance);
            }
            item.appendChild(body);

            el.appendChild(item);
        });
        return el;
    }

    function renderProblemSolutionStructure(content) {
        const el = document.createElement('div');
        el.className = 'kse-problem-solution';
        const ROWS = [
            ['problem', '問題'],
            ['root_cause', '原因'],
            ['solution', '解法'],
            ['result', '結果'],
        ];
        (content.cases || []).forEach(function(caseItem) {
            const caseEl = document.createElement('div');
            caseEl.className = 'kse-ps-case';
            ROWS.forEach(function(pair) {
                const key = pair[0];
                const label = pair[1];
                if (!caseItem[key]) return;
                const row = document.createElement('div');
                row.className = 'kse-ps-row';
                const labelEl = document.createElement('span');
                labelEl.className = 'kse-ps-label';
                labelEl.textContent = label;
                const valueEl = document.createElement('span');
                valueEl.className = 'kse-ps-value';
                valueEl.textContent = caseItem[key];
                row.appendChild(labelEl);
                row.appendChild(valueEl);
                caseEl.appendChild(row);
            });
            el.appendChild(caseEl);
        });
        return el;
    }

    // Fallback for structure_type = "generic", and defensively for any
    // unrecognized/future structure_type — never a hard crash on unexpected data.
    function renderGenericStructure(content) {
        const list = document.createElement('ul');
        list.className = 'kse-generic';
        (content.points || []).forEach(function(point) {
            const li = document.createElement('li');
            li.textContent = point;
            list.appendChild(li);
        });
        return list;
    }

    // Knowledge Structure Engine Renderer (Sprint 7, Task 4): `data` is the
    // structured Knowledge JSON object (structure_type/structure_label/
    // content) Task 3 produces/caches. Dispatches on structure_type to the
    // matching renderer above; unrecognized structure_type falls back to the
    // generic bullet renderer (reads content.points if present, otherwise
    // renders nothing rather than crashing).
    function buildLearningBlueprintSection(videoId, data) {
        const section = document.createElement('div');
        section.className = 'rapid-learning-section';

        const block = document.createElement('div');
        block.className = 'rapid-learning-block';
        const label = data.structure_label || data.structure_type || 'Learning Blueprint';
        block.innerHTML =
            '<div class="rapid-learning-divider">━━━━━━━━━━━━━━━━━━</div>' +
            '<div class="rapid-learning-heading">🗺️ Learning Blueprint（' + label + '）</div>' +
            '<div class="rapid-learning-divider">━━━━━━━━━━━━━━━━━━</div>';

        const renderer = KNOWLEDGE_STRUCTURE_RENDERERS[data.structure_type] || renderGenericStructure;
        const contentEl = renderer(data.content || {});
        contentEl.classList.add('rapid-learning-content');
        block.appendChild(contentEl);

        section.appendChild(block);
        return section;
    }

    // Teach Back (Sprint 7, Task 5): manual, opt-in trigger — mirrors
    // startLearningBlueprint()'s shape but hits the /teach-back endpoint,
    // which requires a Learning Blueprint to already exist server-side.
    async function startTeachBack(videoId, button) {
        button.disabled = true;
        try {
            const response = await fetch(
                '/api/queue/' + encodeURIComponent(videoId) + '/teach-back',
                { method: 'POST' }
            );
            const data = await response.json();
            if (!response.ok) {
                showStatus(data.detail || '產生 Teach Back 失敗', 'error');
                button.disabled = false;
                return;
            }
            teachBackCache.set(videoId, data.teach_back);
            await loadQueue();
        } catch (error) {
            showStatus('網路連線失敗', 'error');
            button.disabled = false;
        }
    }

    // Revisiting an item whose Teach Back was already generated in an earlier
    // session — same reasoning as fetchLearningBlueprintIntoCache().
    async function fetchTeachBackIntoCache(videoId) {
        if (teachBackFetchInFlight.has(videoId)) {
            return;
        }
        teachBackFetchInFlight.add(videoId);
        try {
            const response = await fetch(
                '/api/queue/' + encodeURIComponent(videoId) + '/teach-back',
                { method: 'POST' }
            );
            if (!response.ok) {
                return;
            }
            const data = await response.json();
            teachBackCache.set(videoId, data.teach_back);
            await loadQueue();
        } catch (error) {
            // Silent — next poll tick (or manual refresh) retries naturally.
        } finally {
            teachBackFetchInFlight.delete(videoId);
        }
    }

    // Fixed reflection prompts — mirrors app/teach_back.py's
    // _REFLECTION_QUESTIONS exactly (not Gemini-generated, same for every
    // Blueprint item; see that module for why).
    const TEACH_BACK_REFLECTION_QUESTIONS = [
        '今天最大的收穫？',
        '哪裡還不理解？',
        '下一步準備做什麼？',
        '什麼時候會再次使用？',
    ];

    // Renders one Blueprint's Teach Back block as real semantic HTML (real
    // checkbox <input>s, real headings) — not <pre> text — per Task 5's
    // "match Study Note's reading experience" requirement.
    function buildTeachBackItem(index, item) {
        const block = document.createElement('div');
        block.className = 'teach-back-item';

        const heading = document.createElement('h4');
        heading.className = 'teach-back-item-heading';
        heading.textContent = 'Blueprint ' + (index + 1) + '：' + (item.title || '');
        block.appendChild(heading);

        const promptHeading = document.createElement('div');
        promptHeading.className = 'teach-back-subheading';
        promptHeading.textContent = 'Explain in Your Own Words';
        block.appendChild(promptHeading);

        const promptText = document.createElement('p');
        promptText.className = 'teach-back-prompt';
        promptText.textContent = item.teaching_prompt || '';
        block.appendChild(promptText);

        const checklistHeading = document.createElement('div');
        checklistHeading.className = 'teach-back-subheading';
        checklistHeading.textContent = 'Self Check Checklist';
        block.appendChild(checklistHeading);

        const checklist = document.createElement('ul');
        checklist.className = 'teach-back-checklist';
        (item.checklist || []).forEach(function(check) {
            const li = document.createElement('li');
            const checkbox = document.createElement('input');
            checkbox.type = 'checkbox';
            checkbox.disabled = true;
            const label = document.createElement('span');
            label.textContent = check;
            li.appendChild(checkbox);
            li.appendChild(label);
            checklist.appendChild(li);
        });
        block.appendChild(checklist);

        const questionsHeading = document.createElement('div');
        questionsHeading.className = 'teach-back-subheading';
        questionsHeading.textContent = 'Practice Questions';
        block.appendChild(questionsHeading);

        const questions = document.createElement('dl');
        questions.className = 'teach-back-questions';
        const q = item.practice_questions || {};
        [['Concept', q.concept], ['Scenario', q.scenario], ['Application', q.application]].forEach(function(pair) {
            const dt = document.createElement('dt');
            dt.textContent = pair[0];
            const dd = document.createElement('dd');
            dd.textContent = pair[1] || '';
            questions.appendChild(dt);
            questions.appendChild(dd);
        });
        block.appendChild(questions);

        const reflectionHeading = document.createElement('div');
        reflectionHeading.className = 'teach-back-subheading';
        reflectionHeading.textContent = 'Reflection';
        block.appendChild(reflectionHeading);

        const reflectionList = document.createElement('ul');
        reflectionList.className = 'teach-back-reflection';
        TEACH_BACK_REFLECTION_QUESTIONS.forEach(function(question) {
            const li = document.createElement('li');
            li.textContent = question;
            reflectionList.appendChild(li);
        });
        block.appendChild(reflectionList);

        return block;
    }

    // Preview + Download, per Task 5's confirmed UI flow: Learning Blueprint
    // → Generate Teach Back → Preview → Download Markdown.
    function buildTeachBackSection(videoId, data) {
        const section = document.createElement('div');
        section.className = 'rapid-learning-section';

        const block = document.createElement('div');
        block.className = 'rapid-learning-block';
        block.innerHTML =
            '<div class="rapid-learning-divider">━━━━━━━━━━━━━━━━━━</div>' +
            '<div class="rapid-learning-heading">📝 Teach Back</div>' +
            '<div class="rapid-learning-divider">━━━━━━━━━━━━━━━━━━</div>';

        (data.items || []).forEach(function(item, index) {
            block.appendChild(buildTeachBackItem(index, item));
        });

        const downloadBtn = document.createElement('a');
        downloadBtn.className = 'queue-item-export teach-back-download';
        downloadBtn.href = '/api/queue/' + encodeURIComponent(videoId) + '/teach-back/download';
        downloadBtn.innerHTML = '<span aria-hidden="true">⬇</span> 下載 Teach Back';
        block.appendChild(downloadBtn);

        section.appendChild(block);
        return section;
    }

    // Quick Learn Layer (Sprint 7, Task 2): pulls up to `maxCount` top-level
    // list items out of the existing Knowledge Outline text — a pure UI-layer
    // condensation of content Task 1 already generated, not a new Gemini call.
    // Matches common top-level markers (1. / 1) / - / * / •) with little to no
    // leading whitespace; deeper-indented sub-items are skipped so this stays
    // a "5 points" summary, not the full nested outline.
    function extractTopPoints(knowledgeOutlineText, maxCount) {
        const lines = knowledgeOutlineText.split('\n');
        const points = [];
        for (const line of lines) {
            const match = line.match(/^\s{0,3}(?:[0-9]+[.)]|[-*•])\s+(.+)/);
            if (match) {
                points.push(match[1].trim());
                if (points.length >= maxCount) {
                    break;
                }
            }
        }
        return points;
    }

    // Renders the Quick Learn Layer directly on a Queue Card: One Sentence +
    // condensed points are always visible (fits in one screen — the product
    // goal is "30 seconds to a knowledge outline" before deciding to read
    // more); the full Knowledge Outline is collapsed by default behind a
    // toggle that only flips a CSS class, no Gemini call, no re-fetch.
    function buildRapidLearningSection(videoId, rawText) {
        const parsed = parseKnowledgeOutline(rawText);
        const points = extractTopPoints(parsed.knowledgeOutline, 5);

        const section = document.createElement('div');
        section.className = 'rapid-learning-section';

        const quickBlock = document.createElement('div');
        quickBlock.className = 'rapid-learning-block';
        quickBlock.innerHTML =
            '<div class="rapid-learning-divider">━━━━━━━━━━━━━━━━━━</div>' +
            '<div class="rapid-learning-heading">🎯 30 秒快速理解</div>' +
            '<div class="rapid-learning-divider">━━━━━━━━━━━━━━━━━━</div>';

        const oneSentenceText = document.createElement('p');
        oneSentenceText.className = 'rapid-learning-content';
        oneSentenceText.textContent = parsed.oneSentence;
        quickBlock.appendChild(oneSentenceText);

        const pointsHeading = document.createElement('div');
        pointsHeading.className = 'rapid-learning-heading';
        pointsHeading.textContent = '🧠 ' + points.length + ' 個重點';
        quickBlock.appendChild(pointsHeading);

        const CIRCLED_DIGITS = ['①', '②', '③', '④', '⑤'];
        const pointsList = document.createElement('div');
        pointsList.className = 'rapid-learning-points';
        points.forEach(function(point, index) {
            const pointEl = document.createElement('p');
            pointEl.className = 'rapid-learning-content';
            pointEl.textContent = (CIRCLED_DIGITS[index] || (index + 1) + '.') + ' ' + point;
            pointsList.appendChild(pointEl);
        });
        quickBlock.appendChild(pointsList);

        section.appendChild(quickBlock);

        const isExpanded = expandedKnowledgeOutlineCards.has(videoId);

        const toggleBtn = document.createElement('button');
        toggleBtn.className = 'rapid-learning-toggle';
        toggleBtn.type = 'button';
        toggleBtn.textContent = isExpanded ? '▲ 收合' : '▶ 展開完整內容';
        section.appendChild(toggleBtn);

        const outlineBlock = document.createElement('div');
        outlineBlock.className = 'rapid-learning-block rapid-learning-full' + (isExpanded ? '' : ' is-hidden');
        outlineBlock.innerHTML =
            '<div class="rapid-learning-divider">━━━━━━━━━━━━━━━━━━</div>' +
            '<div class="rapid-learning-heading">🗺️ Knowledge Outline</div>' +
            '<div class="rapid-learning-divider">━━━━━━━━━━━━━━━━━━</div>';
        const outlineText = document.createElement('pre');
        outlineText.className = 'rapid-learning-content';
        outlineText.textContent = parsed.knowledgeOutline;
        outlineBlock.appendChild(outlineText);
        section.appendChild(outlineBlock);

        // Pure UI toggle — no fetch, no re-render, just a class flip — so
        // expand/collapse never re-calls Gemini. State is also mirrored into
        // expandedKnowledgeOutlineCards so it survives a full renderQueue()
        // rebuild triggered by an unrelated action (e.g. deleting another item).
        toggleBtn.addEventListener('click', function() {
            const nowExpanded = outlineBlock.classList.toggle('is-hidden') === false;
            toggleBtn.textContent = nowExpanded ? '▲ 收合' : '▶ 展開完整內容';
            if (nowExpanded) {
                expandedKnowledgeOutlineCards.add(videoId);
            } else {
                expandedKnowledgeOutlineCards.delete(videoId);
            }
        });

        return section;
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

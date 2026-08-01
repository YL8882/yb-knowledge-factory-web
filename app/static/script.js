document.addEventListener('DOMContentLoaded', function() {
    const urlInput = document.getElementById('youtube-url');
    const generateBtn = document.getElementById('generate-btn');
    const statusDiv = document.getElementById('status');
    const queueList = document.getElementById('queue-list');
    const queueEmpty = document.getElementById('queue-empty');
    const processingPanel = document.getElementById('processing-panel');
    const processingStagesEl = document.getElementById('processing-stages');
    const processingResultEl = document.getElementById('processing-result');

    // The video_id the processing panel is currently showing — the one most recently
    // added via the Generate button. Only one panel, so only one video is tracked.
    let trackedVideoId = null;

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
    // Generating) still has real work in flight, or hasn't started yet but hasn't
    // failed either. False once it reaches a terminal state (Study Note Ready, or
    // a failure recorded via last_error — nothing auto-retries a failure, so
    // polling forever on a failed "Queued" item would be wasted work).
    function isPipelineActive(item) {
        if (item.status === 'Downloading' || item.status === 'Transcribing' || item.status === 'Generating') {
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
            // Transcript done, Study Note not chained yet (rare — e.g. old queue.json
            // entry from before this pipeline existed). Not an error, just not final.
            p.className = 'queue-item-report';
            p.textContent = '✓ Transcript 已完成並下載，Study Note 準備中...';
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
            // "Queued" just means "waiting its turn" — a plain status label, not a
            // call to action.
            const badge = document.createElement('span');
            badge.className = 'queue-item-badge';
            if (isWaitingInLine) {
                badge.classList.add('is-waiting');
                badge.textContent = '排隊中';
            } else if (item.status === 'Downloading' || item.status === 'Transcribing' || item.status === 'Generating') {
                badge.classList.add('is-active');
                badge.textContent = item.status;
            } else if (item.status === 'Transcript Ready' || item.status === 'Study Note Ready') {
                badge.classList.add('is-done');
                badge.textContent = item.status;
            } else {
                badge.textContent = item.status;
            }

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

            queueList.appendChild(li);

            // No browser-side auto-download here: the backend already persists
            // Transcript/Study Note markdown into outputs/transcripts and
            // outputs/study_notes the moment each is ready — that's the single
            // canonical copy. A second browser-triggered download (to the
            // OS Downloads folder or a chosen folder) would just be a redundant
            // duplicate of a file that already exists on disk.
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

    function renderProcessingPanel(items) {
        const item = trackedVideoId ? items.find(function(i) { return i.video_id === trackedVideoId; }) : null;

        if (!item) {
            processingPanel.classList.add('is-hidden');
            return;
        }

        processingPanel.classList.remove('is-hidden');
        processingStagesEl.innerHTML = '';

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

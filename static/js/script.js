document.addEventListener('DOMContentLoaded', () => {
    refreshData();
});

function triggerScan() {
    const btn = document.getElementById('scanBtn');
    if(btn) {
        const icon = btn.querySelector('i');
        icon.classList.add('fa-spin');
        btn.innerHTML = '<i class="fas fa-radar fa-spin me-2"></i> SCANNING...';
        
        fetch('/api/scan', { method: 'POST' })
        .then(r => r.json())
        .then(d => {
            refreshData();
            btn.innerHTML = '<i class="fas fa-check me-2"></i> COMPLETED';
            setTimeout(() => {
                btn.innerHTML = '<i class="fas fa-satellite-dish me-2"></i> INITIALIZE SCAN';
                icon.classList.remove('fa-spin');
            }, 2000);
        });
    }
}

function refreshData() {
    fetch('/api/data')
    .then(r => r.json())
    .then(d => {
        const stats = d.stats;
        
        if(document.getElementById('total-threats')) {
            document.getElementById('total-threats').innerText = stats.total;
            document.getElementById('crit-threats').innerText = stats.critical;
            document.getElementById('risk-score').innerText = stats.avg_score + "/100";
        }

        const tbody = document.getElementById('intel-body');
        if(tbody) {
            tbody.innerHTML = '';
            d.threats.forEach(t => {
                // Determine Badge Class based on severity string
                let badgeClass = 'badge-med';
                if(t.severity === 'Critical') badgeClass = 'badge-crit';
                if(t.severity === 'High') badgeClass = 'badge-high';

                tbody.innerHTML += `
                    <tr>
                        <td><span class="badge-modern ${badgeClass}">${t.severity}</span></td>
                        <td><span class="data-cell">${t.threat_score}</span></td>
                        <td>
                            <div class="text-white fw-bold mb-1">${t.title.substring(0, 60)}...</div>
                            <div class="small" style="color: #94a3b8;">${t.source} • ${t.threat_type}</div>
                        </td>
                        <td><span class="text-white">${t.target_sector}</span></td>
                        <td class="small text-muted">${t.published_date}</td>
                        <td class="text-end">
                            <a href="${t.link}" target="_blank" class="btn btn-sm btn-outline-secondary border-0" style="color: var(--neon-cyan);">
                                <i class="fas fa-external-link-alt"></i> VIEW
                            </a>
                        </td>
                    </tr>
                `;
            });
        }
    });
}
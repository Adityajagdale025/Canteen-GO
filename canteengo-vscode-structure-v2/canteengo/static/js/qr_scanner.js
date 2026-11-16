function displayResult(data) {
    const box = document.getElementById('scan-result');
    if (data.valid) {
        box.className = "p-4 bg-emerald-100 border border-emerald-300 text-emerald-900 rounded-xl text-sm font-bold mb-6";
        box.innerHTML = `
            <div class="text-lg font-black mb-1">✅ VERIFIED: ${data.token}</div>
            <div>Student: ${data.student}</div>
            <div>Slot: ${data.slot}</div>
            <div class="mt-2 pt-2 border-t border-emerald-200 text-emerald-800">
                Hand Over Tray: ${data.items.join(', ')}
            </div>
        `;
    } else {
        box.className = "p-4 bg-rose-100 border border-rose-300 text-rose-900 rounded-xl text-sm font-bold mb-6";
        box.innerText = `❌ ${data.message}`;
    }
}

function onScanSuccess(decodedText) {
    fetch(`/kitchen/api/verify-token/?qr_data=${encodeURIComponent(decodedText)}`)
        .then(res => res.json())
        .then(data => displayResult(data));
}

function verifyManualToken() {
    const tokenInput = document.getElementById('manual-token').value.trim();
    if (!tokenInput) return;
    fetch(`/kitchen/api/verify-token/?token_number=${encodeURIComponent(tokenInput)}`)
        .then(res => res.json())
        .then(data => displayResult(data));
}

if (document.getElementById('reader')) {
    const scanner = new Html5QrcodeScanner("reader", { fps: 10, qrbox: 240 });
    scanner.render(onScanSuccess);
}
document.addEventListener('DOMContentLoaded', function () {
    document.getElementById('menuForm').addEventListener('submit', function (e) {
        e.preventDefault();
        const days = document.getElementById('days').value;
        displayCurryMenu(days);
    });
});

function displayCurryMenu(days) {
    const tableBody = document.getElementById('menuTableBody');
    tableBody.innerHTML = ''; // テーブルをクリア

    const curryTypes = [
        'ビーフカレー',
        'チキンカレー',
        'ポークカレー',
        'シーフードカレー',
        'ベジタブルカレー',
        'キーマカレー',
        'グリーンカレー'
    ];

    for (let i = 1; i <= days; i++) {
        const row = tableBody.insertRow();
        row.insertCell(0).textContent = `${i}日目`;
        row.insertCell(1).textContent = curryTypes[Math.floor(Math.random() * curryTypes.length)];
        row.insertCell(2).textContent = curryTypes[Math.floor(Math.random() * curryTypes.length)];
        row.insertCell(3).textContent = curryTypes[Math.floor(Math.random() * curryTypes.length)];
        row.insertCell(4).textContent = `${Math.floor(500 + Math.random() * 500)} kcal`;
        row.insertCell(5).textContent = `¥${Math.floor(500 + Math.random() * 500)}`;
    }

    document.getElementById('menuTable').style.display = 'table';
}

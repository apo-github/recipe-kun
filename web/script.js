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

        // 朝食、昼食、夕食のセルを作成
        for (let j = 1; j <= 3; j++) {
            const cell = row.insertCell(j);
            const curry = curryTypes[Math.floor(Math.random() * curryTypes.length)];
            cell.innerHTML = `
                <div style="display: flex; flex-direction: column; align-items: center; text-align: center;">
                    
${curry}

                    <img src="img/a.png" alt="${curry}" style="width: 150px; height: 150px; margin-top: 5px;">
                
            `;
        }

        row.insertCell(4).textContent = `${Math.floor(500 + Math.random() * 500)} kcal`;
        row.insertCell(5).textContent = `¥${Math.floor(500 + Math.random() * 500)}`;
    }

    document.getElementById('menuTable').style.display = 'table';
}
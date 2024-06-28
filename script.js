// const endpointUrl = "https://mbwtn3h217.execute-api.us-west-2.amazonaws.com/stage"
const endpointUrl = "https://o6nc0axucd.execute-api.us-west-2.amazonaws.com/test"
document.addEventListener('DOMContentLoaded', function () {
    document.getElementById('menuForm').addEventListener('submit', function (e) {
        e.preventDefault();
        const familyId = document.getElementById('familyId').value;
        const days = document.getElementById('days').value;
        displayCurryMenu(days);
        api(endpointUrl, familyId, days);
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


// API GatewayのエンドポイントURLを設定

// getでとってくるパターン
// function api(endpointUrl){
//     // Fetch APIを使用してGETリクエストを送信
//     fetch(endpointUrl)
//     .then(response => {
//     if (!response.ok) {
//         throw new Error('Network response was not ok');
//     }
//     return response.json(); // JSON形式でレスポンスを解析
//     })
//     .then(data => {
//     console.log('API Gatewayからのレスポンス:', data);
//     // ここでdataを使った処理を記述
//     })
//     .catch(error => {
//     console.error('Fetchエラー:', error);
//     });
// }


// ポストでとってくるパターン
function api(endpointUrl, familyId, numDay) {
    fetch(endpointUrl, {
        method: "POST",
        body: JSON.stringify({
            family_id: familyId,
            num_day: numDay
        }),
        headers: {
            "Content-type": "application/json; charset=UTF-8"
        },
        mode: "no-cors"
    })
        .then((response) => {
            console.log('API Gatewayからのレスポンス:', response)
            console.log("respose.body", response.body)
        })
        .then((data) => {
            console.log('API Gatewayからのレスポンス:', data)
            // ここでdata.generated_textを使用して何かを行います
            const generatedText = data.generated_text;
            console.log(generatedText);

        }
        )



    // .then((data) => console.log('API Gatewayからのレスポンス:', data))
    // .catch((error) => console.log('Error:', error));
}
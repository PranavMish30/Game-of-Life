
const submit = document.getElementById("submit");
let myChart
let isPaused = false;

submit.onclick = function() {
    generateLifeGrid("lifeGrid","rows","columns");

    const generations = document.getElementById("generation").value;
    const rows = document.getElementById("rows").value;
    const columns = document.getElementById("columns").value;
    
    const form = {
        generations : generations,
        rows : rows,
        columns : columns
    }

    fetch("/submit",{
        method:'POST',
        headers: {
            'Content-Type': 'application/json'
          },
          body: JSON.stringify(form)
    })
    .then(response => response.json())
    .then(simulationData =>  simulate(simulationData,generations,rows,columns,1000))
    .catch(error => console.log(error))
}

function generateLifeGrid(divId,rows,columns) {
    const gridDiv = document.getElementById(divId);
    const gridRows = document.getElementById(rows).value;
    const gridColumns = document.getElementById(columns).value;
    
    gridDiv.style.display='grid';
    gridDiv.style.gridTemplateRows=`repeat(${gridRows},1fr)`;
    gridDiv.style.gridTemplateColumns=`repeat(${gridColumns},1fr)`;
    for(let i=0;i<gridRows;i++){
        for(let j=0;j<gridColumns;j++){
            const cell = document.createElement('div');
            cell.id = `${i} ${j}`;
            cell.classList.add('cell');
            cell.textContent = ' ';
            gridDiv.appendChild(cell);
        }
    }
    for(i=0;i<gridRows;i++){
        for(let j=0;j<gridColumns;j++){
            cell = document.getElementById(`${i} ${j}`);
            cell.style.gridArea = `${i + 1} / ${j + 1} / ${i + 2} / ${j + 2}`;
        }
    }
}

document.getElementById("pauseButton").addEventListener("click", function () {
    isPaused = !isPaused;
});

const simulate = async function(simulationData,generations,rows,columns,pauseTime) {
    for(let i = 0;i<generations;i++){

        while (isPaused) {
            await new Promise(resolve => setTimeout(resolve, 100)); 
        }

        if (myChart) {
            myChart.destroy();
        }

        
        for(let j = 0;j<rows;j++){
            for(let k =0;k<columns;k++){
                if (simulationData[i][0][j][k] == 0){
                    document.getElementById(`${j} ${k}`).style.backgroundColor='white';
                }
                else{
                    document.getElementById(`${j} ${k}`).style.backgroundColor='green'; 
                }
            }
        }
        const gridInfo = document.getElementById("textData");
        gridInfo.innerHTML=

        `<pre>
            <h1> Infographics:</h1>
            <h2> Generation: ${i+1} Population: ${simulationData[i][1]}</h2>
        </pre>`;

        const ctx = document.getElementById('myChart').getContext('2d');
        let populationArray = Object.values(simulationData).slice(-(i + 1)).map(entry => entry[1]);
        let labelss = Array.from({ length: populationArray.length }, (_, i) => i + 1);
        myChart = new Chart(ctx, {
            type: 'line',
            data: {
                labels: labelss,
                datasets: [{
                    label: 'Population Trends',
                    data: populationArray,
                    borderColor: 'green',
                    fill: true
                }]
            }
        });
        await new Promise(resolve => setTimeout(resolve, pauseTime));
    }
    
}

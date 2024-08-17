
const submit = document.getElementById("submit");

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

function pause(milliseconds) {
    return new Promise(resolve => setTimeout(resolve, milliseconds));
}

const simulate = async function(simulationData,generations,rows,columns,pauseTime) {
    for(let i = 0;i<generations;i++){
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
        const gridInfo = document.getElementById("infographics");
        gridInfo.innerHTML=
        
        `<pre>
            <h1>Generation: ${i}</h1>
            <h1>Population: ${simulationData[i][1]}</h1>
        </pre>`;

        await pause(pauseTime);
    }
    
}

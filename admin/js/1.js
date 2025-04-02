async function get_GS() {
    let response = await fetch("http://localhost:8000/api/GS/all");
    if (response.ok) {
        let json = await response.json();
        return json;
    } else {
        alert("Ошибка HTTP: " + response.status);
    }
}

async function render_GS() {
    let template = `
    <tr>
        <th scope="row">{ИД}</th>
        <td>{ПроизводительПроцессора}</td>
        <td>{МодельПроцессора}</td>
        <td>{ПроизводительВидеокарты}</td>
        <td>{МодельВидеокарты}</td>
        <td>{ОбъёмОП}</td>
        <td>{ГцОП}</td>
        <td>{NAME}</td>
    
    </tr>`;

    let GSs = await get_GS();
    let container = document.getElementById("GS");
    GSs.forEach(element => {
        let GS = template
        .replace("{ИД}", element.id)
        .replace("{ПроизводительПроцессора}", element.ManufacturerCPU)
        .replace("{МодельПроцессора}", element.ModelCPU)
        .replace("{ПроизводительВидеокарты}", element.ManufacturerGPU)
        .replace("{МодельВидеокарты}", element.ModelGPU)
        .replace("{ОбъёмОП}", element.SizeRAM)
        .replace("{ГцОП}", element.HertzRAM)
        .replace("{NAME}", element.NAME)
        container.innerHTML += GS;
    });
}

render_GS();
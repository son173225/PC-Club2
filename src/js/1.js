async function get_GS() {
    let response = await fetch("http://192.168.50.18:8000/api/GS/all");
    if (response.ok) {
        let json = await response.json();
        return json;
    } else {
        alert("Ошибка HTTP: " + response.status);
    }
}

async function render_GS() {
    let template = `
<div class="card card-2" style="width: 18rem;">
    <div class="card-body">
        <h5 class="card-title"><u>{NAME}</u></h5>
        <div class="acesor">
            <div style="text-decoration: underline;">
                <p>Процессор</p>
                <p class="card-text">Видеокарта</p>
                <p class="card-text">Оперативная<br>память</p>
            </div>
            <div class="gso" style="text-decoration: underline;">
                <p>{ПроизводительПроцессора}<br>{МодельПроцессора}</p>
                <p>{ПроизводительВидеокарты}<br>{МодельВидеокарты}</p>
                <p>{ОбъёмОП}<br>{ГцОП}</p>
            </div>
        </div>
    </div>
</div>`;
let GSs = await get_GS();
    let container = document.getElementById("GS");
    GSs.forEach(element => {
        let GS = template
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

function registar(nivel) {
    fetch("/registar", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ nivel: nivel })
    })
    .then(response => response.json())
    .then(() => {
        document.getElementById("msg").innerText =
            "Obrigado pela sua opinião!";
        setTimeout(() => {
            document.getElementById("msg").innerText = "";
        }, 2000);
    });
}

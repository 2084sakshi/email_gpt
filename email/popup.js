document.getElementById("email-form").addEventListener( "submit", async function (event) {
    event.preventDefault();
    
    const src = document.getElementById("src").value;
    const des = document.getElementById("des").value;
    const subject = document.getElementById("subject").value;
    const tone = document.getElementById("tone").value;
    const about = document.getElementById("about").value;

    const response = await fetch("http://127.0.0.1:5000/generate-email", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({ src, des, subject, tone, about })
    });

    const result = await response.json();

    if (response.ok) {
        document.getElementById("result").innerText = result.email;
    } else {
        document.getElementById("result").innerText = result.error || "Error generating email";
    }
});

document.getElementById('speakButton').addEventListener('click', function() {
    const text = document.getElementById('text').value;
    if (text.trim() === "") {
      alert("Por favor, escribe algún texto.");
      return;
    }
    
    const formData = new FormData();
    formData.append("text", text);
  
    fetch("/speak", {
      method: "POST",
      body: formData
    })
    .then(response => response.blob())
    .then(blob => {
      const audioUrl = URL.createObjectURL(blob);
      const audio = new Audio(audioUrl);
      audio.play();
    })
    .catch(error => {
      console.error("Error al convertir el texto a audio:", error);
    });
  });
  
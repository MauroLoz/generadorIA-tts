document.addEventListener('DOMContentLoaded', () => {

    const audio = document.getElementById('audioPlayer');
    
    if (audio) {
        const playBtn = document.querySelector('.play_btn');
        const progressFill = document.querySelector('.progress_fill');
        const timeDisplay = document.querySelector('.time_display');
        const volumeSlider = document.querySelector('.volume_slider');
        const volumeFill = document.querySelector('.volume_fill');

        function formatTime(seconds) {
            const mins = Math.floor(seconds / 60);
            const secs = Math.floor(seconds % 60);
            return `${mins}:${secs.toString().padStart(2, '0')}`;
        }

        audio.addEventListener('loadedmetadata', () => {
            const total = formatTime(audio.duration);
            timeDisplay.textContent = `0:00 / ${total}`;
            console.log("Duración real:", total);
            
            audio.play().catch(error => {
                console.log("Error de auto-reproducción:", error);
            });
        });

        audio.addEventListener('play', () => {
            playBtn.innerHTML = `
                <svg class="icon" xmlns="http://www.w3.org/2000/svg"
                    viewBox="0 0 24 24" fill="none" stroke="currentColor"
                    stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                    <rect x="6" y="4" width="4" height="16"></rect>
                    <rect x="14" y="4" width="4" height="16"></rect>
                </svg>`;
        });

        audio.addEventListener('pause', () => {
            playBtn.innerHTML = `
                <svg class="icon" xmlns="http://www.w3.org/2000/svg"
                    viewBox="0 0 24 24" fill="none" stroke="currentColor"
                    stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                    <polygon points="6 4 20 12 6 20 6 4"></polygon>
                </svg>`;
        });

        playBtn.addEventListener('click', () => {
            if (audio.paused) {
                audio.play();
            } else {
                audio.pause();
            }
        });

        audio.addEventListener('timeupdate', () => {
            const progress = (audio.currentTime / audio.duration) * 100;
            progressFill.style.width = progress + '%';
            
            const current = formatTime(audio.currentTime);
            const total = formatTime(audio.duration);
            timeDisplay.textContent = `${current} / ${total}`;
        });

        audio.volume = 1; 
        volumeFill.style.width = '100%';
        
        volumeSlider.addEventListener("click", (e) => {
            const rect = volumeSlider.getBoundingClientRect();
            const offsetX = e.clientX - rect.left;
            const newVolume = Math.min(Math.max(offsetX / rect.width, 0), 1);
            audio.volume = newVolume;
            volumeFill.style.width = `${newVolume * 100}%`;
        });
    }

    const time = document.querySelector('.timestamp');
    if (time) { 
        const ahora = new Date();
        const fechaFormateada = ahora.toLocaleString('es-AR', {
            dateStyle: 'short',
            timeStyle: 'short'
        });
        time.textContent = `🕒 ${fechaFormateada}`; 
    }

    document.querySelector('.copy-btn')?.addEventListener('click', () => {
        const text = document.querySelector('.interpretation_text').textContent;
        navigator.clipboard.writeText(text);
        alert('Texto copiado al portapapeles');
    });

    const downloadBtn = document.querySelector(".download_btn");
    const fileDownload = document.querySelector(".generated_image");

    if (downloadBtn && fileDownload) {
        const imageUrl = fileDownload.src;

        downloadBtn.addEventListener("click", async() => {
            const response = await fetch(imageUrl);
            const blob = await response.blob();

            const blobUrl = URL.createObjectURL(blob);

            const link = document.createElement('a');
            link.href = blobUrl;
            link.download = 'arte_emocional.png'; 

            document.body.appendChild(link);
            link.click();

            document.body.removeChild(link);
            URL.revokeObjectURL(blobUrl);
        });
    }

    const btnLang = document.getElementById("btn-lang");
    const langInput = document.getElementById("current-lang-input"); 
    
    const langs = ["es", "en"];
    
    const textos = {
        es: {
            flag: "🇪🇸",
            crearArte: "Crear Arte Emocional",
            emocion: "Emoción",
            placeholderEmocion: "Ej: Tristeza, Alegría, Misterio",
            elemento: "Elemento",
            placeholderElemento: "Ej: Océano tempestuoso, Bosque, Fuego",
            generar: "Generar Arte",
            imagenGenerada: "Imagen Generada",
            generarImgPlaceholder: "Genera una imagen para verla aquí",
            narracion: "Narración de Audio",
            generarAudioPlaceholder: "Genera audio para reproducirlo aquí",
            interpretacion: "Interpretación de Gemini AI",
            interpretacionPlaceholder: "Genera una interpretación para verla aquí",
            copiar: "🔗 Copiar", 
        },
        
        en: {
            flag: "🇺🇸",
            crearArte: "Create Emotional Art",
            emocion: "Emotion",
            placeholderEmocion: "E.g.: Sadness, Joy, Mystery",
            elemento: "Element",
            placeholderElemento: "E.g.: Stormy ocean, Forest, Fire",
            generar: "Generate Art",
            imagenGenerada: "Generated Image",
            generarImgPlaceholder: "Generate an image to display here",
            narracion: "Audio Narration",
            generarAudioPlaceholder: "Generate audio to play here",
            interpretacion: "Gemini AI Interpretation",
            interpretacionPlaceholder: "Generate an interpretation to see it here",
            copiar: "🔗 Copy", 
        }
    };
    
    function setLanguage(lang) {
        const t = textos[lang];
        btnLang.textContent = t.flag;
        
        document.getElementById("card_title_h3").textContent = t.crearArte;
        
        const labels = document.querySelectorAll(".form_entryInput label");
        if (labels[0]) labels[0].innerHTML = `<div class="label_icon heart"></div>${t.emocion}`;
        if (labels[1]) labels[1].innerHTML = `<div class="label_icon wave"></div>${t.elemento}`;
        
        const emocionInput = document.querySelector("input[name='emocion']");
        const elementoInput = document.querySelector("input[name='elemento']");
        if (emocionInput) emocionInput.placeholder = t.placeholderEmocion;
        if (elementoInput) elementoInput.placeholder = t.placeholderElemento;
        
        const generateBtn = document.querySelector(".generate_btn");
        if (generateBtn) generateBtn.textContent = t.generar;
        
        const cardTitles = document.querySelectorAll(".card_title");
        if (cardTitles.length > 1) {
            const iconElement = cardTitles[1].querySelector(".icon");
            if (iconElement) iconElement.nextSibling.textContent = t.imagenGenerada;
        }

        const imgPlaceholder = document.querySelector(".right_column .card:nth-child(1) .placeholder");
        if (imgPlaceholder) imgPlaceholder.textContent = t.generarImgPlaceholder;
        
        if (cardTitles.length > 2) { 
            const iconElement = cardTitles[2].querySelector(".icon");
            if (iconElement) iconElement.nextSibling.textContent = t.interpretacion;
        }
        const interpPlaceholder = document.querySelector(".right_column .card:nth-child(2) .placeholder");
        if (interpPlaceholder) interpPlaceholder.textContent = t.interpretacionPlaceholder;
        
        if (cardTitles.length > 3) {
            const iconElement = cardTitles[3].querySelector(".icon");
            if (iconElement) iconElement.nextSibling.textContent = t.narracion;
        }
        const audioPlaceholder = document.querySelector(".right_column .card:last-child .placeholder");
        if (audioPlaceholder) audioPlaceholder.textContent = t.generarAudioPlaceholder;
        
        const copyBtn = document.querySelector(".copy-btn");
        if (copyBtn) copyBtn.innerHTML = t.copiar; 

    }

    const initialLangElement = document.getElementById('initial-lang-data');
    const initialLang = (initialLangElement && initialLangElement.textContent) ? initialLangElement.textContent.trim() : 'en';

    let langIndex = langs.indexOf(initialLang); 
    if (langIndex === -1) { 
        langIndex = 1; 
    }

    const currentLang = langs[langIndex];
    setLanguage(currentLang);
    
    if (langInput) {
        langInput.value = currentLang;
    }

    if (btnLang) {
        btnLang.addEventListener("click", () => {
            langIndex = (langIndex + 1) % langs.length;
            const newLang = langs[langIndex]; 

            setLanguage(newLang);

            if (langInput) {
                langInput.value = newLang;
            }
        });
    }
});
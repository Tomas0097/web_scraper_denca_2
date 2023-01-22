## Docker
Vyvoj projektu je zatim multiplatformni. To znamena, ze se da k vyvoji pouzit Linux, MacOS 
nebo WSL2 diky uzasnemu Dockeru.

Mensi problem nastane, kdyz se image buildne na Macu s M1 chipem (arm) a pak se ten samy 
image stahne do PC bez arm chipu. V tom pripadne ten image bude zpusobovat problemy. 
Misto pullovani takoveho image bude potreba ho znovu buildnou v PC bez arm chipu.

Pri buildovani image je potreba byt v korenove slozce projektu. Skripty pro vytvoreni 
potrebnych custom images: 
- `docker build -t flakooo/myprojects:web_scraper_denca_2-app -f dev/app/Dockerfile .`

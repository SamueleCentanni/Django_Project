const siteUrl = '//127.0.0.1:8000/';
const styleUrl = siteUrl + 'static/css/bookmarklet.css';
const minWidth = 250;
const minHeight = 250;

// Carico CSS
var head = document.getElementsByTagName('head')[0];  // Get HTML head element
var link = document.createElement('link'); // Create new link Element
link.rel = 'stylesheet'; // set the attributes for link element
link.type = 'text/css';
link.href = styleUrl + '?r=' + Math.floor(Math.random()*9999999999999999);
head.appendChild(link);  // Append link element to HTML head

// Carico HTML
var body = document.getElementsByTagName('body')[0];
boxHtml = `
  <div id="bookmarklet">
    <a href="#" id="close">&times;</a>
    <h1>Seleziona una immagine:</h1>
    <div class="images"></div>
  </div>`;
body.innerHTML += boxHtml;

function bookmarkletLaunch() {
  bookmarklet = document.getElementById('bookmarklet');
  var imagesFound = bookmarklet.querySelector('.images');

 
  imagesFound.innerHTML = '';
  // mostro il bookmarklet
  bookmarklet.style.display = 'block';

  // fine evento
  bookmarklet.querySelector('#close')
             .addEventListener('click', function(){
    bookmarklet.style.display = 'none'
  });

  // trova immagini nel DOM con dimensioni minime
  images = document.querySelectorAll('img[src$=".jpg"], img[src$=".jpeg"], img[src$=".png"]');
  images.forEach(image => {
    if(image.naturalWidth >= minWidth
       && image.naturalHeight >= minHeight)
    {
      var imageFound = document.createElement('img');
      imageFound.src = image.src;
      imagesFound.append(imageFound);
    }
  })

  // evento di selezione dell'immagine
  imagesFound.querySelectorAll('img').forEach(image => {
    image.addEventListener('click', function(event){
      imageSelected = event.target;
      bookmarklet.style.display = 'none';
      window.open(siteUrl + 'images/create/?url='
                  + encodeURIComponent(imageSelected.src)
                  + '&title='
                  + encodeURIComponent(document.title),
                  '_blank');
    })
  })
}

// lancia il bookmarklet
bookmarkletLaunch();
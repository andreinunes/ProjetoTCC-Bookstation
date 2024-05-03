function loading(){
  document.getElementById("loading").style.display = "block";
  document.getElementById("Conteúdo").style.display = "none";    
}

function submitBusca(){
  var textoBusca = document.getElementById("buscaLivro").value;
  if (textoBusca == ''){
    textoBusca = ' ';
  }
  var selectBusca = document.getElementById("selectBusca").value;
  if (selectBusca == 'Titulo'){
    document.getElementById("formBusca").action = "/livros/buscarLivrosTitulo/" + textoBusca + "/0";
  }
  else if (selectBusca == 'Autor'){
    document.getElementById("formBusca").action = "/livros/buscarLivrosAutor/" + textoBusca + "/0";
  }
  document.getElementById("formBusca").submit();
  loading();
}

function limpar_url(){
  var uri = window.location.toString();
  if (uri.indexOf("?") > 0) {
      var clean_uri = uri.substring(0, uri.indexOf("?"));
      window.history.replaceState({}, document.title, clean_uri);
  }
}


function submit(id){
  document.getElementById("idDoLivro").value = id;
  document.getElementById("urlAtual").value = window.location.href;
  document.getElementById("formPagina").action = "/livros/paginalivro/" + id;
  document.getElementById("formPagina").submit();
  loading();
}


const myModal = document.getElementById('myModal')
const myInput = document.getElementById('myInput')

myModal.addEventListener('shown.bs.modal', () => {
  myInput.focus()
})
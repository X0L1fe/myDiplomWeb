// Получаем элементы
var modal = document.getElementById("modal");
var btn = document.getElementById("edit-btn");
var span = document.getElementsByClassName("close")[0];

// Открытие модального окна при клике на кнопку
btn.onclick = function() {
  modal.style.display = "flex";  // Устанавливаем display: flex для показа и центрирования
}

// Закрытие модального окна при клике на X
span.onclick = function() {
  modal.style.display = "none";  // Закрываем модальное окно
}

// Закрытие модального окна при клике вне его
window.onclick = function(event) {
  if (event.target == modal) {
    modal.style.display = "none";  // Закрытие при клике вне модального окна
  }
}

function updateSlider() {
	var currentVal = document.querySelector("#tippct").value;
	document.querySelector("#tipval").innerHTML = currentVal;
}
window.addEventListener('load', updateSlider);

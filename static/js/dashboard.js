$("#menu-toggle").click(function (e) {
	e.preventDefault();
	$("#wrapper").toggleClass("toggled");
});

jQuery.datetimepicker.setLocale('pt');

$("#picker").datetimepicker({
	timepicker: false,
	datepicker: true,
	format: 'Y-m-d'
});

$("#pickerStart").datetimepicker({
	timepicker: true,
	datepicker: true,
	format: 'Y-m-d H:i',
	step: 5,
	yearStart: new Date().getFullYear(),
	yearEnd: new Date().getFullYear() + 50,
});

$("#pickerEnd").datetimepicker({
	timepicker: true,
	datepicker: true,
	format: 'Y-m-d H:i',
	step: 5,
	yearStart: new Date().getFullYear(),
	yearEnd: new Date().getFullYear() + 50,
});

document.querySelector('.custom-file-input').addEventListener('change', function (e) {
	let fileName = document.getElementById("image_input").files[0].name;
	let nextSibling = document.getElementById("file-label");
	nextSibling.innerText = fileName;
});


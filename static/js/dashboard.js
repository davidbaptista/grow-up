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

let myMap = L.map('mapid').setView([-68.75, 161.7], 11.5);

L.tileLayer('https://api.maptiler.com/maps/basic/{z}/{x}/{y}.png?key=Pf7U1WtsQP3ciXzxfdEY', {
	maxZoom: 16,
	tileSize: 512,
	attribution: '&copy; <a href="https://openstreetmap.org/copyright">OpenStreetMap contributors</a> | &copy; <a href="https://www.maptiler.com/copyright/" target="_blank">MapTiler</a>',
}).addTo(myMap);


setTimeout(function(){ myMap.invalidateSize()}, 100);



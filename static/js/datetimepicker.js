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
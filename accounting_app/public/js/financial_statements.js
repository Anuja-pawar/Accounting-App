
frappe.provide("accounting.financial_statements");

accounting.financial_statements = {
    "formatter": function (value, row, column, data, default_formatter) {
		value = default_formatter(value, row, column, data);
		if (data.is_group == 1) {
			var head = $(value).css("font-weight", "bold");
			value = head.wrap("<p></p>").parent().html();
		}
		return value;
	}
}
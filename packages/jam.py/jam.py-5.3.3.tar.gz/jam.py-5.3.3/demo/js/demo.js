(function($, task) {
"use strict";

function Events1() { // demo 

	function on_page_loaded(task) {
		
		task.init_tabs($("#content")); // comment this line if you do not want forms in tabs
		task.edit_form_container = $("#content"); // comment this line to have modal edit forms
	
		$("title").text(task.item_caption);
		$("#title").text(task.item_caption);
		 
		if (task.safe_mode) {
			$("#user-info").text(task.user_info.role_name + ' ' + task.user_info.user_name);
			$('#log-out')
			.show() 
			.click(function(e) {
				e.preventDefault();
				task.logout();
			}); 
		}
	
		$("#taskmenu").show();
		task.each_item(function(group) {
			var li,
				ul;
			if (group.visible) {
				li = $('<li class="dropdown"><a class="dropdown-toggle" data-toggle="dropdown" href="#">' + 
					group.item_caption + ' <b class="caret"></b></a></li>');			
				$("#menu").append(li);
				if (group.items.length) {
					ul = $('<ul class="dropdown-menu">'); 
					li.append(ul);
					group.each_item(function(item) {
						if (item.visible && item.can_view()) {
							ul.append($('<li>')
								.append($('<a class="item-menu" href="#">' + item.item_caption + '</a>')
								.data('item', item)));					
						}
					});
				}
			}
		});
	
		$('#menu .item-menu').on('click', (function(e) {
			var item = $(this).data('item'); 
			e.preventDefault();
			if (item.item_type === "report") { 
				item.print(false);
			} 
			else { 
				item.view($("#content"));
			}
		}));
	
		$("#menu").append($('<li></li>').append($('<a href="#">Dashboard</a>').click(function(e) {
			e.preventDefault();
			task.dashboard.view($("#content"));
		})));
	
		$("#menu").append($('li#themes'));
		
		$("#menu-right #admin a").click(function(e) {
			var admin = [location.protocol, '//', location.host, location.pathname, 'builder.html'].join('');
			e.preventDefault();
			window.open(admin, '_blank');
		});
		set_theme(task, 'Bootrap');
		// set_theme(task, 'Cerulean');
		$('#menu #themes ul a').on('click', (function(e) {
			e.preventDefault();		
			set_theme(task, $(this).text().substr(2));
		}));
		$("#menu-right #about a").click(function(e) {
			e.preventDefault();
			task.message(
				task.templates.find('.about'),
				{title: 'Jam.py framework', margin: 0, text_center: true, 
					buttons: {"OK": undefined}, center_buttons: true}
			);
		});
		
		$('#menu .item-menu:first').click(); 
	
		// $(document).ajaxStart(function() { $("html").addClass("wait"); });
		// $(document).ajaxStop(function() { $("html").removeClass("wait"); });
	} 
	
	
	function set_theme(task, theme) {
		var new_css,
			old_css;
		if (!task.theme) {
			task.theme = theme;
			task.small_font = true;
			task.in_container = true;
			task.small_font = false;
			$('#taskmenu #themes ul a').each(function() {
				var theme = $(this).text();
				$(this).html('&nbsp;&nbsp;' + theme);
			});
		}
		if (theme === 'Container') {
			task.in_container = !task.in_container;
			if (task.in_container) {
				$('body #container').removeClass('container-fluid');
				$('body #container').addClass('container');
			}
			else {
				$('body #container').removeClass('container');
				$('body #container').addClass('container-fluid');
			}
			$('#menu .item-menu:first').click();
			$('window').resize();		
		}
		else if (theme === 'Small font') {	
			task.small_font = !task.small_font;
			if (task.small_font) {
				new_css = 'jam12.css';
				old_css = 'jam.css';
			}
			else {
				new_css = 'jam.css';
				old_css = 'jam12.css';
			}
			$("head").find("link").attr("href", function () {
				if (this.href.split('/').pop() === old_css) {
					this.href = this.href.replace(old_css, new_css);
				}
			});
			setTimeout(
				function() {
					$('#menu .item-menu:first').click();
				},
				10
			);
		}
		else {
			new_css = get_theme(task, theme),
			old_css = get_theme(task, task.theme);
			if (theme !== task.theme) {
				$("head").find("link").attr("href", function () {
					if (this.href.split('/').pop() === old_css) {
						this.href = this.href.replace(old_css, new_css);
					}
				});
				task.theme = theme;
				$('window').resize();			
			}
		}
		$('#taskmenu #themes ul a').each(function() {
			var theme = $(this).text().substr(2);
			if (theme === 'Container' && task.in_container) {
				$(this).html('&#x2714;&nbsp;' + theme);
			}		
			else if (theme === 'Small font' && task.small_font) {
				$(this).html('&#x2714;&nbsp;' + theme);
			}		
			else if (theme === task.theme) {
				$(this).html('&#x2714;&nbsp;' +theme);
			}
			else {
				$(this).html('&nbsp;&nbsp;' + theme);			
			}
		});		
	}
	
	function get_theme(task, theme) {
		var css;
		if (theme === 'Bootrap') {
			css = "bootstrap.css";
		}
		else if (theme === 'Cosmo') {
			css = "bootstrap-cosmo.css";
		}
		else if (theme === 'Cerulean') {
			css = "bootstrap-cerulean.css";
		}
		else if (theme === 'Journal') {
			css = "bootstrap-journal.css";
		}
		else if (theme === 'Flatly') {
			css = "bootstrap-flatly.css";
		}
		else if (theme === 'Slate') {
			css = "bootstrap-slate.css";
		}
		else if (theme === 'Amelia') {
			css = "bootstrap-amelia.css";
		}
		else if (theme === 'United') {
			css = "bootstrap-united.css";
		}
		else if (theme === 'Spacelab') {
			css = "bootstrap-spacelab.css";
		}
		else if (theme === 'Readable') {
			css = "bootstrap-readable.css";
		}
		return css;
	}
	
	function on_view_form_created(item) {
		var table_options = {
				height: 620,
				sortable: true,
				freeze_count: 2,
				on_dblclick: function() {
					item.edit_record(task.edit_form_container);
				}
			};
	  
		if (!item.master) {
			item.paginate = true;
		}
	
		item.clear_filters();
	
		if (item.view_form.hasClass('modal')) {
			item.view_options.width = 1060;
			item.view_form.find("#form-title").hide();
		}
		else {
			table_options.height = $(window).height() - $('body').height() - 20;
		}
		if (item.can_create()) {
			item.view_form.find("#new-btn").on('click.task', function(e) { 
				e.preventDefault();
				item.insert_record(task.edit_form_container);
			});
		}
		else {
			item.view_form.find("#new-btn").prop("disabled", true);
		}
		
		item.view_form.find("#edit-btn").on('click.task', function(e) { 
			e.preventDefault();
			item.edit_record(task.edit_form_container);
		});
		
		if (item.can_delete()) {
			item.view_form.find("#delete-btn").on('click.task', function(e) { 
				e.preventDefault();
				item.delete_record(function() {
					item.refresh_page(true);
				}) 
			});
		}
		else {
			item.view_form.find("#delete-btn").prop("disabled", true);
		}
		
		create_print_btns(item);
	
		if (item.view_form.find(".view-table").length) {
			if (item.init_table) {
				item.init_table(item, table_options);
			}
			item.create_table(item.view_form.find(".view-table"), table_options);
			item.open(true);
		}
	}
	
	function on_view_form_closed(item) {
		item.close();
	}
	
	function on_edit_form_created(item) {
		var options = {
				col_count: 1
			};
			
		// item.edit_options.print = true
		item.edit_options.width = 600;
		if (item.init_inputs) {
			item.init_inputs(item, options);
		}
	
		item.create_inputs(item.edit_form.find(".edit-body"), options);
			
		item.edit_form.find("#cancel-btn").on('click.task', function(e) { item.cancel_edit(e) });
		item.edit_form.find("#ok-btn").on('click.task', function() { item.apply_record() });
	}
	
	function on_edit_form_close_query(item) {
		var result = true;
		if (item.is_changing()) {
			if (item.is_modified()) {
				item.yes_no_cancel(task.language.save_changes,
					function() {
						item.apply_record();
					},
					function() {
						item.cancel_edit();
					}
				);
				result = false;
			}
			else {
				item.cancel();
			}
		}
		return result;
	}
	
	function on_filter_form_created(item) {
		item.filter_options.title = item.item_caption + ' - filter';
		item.create_filter_inputs(item.filter_form.find(".edit-body"));
		item.filter_form.find("#cancel-btn")
			.on('click.task', function() { item.close_filter_form() });
		item.filter_form.find("#ok-btn")
			.on('click.task', function() { item.apply_filters() });
	}
	
	function on_param_form_created(item) {
		item.create_param_inputs(item.param_form.find(".edit-body"));
		item.param_form.find("#cancel-btn")
			.on('click.task', function() { item.close_param_form() });
		item.param_form.find("#ok-btn")
			.on('click.task', function() { item.process_report() });
	}
	
	function on_before_print_report(report) {
		var select;
		report.extension = 'pdf';
		if (report.param_form) {
			select = report.param_form.find('select');
			if (select && select.val()) {
				report.extension = select.val();
			}
		}
	}
	
	function on_view_form_keyup(item, event) {
		if (event.keyCode === 45 && event.ctrlKey === true){
			item.insert_record(task.edit_form_container);
		}
		else if (event.keyCode === 46 && event.ctrlKey === true){
			item.delete_record();
		}
	}
	
	function on_edit_form_keyup(item, event) {
		if (event.keyCode === 13 && event.ctrlKey === true){
			item.edit_form.find("#ok-btn").focus();
			item.apply_record();
		}
	}
	
	function create_print_btns(item) {
		var i,
			$ul,
			$li,
			reports = [];
		if (item.reports) {
			for (i = 0; i < item.reports.length; i++) {
				if (item.reports[i].can_view()) {
					reports.push(item.reports[i]);
				}
			}
			if (reports.length) {
				$ul = item.view_form.find("#report-btn ul");
				for (i = 0; i < reports.length; i++) {
					$li = $('<li><a href="#">' + reports[i].item_caption + '</a></li>');
					$li.find('a').data('report', reports[i]);
					$li.on('click', 'a', function(e) {
						e.preventDefault();
						$(this).data('report').print(false);
					});
					$ul.append($li);
				}
			}
			else {
				item.view_form.find("#report-btn").hide();
			}
		}
		else {
			item.view_form.find("#report-btn").hide();
		}
	}
	this.on_page_loaded = on_page_loaded;
	this.set_theme = set_theme;
	this.get_theme = get_theme;
	this.on_view_form_created = on_view_form_created;
	this.on_view_form_closed = on_view_form_closed;
	this.on_edit_form_created = on_edit_form_created;
	this.on_edit_form_close_query = on_edit_form_close_query;
	this.on_filter_form_created = on_filter_form_created;
	this.on_param_form_created = on_param_form_created;
	this.on_before_print_report = on_before_print_report;
	this.on_view_form_keyup = on_view_form_keyup;
	this.on_edit_form_keyup = on_edit_form_keyup;
	this.create_print_btns = create_print_btns;
}

task.events.events1 = new Events1();

function Events2() { // demo.catalogs 

	function on_view_form_created(item) {
		var timeOut,
			i,
			search,
			captions = [],
			field,
			search_field;
		if (item.default_field) {
			search_field = item.default_field.field_name;
		}
		else if (item.view_options.fields.length) {
			for (i = 0; i < item.view_options.fields.length; i++) {
				field = item.field_by_name(item.view_options.fields[i]);
				if (field && can_sort_on_field(field)) {
					search_field = item.view_options.fields[i];
					break;
				}
			}
		}
		if (search_field) {
			item.view_form.find('.header-search').show();
			if (item.lookup_field && item.lookup_field.value && !item.lookup_field.multi_select) {
				item.view_form.find("#selected-value")
					.text(item.lookup_field.display_text)
					.click(function() {
						item.view_form.find('#search-input').val(item.lookup_field.lookup_text);					
						item.search(item.default_field.field_name, item.lookup_field.lookup_text);
					});
				item.view_form.find("#selected-div").css('display', 'inline-block');
			}
			item.view_form.find('#search-fieldname').text(
				item.field_by_name(search_field).field_caption);
			item.view_form.find('#search-field-info')
				.popover({
					container: 'body',
					placement: 'left',
					trigger: 'hover',
					title: 'Search field selection',
					content: 'To select a search field hold Ctrl key and click on the corresponding column of the table.'
				})
				.click(function(e) {
					e.preventDefault();
				});
			search = item.view_form.find("#search-input");
			search.on('input', function() {
				var input = $(this);
				input.css('font-weight', 'normal');
				clearTimeout(timeOut);
				timeOut = setTimeout(function() {
						var field = item.field_by_name(search_field),
							search_type = 'contains_all';
						if (field.lookup_type !== 'text') {
							search_type = 'eq';
						}
						item.search(search_field, input.val(), search_type, function() {
							input.css('font-weight', 'bold');
						});
					},
					500
				);
			});
			search.keydown(function(e) {
				var code = e.which;
				if (code === 13) {
					e.preventDefault();
				}
				else if (code === 40) {
					item.view_form.find('.dbtable.' + item.item_name + ' .inner-table').focus();
	//				item.view_form.find(".inner-table").focus();
					e.preventDefault();
				}
			});
			item.view_form.on('keydown', function(e) {
				var code = e.which;
				if (isCharCode(code) || code === 8) {				
					if (!search.is(":focus")) {
						if (code !== 8) {
							search.val('');
						}
						search.focus();
					}
				}
			});
			item.view_form.on('click.search', '.dbtable.' + item.item_name + ' .inner-table td', function(e) {
				var field;
				if (e.ctrlKey) {			
					if (search_field !== $(this).data('field_name')) {
						search_field = $(this).data('field_name');
						field = item.field_by_name(search_field);
						if (can_sort_on_field(field)) {
							item.view_form.find('#search-fieldname')
								.text(item.field_by_name(search_field).field_caption);
							item.view_form.find("#search-input").val('');
						}
					}
				}
			});
		}
		else {
			item.view_form.find("#search-form").hide();
		}
	}
	
	function can_sort_on_field(field) {
		if (field && field.lookup_type !== "blob" && field.lookup_type !== "currency" &&
			field.lookup_type !== "float" && field.lookup_type !== "boolean" && 
			field.lookup_type !== "date" && field.lookup_type !== "datetime") {
			return true;
		}
	}
	
	function isCharCode(code) {
		if (code >= 48 && code <= 57 || code >= 96 && code <= 105 || 
			code >= 65 && code <= 90 || code >= 186 && code <= 192 || 
			code >= 219 && code <= 222) {
			return true;
		}
	}
	this.on_view_form_created = on_view_form_created;
	this.can_sort_on_field = can_sort_on_field;
	this.isCharCode = isCharCode;
}

task.events.events2 = new Events2();

function Events3() { // demo.journals 

	function on_view_form_created(item) { 
		item.view_form.find("#filter-btn").click(function() {item.create_filter_form()});	
		if (!item.on_filters_applied) {
			item.on_filters_applied = function() {
				if (item.view_form) {
					item.view_form.find(".filter-text").text(item.get_filter_text());		
				}
			};
		}
	}
	
	function on_view_form_shown(item) {
		item.view_form.find('.dbtable.' + item.item_name + ' .inner-table').focus();
	}
	this.on_view_form_created = on_view_form_created;
	this.on_view_form_shown = on_view_form_shown;
}

task.events.events3 = new Events3();

function Events10() { // demo.catalogs.customers 

	function init_table(item, options) {
		if (!item.view_form.hasClass('modal')) {
			item.selections = [];	
		} 
	} 
	 
	function on_view_form_created(item) {
		if (!item.view_form.hasClass('modal')) {	
			item.view_form.find('#email-btn')
				.click(function() {
					if (item.task.mail.can_create()) {
						item.task.mail.open({open_empty: true}); 
						item.task.mail.append_record(); 
					}
					else { 
						item.warning('You are not allowed to send emails.');
					}
				}) 
				.show(); 
			item.view_form.find('#print-btn')
				.click(function() { 
					item.task.customers_report.customers.value = item.selections;
					item.task.customers_report.print(false);
				})
				.show();
		}
		
	}  
	
	function on_edit_form_created(item) {
		var container = item.edit_form.find('.tabs'); 
		task.init_tabs(container);
		item.create_inputs(task.add_tab(container, 'Customer'),
			{fields: ['firstname', 'lastname', 'company', 'support_rep_id']}
		);
		item.create_inputs(task.add_tab(container, 'Address'),
			{fields: ['country', 'state', 'address', 'postalcode']}
		);
		item.create_inputs(task.add_tab(container, 'Contact'),
			{fields: ['phone', 'fax', 'email']}
		);
	}
	this.init_table = init_table;
	this.on_view_form_created = on_view_form_created;
	this.on_edit_form_created = on_edit_form_created;
}

task.events.events10 = new Events10();

function Events15() { // demo.catalogs.tracks 

	function init_table(item, options) {
		options.row_line_count = 2;
		options.expand_selected_row = 3;
		options.column_width = {'artist': '7%'};
	}
	
	function on_edit_form_created(item) {
		item.edit_options.width = 900;
		item.create_inputs(item.edit_form.find("#edit-top"), {fields: ['name']});
		item.create_inputs(item.edit_form.find("#edit-left"), {
			fields: ['album', 'artist', 'composer', 'media_type'],
			label_width: 90
		});
		item.create_inputs(item.edit_form.find("#edit-right"), {
			fields: ['genre', 'milliseconds', 'bytes', 'unitprice'],
			label_width: 90
		}); 
	}
	
	
	function on_view_form_close_query(item) {
		var copy;
		if (item.select_records) {
			if (item.selections.length > 100) {
				item. warning('Too many records selected. Maximum is 100');
				return false;
			}
			else if (item.selections.length) {
				copy = item.copy();
				copy.set_where({id__in: item.selections});
				copy.open(function() {
					var rec_no = item.invoices.invoice_table.record_count();
					item.invoices.invoice_table.disable_controls();
					try {
						copy.each(function(c){
							if (!item.invoices.invoice_table.locate('track', c.id.value)) {
								item.invoices.invoice_table.append();
								item.invoices.invoice_table.track.value = c.id.value;
								item.invoices.invoice_table.track.lookup_value = c.name.value;
								item.invoices.invoice_table.album.lookup_value = c.album.display_text;
								item.invoices.invoice_table.artist.lookup_value = c.artist.display_text;
								item.invoices.invoice_table.unitprice.value = c.unitprice.value;
								item.invoices.invoice_table.quantity.value = 1;
								item.invoices.invoice_table.post();
							}
						});
					}
					finally {
						item.invoices.invoice_table.rec_no = rec_no;
						item.invoices.invoice_table.enable_controls();
						item.invoices.invoice_table.update_controls();
					}
				});
			}
		}
	}
	this.init_table = init_table;
	this.on_edit_form_created = on_edit_form_created;
	this.on_view_form_close_query = on_view_form_close_query;
}

task.events.events15 = new Events15();

function Events16() { // demo.journals.invoices 

	function on_after_append(item) {
		item.date.value = new Date(); 
		item.taxrate.value = 5;
	}
	
	function init_inputs(item, input_options) {
		input_options.col_count = 2;	
	}
	 
	function on_view_form_created(item) {
		var height = $(window).height() - $('body').height() - 200 - 10;
		
		if (height < 200) {
			height = 200;
		}
		
		item.filters.invoicedate1.value = new Date(new Date().setYear(new Date().getFullYear() - 1));
		
		item.create_table(item.view_form.find(".view-master"), {
			height: height,
			sortable: true, 
			show_footer: true,	
			summary_fields: ['date', 'subtotal', 'tax', 'total'],
			freeze_count: 2,
			row_callback: function(row, it) {
				var font_weight = 'normal';
				if (it.total.value > 10) {
					font_weight = 'bold';
				}
				row.find('td.total').css('font-weight', font_weight);
			},
			on_dblclick: function() {
				item.edit_record(task.edit_form_container);
			}
		});	
	
		item.invoice_table.create_table(item.view_form.find(".view-detail"), {
				height: 200 - 4, 
				dblclick_edit: false, 
				column_width: {'track': '25%', 'album': '25%', 'artists': '10%'}
		});
		
		item.open(true);
	}
	
	function on_edit_form_created(item) {
		item.edit_options.width = 1100;
		item.invoice_table.create_table(item.edit_form.find(".edit-detail"),
			{
				height: 300,
				editable: true,
				editable_fields: ['track', 'quantity'],
				selected_field: 'quantity',
				sortable: true,
				column_width: {'track': '25%', 'album': '25%', 'artists': '10%'}
			});
		item.edit_form.find("#new-btn")
			.on('click.task', function() { item.invoice_table.append_record() });
		item.edit_form.find("#edit-btn")
			.on('click.task', function() { item.invoice_table.edit_record() });
		item.edit_form.find("#select-btn")
			.on('click.task', function() { select_records(item) });
		item.edit_form.find("#delete-btn")
			.on('click.task', function() { item.invoice_table.delete_record() });
	}
	
	function select_records(item) {
		var tracks = task.tracks.copy();
		tracks.invoices = item;
		tracks.select_records = true;
		tracks.selections = [];
		tracks.view();
	}
	
	function on_field_get_text(field) {
		if (field.field_name === 'customer' && field.value) {
			return field.owner.firstname.lookup_text + ' ' + field.lookup_text;
		}
	}
	
	function on_field_changed(field, lookup_item) {
		if (field.field_name === 'taxrate') {
			calculate(field.owner, true); 
		}
	}
	
	function calc_total(item) {
		item.amount.value = item.round(item.quantity.value * item.unitprice.value, 2);
		item.tax.value = item.round(item.amount.value * item.owner.taxrate.value / 100, 2);
		item.total.value = item.amount.value + item.tax.value;
	}
	
	function calculate(item, recalc) {
		var subtotal,
			tax,
			total,
			rec;
		if (!item.calculating) {
			item.calculating = true;
			try {
				subtotal = 0;
				tax = 0;
				total = 0;
				item.invoice_table.disable_controls();
				rec = item.invoice_table.rec_no;
				try {
					item.invoice_table.each(function(d) {
						if (recalc) {
							d.edit();
							calc_total(d);
							d.post();
						}
						subtotal += d.amount.value;
						tax += d.tax.value;
						total += d.total.value;
					});
				}
				finally {
					item.invoice_table.rec_no = rec;
					item.invoice_table.enable_controls();
				}
				item.subtotal.value = subtotal;
				item.tax.value = tax;
				item.total.value = total;
				if (recalc) {
					item.invoice_table.update_controls();
				}
			}
			finally {
				item.calculating = false;
			}
		}
	}
	
	function on_edit_form_keyup(item, event) {
		if (event.keyCode === 45 && event.ctrlKey === true){
			item.invoice_table.append_record();
		}
		else if (event.keyCode === 46 && event.ctrlKey === true){
			item.invoice_table.delete_record();
		}
	}
	
	var ScrollTimeOut;
	
	function on_after_scroll(item) {
		clearTimeout(ScrollTimeOut);
		ScrollTimeOut = setTimeout(
			function() {
				item.invoice_table.open(true);
			},
			100
		);
	}
	this.on_after_append = on_after_append;
	this.init_inputs = init_inputs;
	this.on_view_form_created = on_view_form_created;
	this.on_edit_form_created = on_edit_form_created;
	this.select_records = select_records;
	this.on_field_get_text = on_field_get_text;
	this.on_field_changed = on_field_changed;
	this.calc_total = calc_total;
	this.calculate = calculate;
	this.on_edit_form_keyup = on_edit_form_keyup;
	this.on_after_scroll = on_after_scroll;
}

task.events.events16 = new Events16();

function Events18() { // demo.journals.invoices.invoice_table 

	function on_after_post(item) {
		item.owner.calculate(item.owner);
	}
	
	function on_field_changed(field, lookup_item) {
		var item = field.owner;
		if (field.field_name === 'quantity' || field.field_name === 'unitprice') {
			item.owner.calc_total(item);
		}
		else if (field.field_name === 'track' && lookup_item) {
			item.quantity.value = 1;
			item.unitprice.value = lookup_item.unitprice.value;
		}
	}
	
	function on_after_delete(item) {
		item.owner.calculate(item.owner);
	}
	this.on_after_post = on_after_post;
	this.on_field_changed = on_field_changed;
	this.on_after_delete = on_after_delete;
}

task.events.events18 = new Events18();

function Events19() { // demo.reports.invoice 

	function on_before_print_report(report) {
		report.id.value = report.task.invoices.id.value;
	}
	this.on_before_print_report = on_before_print_report;
}

task.events.events19 = new Events19();

function Events20() { // demo.reports.purchases_report 

	function on_param_form_created( report ) {
		var now = new Date();
		if (!report.invoicedate1.value) {
			report.invoicedate1.value = new Date(now.getFullYear() - 1, now.getMonth(), now.getDate());
			report.invoicedate2.value = now;
		}
	}
	this.on_param_form_created = on_param_form_created;
}

task.events.events20 = new Events20();

function Events24() { // demo.analytics.dashboard 

	function on_view_form_created(item) {
		show_cusomers(item, item.view_form.find('#cutomers-canvas').get(0).getContext('2d')),
		show_tracks(item, item.view_form.find('#tracks-canvas').get(0).getContext('2d'));
	}
	
	function show_cusomers(item, ctx) {
		var inv = item.task.invoices.copy({handlers: false});
		inv.open(
			{
				fields: ['customer', 'total'], 
				funcs: {total: 'sum'},
				group_by: ['customer'],
				order_by: ['-total'],
				limit: 10
			}, 
			function() {
				var labels = [],
					data = [],
					colors = [];
				inv.each(function(i) {
					labels.push(i.customer.display_text);
					data.push(i.total.value.toFixed(2));
					colors.push(lighten('#006bb3', (i.rec_no - 1) / 10));
				});
				inv.first();
				draw_chart(item, ctx, labels, data, colors, 'Ten most active customers');
				inv.create_table(item.view_form.find('#customer-table'), 
					{row_count: 10, dblclick_edit: false});		
			}
		);
		return inv;
	}
	
	function show_tracks(item, ctx) {
		var tracks = item.task.tracks.copy({handlers: false});
		tracks.open(
			{
				fields: ['name', 'tracks_sold'], 
				order_by: ['-tracks_sold'],
				limit: 10
			}, 
			
			function() {
				var labels = [],
					data = [],
					colors = [];
				tracks.each(function(t) {
					labels.push(t.name.display_text);
					data.push(t.tracks_sold.value);
					colors.push(lighten('#196619', (t.rec_no - 1) / 10));
				});
				tracks.first();
				tracks.name.field_caption = 'Track';
				draw_chart(item, ctx, labels, data, colors, 'Ten most popular tracks');
				tracks.create_table(item.view_form.find('#tracks-table'), 
					{row_count: 10, dblclick_edit: false});
			}
		);
		return tracks;
	}
	
	function draw_chart(item, ctx, labels, data, colors, title) {
		new Chart(ctx,{
			type: 'pie',
			data: {
				labels: labels,
				datasets: [
					{
						data: data,
						backgroundColor: colors
					}
				]					
			},
			options: {
				 title: {
					display: true,
					fontsize: 14,
					text: title
				},
				legend: {
					position: 'bottom',
				},
			}
		});
	}
	
	function lighten(color, luminosity) {
		color = color.replace(/[^0-9a-f]/gi, '');
		if (color.length < 6) {
			color = color[0]+ color[0]+ color[1]+ color[1]+ color[2]+ color[2];
		}
		luminosity = luminosity || 0;
		var newColor = "#", c, i, black = 0, white = 255;
		for (i = 0; i < 3; i++) {
			c = parseInt(color.substr(i*2,2), 16);
			c = Math.round(Math.min(Math.max(black, c + (luminosity * white)), white)).toString(16);
			newColor += ("00"+c).substr(c.length);
		}
		return newColor; 
	}
	this.on_view_form_created = on_view_form_created;
	this.show_cusomers = show_cusomers;
	this.show_tracks = show_tracks;
	this.draw_chart = draw_chart;
	this.lighten = lighten;
}

task.events.events24 = new Events24();

function Events25() { // demo.catalogs.mail 

	function on_edit_form_created(item) {
		var title = 'Email to ';
		if (item.task.customers.selections.length)
			title += item.task.customers.selections.length + ' selected customers';
		else {
			title += item.task.customers.firstname.value + ' ' +
				item.task.customers.lastname.value;
		}
		item.edit_form.find('.modal-title').text(title);
		item.edit_form.find('#ok-btn')
			.text('Send email')
			.off('click.task')
			.on('click', function() {
				send_email(item);
			});
		item.edit_form.find('textarea.mess').height(120);
	}
	
	function send_email(item) {
		var customers = task.customers.selections;
		try {
			item.post();
			if (!customers.length) {
				customers.push(task.customers.id.value);
			}
			item.server('send_email', [customers, item.subject.value, item.mess.value], 
				function(result, err) {
					if (err) {
						item.warning('Failed to send the mail: ' + err);
						item.edit();
					}
					else {
						item.warning('Successfully sent the mail');
						item.close_edit_form();
						item.delete();			
					}
				}
			);
		}
		catch (e) {}
	}
	this.on_edit_form_created = on_edit_form_created;
	this.send_email = send_email;
}

task.events.events25 = new Events25();

})(jQuery, task)
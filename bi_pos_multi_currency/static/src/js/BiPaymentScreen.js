// odoo.define('bi_pos_multi_currency.BiPaymentScreen', function(require) {

// 	const PaymentScreen = require('point_of_sale.PaymentScreen');
// 	const Registries = require('point_of_sale.Registries');
// 	const NumberBuffer = require('point_of_sale.NumberBuffer');
// 	const session = require('web.session');
// 	const PosComponent = require('point_of_sale.PosComponent');

// 	const { useListener } = require('web.custom_hooks');
// 	let core = require('web.core');
// 	let _t = core._t;
// 	var utils = require('web.utils');

// 	var round_di = utils.round_decimals;
// 	var round_pr = utils.round_precision;

// 	const BiPaymentScreen = PaymentScreen => class extends PaymentScreen {
// 		constructor() {
// 			super(...arguments);
// 			this.mobile_multi = false
// 			useListener('click-update_amount', this._UpdateAmountt);
// 			useListener('click-cur-switch', this._UpdateDetails);
// 			useListener('click-cur-switch-mobile', this._UpdateDetailsMobile);
// 		}

// 		mounted() {
// 			$('#details_mobile').hide()
// 			$('#details').hide()
// 		}

// 		deletePaymentLine(event) {
//         	super.deletePaymentLine(event)
//         	var self = this;
//             let currencies = this.env.pos.poscurrency;
// 			let cur = $('.drop-currency').val();
// 			let curr_sym;
// 			let order= this.env.pos.get_order();
// 			let pos_currency = this.env.pos.currency;
// 			// 
// 			let selected_currency_name = $('.drop-currency option:selected').text();
// 			let finalPaymentMethod =  this.payment_methods_from_config.filter(method => method.name.split("/")[0] == selected_currency_name && method.is_cash_count == true)[0];
		
// 			// for(var i=0;i<currencies.length;i++){
// 			if(cur != pos_currency.id && cur==finalPaymentMethod.id){
// 				$('.next').removeClass('highlight');
// 				let currency_in_pos = (finalPaymentMethod.rate/self.env.pos.currency.rate).toFixed(6);
// 				$('.currency_symbol').text(finalPaymentMethod.symbol);
// 				$('.currency_rate').text(currency_in_pos);
// 				curr_sym = finalPaymentMethod.symbol;
// 				let curr_tot =order.get_due()*currency_in_pos;
// 				$('.currency_cal').text(parseFloat(curr_tot.toFixed(6)));
// 				order.set_curamount(parseFloat(curr_tot.toFixed(6)));
// 				order.set_symbol(curr_sym);
// 				order.set_curname(finalPaymentMethod.name);
// 				return curr_tot;
// 			}
// 			if(cur == pos_currency.id && cur==finalPaymentMethod.id){
// 				$('.currency_symbol').text(pos_currency.symbol);
// 				$('.currency_rate').text(1);
// 				curr_sym = pos_currency.symbol;

// 				let curr_tot =order.get_due();
// 				$('.currency_cal').text(parseFloat(curr_tot.toFixed(6)));
// 				order.set_curamount(parseFloat(curr_tot.toFixed(6)));
// 				order.set_symbol(curr_sym);
// 				order.set_curname(pos_currency.name);
// 				return curr_tot;
// 			}
// 			// }
//         }

// 		_UpdateDetails() {
// 			if($("#cur-switch").prop('checked') == true){
// 				$('#details').hide()
// 			}
// 			else{
// 				$('#details').show()
// 			}
// 		}

// 		_UpdateDetailsMobile() {
// 			if(this.mobile_multi == true){
// 				$('#details_mobile').hide()
				
// 				this.mobile_multi = false
// 			}else{
// 				$('#details_mobile').show()
// 				this.mobile_multi = true
// 			}
// 		}

// 		_UpdateAmountt() {
// 			let self = this;
// 			let order = this.env.pos.get_order();
// 			let paymentlines = this.env.pos.get_order().get_paymentlines();
// 			let open_paymentline = false;
// 			let tot = order.get_curamount();
// 			let tot_amount = 0;
// 			let currency = this.env.pos.poscurrency;
// 			let user_amt = $('.edit-amount').val();
// 			let cur = $('.drop-currency').val();
// 			let payment_methods_from_config = this.env.pos.payment_methods.filter(method => this.env.pos.config.payment_method_ids.includes(method.id));
// 			let selected_paymentline = order.selected_paymentline;
			
// 			let selected_currency_name = $('.drop-currency option:selected').text();
// 			// get payment methods from config
			
// 			let finalPaymentMethod =  this.payment_methods_from_config.filter(method => method.name.split("/")[0] == selected_currency_name && method.is_cash_count == true)[0];
// 			order.add_paymentline(finalPaymentMethod);
// 			// for(var i=0;i<currencies.length;i++){
// 			// raise error if no payment method found
// 			// if(!finalPaymentMethod){
// 			// 	this.showPopup('ErrorPopup', {
// 			// 		title: this.env._t('Error'),
// 			// 		body: this.env._t('No payment method found for selected currency.'),
// 			// 	});
// 			// 	return false;
// 			// }

// 			// for(var i=0;i<currency.length;i++){
// 				if(cur==finalPaymentMethod.id){
// 					let c_rate = self.env.pos.company_currency.rate/finalPaymentMethod.rate;
// 					tot_amount = parseFloat(user_amt)*c_rate;
// 					if(this.env.pos.cash_rounding.length > 0){
// 					    selected_paymentline.amount =round_pr(tot_amount,this.env.pos.cash_rounding[0].rounding);
// 					}
// 					selected_paymentline.amount =parseFloat(tot_amount.toFixed(2));
// 					selected_paymentline.amount_currency = parseFloat(parseFloat(user_amt).toFixed(2));
// 					$('.show-payment').text(this.env.pos.format_currency_no_symbol(selected_paymentline.amount));
// 					selected_paymentline.set_curname(finalPaymentMethod.name);
// 					selected_paymentline.set_curamount(selected_paymentline.amount_currency);
// 					selected_paymentline.set_currency_symbol(finalPaymentMethod.symbol);
// 				}
// 			// }
// 			order.get_paymentlines();
// 			if (!order) {
// 				return;
// 			} else if (order.is_paid()) {
// 				$('.next').addClass('highlight');
// 			}else{
// 				$('.next').removeClass('highlight');
// 			}
// 			$('.edit-amount').val('');
// 			self._ChangeCurrency();
// 			window.document.body.removeEventListener('keypress', self.keyboard_handler);
// 			window.document.body.removeEventListener('keydown', self.keyboard_keydown_handler);
// 		}

// 		_ChangeCurrency() {
// 			let self = this;
// 			let cur = $('.drop-currency').val();
// 			let curr_sym;
// 			let order= this.env.pos.get_order();
// 			let pos_currency = this.env.pos.currency;
// 			let currency = this.env.pos.poscurrency;
// 			// let currency = this.env.pos.poscurrency;
// 			let selected_currency_name = $('.drop-currency option:selected').text();
// 			let finalPaymentMethod =  this.payment_methods_from_config.filter(method => method.name.split("/")[0] == selected_currency_name && method.is_cash_count == true)[0];
// 			// raise error if no payment method found
// 			if(!finalPaymentMethod){
// 				this.showPopup('ErrorPopup', {
// 					title: this.env._t('Error'),
// 					body: this.env._t('No payment method found for selected currency.'),
// 				});
// 				return false;
// 			}
// 			// }

// 			if(selected_currency_name != pos_currency.name){
// 				let currency_in_pos = (currency[parseInt(cur)-1].rate/self.env.pos.currency.rate).toFixed(6);
// 				$('.currency_symbol').text(finalPaymentMethod.symbol);
// 				$('.currency_rate').text(currency_in_pos);
// 				curr_sym = finalPaymentMethod.symbol;

// 				let curr_tot = order.get_due()*currency_in_pos;
// 				$('.currency_cal').text(parseFloat(curr_tot.toFixed(6)));
// 				order.set_curamount(parseFloat(curr_tot.toFixed(6)));
// 				order.set_symbol(curr_sym);
// 				order.set_curname(finalPaymentMethod.name);
// 				return curr_tot;
// 			}
// 			else{
// 				$('.currency_symbol').text(pos_currency.symbol);
// 				$('.currency_rate').text(1);
// 				curr_sym = pos_currency.symbol;
// 				let curr_tot = order.get_due();
// 				$('.currency_cal').text(parseFloat(curr_tot.toFixed(6)));
// 				order.set_curamount(parseFloat(curr_tot.toFixed(6)));
// 				order.set_symbol(curr_sym);
// 				order.set_curname(pos_currency.name);
// 				return curr_tot;
// 			}
// 			// // if(cur == pos_currency.id && cur==finalPaymentMethod.id){
// 			// 	$('.currency_symbol').text(finalPaymentMethod.symbol);
// 			// 	$('.currency_rate').text(1);
// 			// 	let curr_tot =order.get_due();
// 			// 	$('.currency_cal').text(parseFloat(curr_tot.toFixed(6)));
// 			// 	order.set_curamount(parseFloat(curr_tot.toFixed(6)));
// 			// 	order.set_symbol(finalPaymentMethod.symbol);
// 			// 	order.set_curname(finalPaymentMethod.name);
// 			// 	return curr_tot;
// 			// // }
// 			// // }
// 		}
// 	}

// 	Registries.Component.extend(PaymentScreen, BiPaymentScreen);
// 	return PaymentScreen;
// });

odoo.define('bi_pos_multi_currency.BiPaymentScreen', function(require) {

	const PaymentScreen = require('point_of_sale.PaymentScreen');
	const Registries = require('point_of_sale.Registries');
	const NumberBuffer = require('point_of_sale.NumberBuffer');
	const session = require('web.session');
	const PosComponent = require('point_of_sale.PosComponent');

	const { useListener } = require('web.custom_hooks');
	let core = require('web.core');
	let _t = core._t;
	var utils = require('web.utils');

	var round_di = utils.round_decimals;
	var round_pr = utils.round_precision;

	const BiPaymentScreen = PaymentScreen => class extends PaymentScreen {
		constructor() {
			super(...arguments);
			this.mobile_multi = false
			useListener('click-update_amount', this._UpdateAmountt);
			useListener('click-cur-switch', this._UpdateDetails);
			useListener('click-cur-switch-mobile', this._UpdateDetailsMobile);
		}

		mounted() {
			$('#details_mobile').hide()
			$('#details').hide()
		}

		deletePaymentLine(event) {
        	super.deletePaymentLine(event)
        	var self = this;
            let currencies = this.env.pos.poscurrency;
			let cur = $('.drop-currency').val();
			let curr_sym;
			let order= this.env.pos.get_order();
			let pos_currency = this.env.pos.currency;
			for(var i=0;i<currencies.length;i++){
				if(cur != pos_currency.id && cur==currencies[i].id){
					$('.next').removeClass('highlight');
					let currency_in_pos = (currencies[i].rate/self.env.pos.currency.rate).toFixed(6);
					$('.currency_symbol').text(currencies[i].symbol);
					$('.currency_rate').text(currency_in_pos);
					curr_sym = currencies[i].symbol;
					let curr_tot =order.get_due()*currency_in_pos;
					$('.currency_cal').text(parseFloat(curr_tot.toFixed(6)));
					order.set_curamount(parseFloat(curr_tot.toFixed(6)));
					order.set_symbol(curr_sym);
					order.set_curname(currencies[i].name);
					return curr_tot;
				}
				if(cur == pos_currency.id && cur==currencies[i].id){
					$('.currency_symbol').text(pos_currency.symbol);
					$('.currency_rate').text(1);
					curr_sym = pos_currency.symbol;

					let curr_tot =order.get_due();
					$('.currency_cal').text(parseFloat(curr_tot.toFixed(6)));
					order.set_curamount(parseFloat(curr_tot.toFixed(6)));
					order.set_symbol(curr_sym);
					order.set_curname(pos_currency.name);
					return curr_tot;
				}
			}
        }

		_UpdateDetails() {
			if($("#cur-switch").prop('checked') == true){
				$('#details').hide()
			}
			else{
				$('#details').show()
			}
		}

		_UpdateDetailsMobile() {
			if(this.mobile_multi == true){
				$('#details_mobile').hide()
				
				this.mobile_multi = false
			}else{
				$('#details_mobile').show()
				this.mobile_multi = true
			}
		}

		_UpdateAmountt() {
			let self = this;
			let order = this.env.pos.get_order();
			let paymentlines = this.env.pos.get_order().get_paymentlines();
			let open_paymentline = false;
			let tot = order.get_curamount();
			let tot_amount = 0;
			let currency = this.env.pos.poscurrency;
			let user_amt = $('.edit-amount').val();
			let cur = $('.drop-currency').val();
			let payment_methods_from_config = this.env.pos.payment_methods.filter(method => this.env.pos.config.payment_method_ids.includes(method.id));
			let selected_currency_name = $('.drop-currency option:selected').text();
			order.add_paymentline(payment_methods_from_config.filter(method => method.name.split("/")[0] == selected_currency_name && method.is_cash_count == true)[0]);
			let selected_paymentline = order.selected_paymentline;

			for(var i=0;i<currency.length;i++){
				if(cur==currency[i].id){
					let c_rate = self.env.pos.company_currency.rate/currency[i].rate;
					tot_amount = parseFloat(user_amt)*c_rate;
					if(this.env.pos.cash_rounding.length > 0){
					    selected_paymentline.amount =round_pr(tot_amount,this.env.pos.cash_rounding[0].rounding);
					}
					selected_paymentline.amount =parseFloat(tot_amount.toFixed(2));
					selected_paymentline.amount_currency = parseFloat(parseFloat(user_amt).toFixed(2));
					$('.show-payment').text(this.env.pos.format_currency_no_symbol(selected_paymentline.amount));
					selected_paymentline.set_curname(currency[i].name);
					selected_paymentline.set_curamount(selected_paymentline.amount_currency);
					selected_paymentline.set_currency_symbol(currency[i].symbol);
				}
			}
			order.get_paymentlines();
			if (!order) {
				return;
			} else if (order.is_paid()) {
				$('.next').addClass('highlight');
			}else{
				$('.next').removeClass('highlight');
			}
			$('.edit-amount').val('');
			self._ChangeCurrency();
			window.document.body.removeEventListener('keypress', self.keyboard_handler);
			window.document.body.removeEventListener('keydown', self.keyboard_keydown_handler);
		}

		_ChangeCurrency() {
			let self = this;
			let currencies = this.env.pos.poscurrency;
			let selectedCurrencyId = $('.drop-currency').val();
			let curr_sym;
			let order= this.env.pos.get_order();
			let pos_currency = this.env.pos.currency;
			let selected_currency_name = $('.drop-currency option:selected').text();
			let finalPaymentMethod =  this.payment_methods_from_config.filter(method => method.name.split("/")[0] == selected_currency_name && method.is_cash_count == true)[0];
			// raise error if no payment method found
			if(!finalPaymentMethod){
				this.showPopup('ErrorPopup', {
					title: this.env._t('Error'),
					body: this.env._t('No payment method found for selected currency.'),
				});
				return false;
			}
			// }
			for(var i=0;i<currencies.length;i++){
				// case1: if selected currency is not equal to pos currency
				if(selectedCurrencyId != pos_currency.id && selectedCurrencyId==currencies[i].id){
					let currency_in_pos = (currencies[i].rate/self.env.pos.currency.rate).toFixed(6);
					$('.currency_symbol').text(currencies[i].symbol);
					$('.currency_rate').text(currency_in_pos);
					curr_sym = currencies[i].symbol;

					let curr_tot = order.get_due()*currency_in_pos;
					$('.currency_cal').text(parseFloat(curr_tot.toFixed(6)));
					order.set_curamount(parseFloat(curr_tot.toFixed(6)));
					order.set_symbol(curr_sym);
					order.set_curname(currencies[i].name);
					return curr_tot;
				}
				// case2: if selected currency is equal to pos currency
				if(selectedCurrencyId == pos_currency.id && selectedCurrencyId==currencies[i].id){
					$('.currency_symbol').text(pos_currency.symbol);
					$('.currency_rate').text(1);
					curr_sym = pos_currency.symbol;

					let curr_tot =order.get_due();
					$('.currency_cal').text(parseFloat(curr_tot.toFixed(6)));
					order.set_curamount(parseFloat(curr_tot.toFixed(6)));
					order.set_symbol(curr_sym);
					order.set_curname(pos_currency.name);
					return curr_tot;
				}

			}
		}
	}

	Registries.Component.extend(PaymentScreen, BiPaymentScreen);
	return PaymentScreen;
});
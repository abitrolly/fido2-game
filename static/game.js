	//-------------------------------------------------------------------------
	function pause_game() {
		if (paused) {
			paused = false;
			$("#pause_game").html("Сделать паузу");
		}
		else {
			paused = true;
			$("#pause_game").html("Возобновить");
		}
	}
	
	//-------------------------------------------------------------------------
	function progress_bar(title) {
		$("#dialog_title").html(title);
		$("#modal_dialog").show();
		$("#dialog_slider").animate({width: "show"}, "very_slow", function(){inside = false;$("#dialog_slider").hide(); $("#modal_dialog").hide();});
	}
	
	function alert_bar(title, text) {
		$("#alert_title").html(title);
		$("#alert_text").html(text);
		$("#alert_dialog").show();
		$("#alert_slider").animate({width: "show"}, "very_slow", function(){$("#alert_slider").hide(); $("#alert_dialog").hide();});
	}
	
	function message_bar(text) {
		$("#message_text").html(text);
		$("#message_dialog").show();
		$("#message_slider").animate({width: "show"}, "very_slow", function(){$("#message_slider").hide(); $("#message_dialog").hide();});
	}

	//-------------------------------------------------------------------------
	function load_data(id) {
		$.post("/ajax_query/"+id+"/", {}, function(data){$("#RightPanel").html(data);});
	}
	
	//-------------------------------------------------------------------------
	function upgrade(id, cost, title) {
        if (inside) {
           return;
        }
        
		if (money < cost) {
			alert_bar("", "А денег то не хватает на апгрейд!\nРаботать, работать и работать... - как завещал великий В.И.");
		}
		else {
		    inside = true;
			progress_bar("Прикручиваем новую железку - " + title);
			money = money - cost;
			$.post("/ajax_query/upgrade/", {'id': id}, function(data){$("#about_user").html(data);});
		}
	}
	
	//-------------------------------------------------------------------------
	function install_soft(id, need_xp, need_power, cost, title) {
        if (inside) {
           return;
        }
        
		if (pc_power < need_power) {
			alert_bar("", pc + " слабоват для установки " + title + "!\nНужна машина помощнее ;-)");
			return;
		}
		
		if (xp < need_xp) {
			alert_bar("Маловато опыта!", "");
			return;
		}
		
		if (money < cost) {
			alert_bar("", "Коробка с софтом так смотрела на вас...\nНо увы, кошелек отказал во взаимной любви.");
			//window.alert("Коробка с софтом так смотрела на вас...\nНо увы, кошелек отказал во взаимной любви.");
		}
		else {
			inside = true;
			progress_bar("Устанавливаем " + title);
			money = money - cost;
			$.post("/ajax_query/install/", {'id': id}, function(data){$("#about_user").html(data);});
			
		}
	}
	
	//-------------------------------------------------------------------------
	function apply_job(id, title) {
        if (inside) {
           return;
        }

		inside = true;
		message_bar(title + " это хорошо :-)");
		$.post("/ajax_query/apply_job/", {'id': id}, function(data){$("#about_user").html(data);});
	}
	
	//-------------------------------------------------------------------------
	function ToggleItems(id) {
		var div = document.getElementById(id);
		if (div.style.display == 'none') {
			div.style.display = 'block';
		}
		else {
			div.style.display = 'none';
		}
	}
	
	//-------------------------------------------------------------------------
	function job() {
		if (paused) {
			return;
		}
		
		hours_worked += 1;
		if(hours_worked == 16) {
			hours_worked = 0;
			money = money + salary;
			
			today_is += 1;
			$("#today_is").html(today_is);
			$.post("/ajax_query/game_day/", {'today_is': today_is}, function(data){$("#about_user").html(data);});
		}
		$("#time_is").html(8 + hours_worked + ':00');
	}

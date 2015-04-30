// js beginner

function getJSONnoCache(url, data, success){
    $.ajax({
      cache: false,
      url: url,
      dataType: "json",
      data: data,
      success: success
    });
}

function reloadArmStatus(data) {
    if (data.power_on) {
        $(".arm_status").removeClass('label-default');
        $(".arm_status").addClass('label-success');
    }
    else {
        $(".arm_status").removeClass('label-success');
        $(".arm_status").addClass('label-default');
    }
}

function getArmStatus(){
    getJSONnoCache('/api/arm/', {}, reloadArmStatus)
}


function actionArmPart(part_id, duration, action){
    post_data = {
        'duration': duration,
        'action': action
    };
    $.post('/api/arm/'+ part_id + '/', post_data, reloadArmStatus);
}

$('.btnAction').click(function(){
   actionArmPart($(this).data('part-id'), $(this).data('duration'), $(this).data('action'))
});


function fadeFlashedMessage(){
    $('.alert-info').fadeOut(2000);
};


function progressCounter(){
  counter = $('#counter');
  process_value = counter.attr('aria-valuenow');
  process_max = counter.attr('aria-valuemax');
  start_count = false;
  interval = setInterval(function() {
    process_value--;
    percent = 100 * process_value / process_max;
    if (percent > 0) {
      start_count = true;
      counter.attr('aria-valuenow', process_value);
      counter.width(percent + '%');
      counter.text('remain ' + process_value + 's');
    }
    if (percent <= 20) {
      counter.removeClass('progress-bar-success');
      counter.addClass('progress-bar-warning');
    }
    if (percent <= 5) {
      counter.removeClass('progress-bar-success');
      counter.removeClass('progress-bar-warning');
      counter.addClass('progress-bar-danger');
    }
    if (percent <= 0) {
	clearInterval(interval);
	if (start_count == true) {
	    counter.width('100%');
	    counter.text('Time Up. Reloading...');
	    setTimeout(function(){
	        location.reload();
	    }, 2000);
	}
    }
  }, 1000);
};


jQuery(document).ready(function(){
    fadeFlashedMessage();
    getArmStatus();
    progressCounter();
});

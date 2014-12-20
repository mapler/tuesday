// js 初学者, 请多多指点

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
    if (data.is_on) {
        $("#arm_status").addClass('glyphicon glyphicon-ok-sign label-success');
    }
    else {
        $("#arm_status").addClass('glyphicon glyphicon-minus-sign label-default');
    }
    if (data.message != null){
        $("#message").text(data.message);
    }
    $.each(data.parts_status, function(i, part){
        console.log(i + ";" + part.part_id + ";" + part.position);
        $('#part_'+ part.part_id).text(part.position);
    });
}

function getArmStatus(){
    getJSONnoCache('/arm/status/', {}, reloadArmStatus)
}


function actionArmPart(part_id, duration, action){
    post_data = {
        'duration': duration,
        'action': action
    };
    $.post('/arm/status/'+ part_id + '/', post_data, reloadArmStatus);
}

$('.btn').click(function(){
   actionArmPart($(this).data('part-id'), $(this).data('duration'), $(this).data('action'))
});


jQuery(document).ready(function(){
    getArmStatus();
});
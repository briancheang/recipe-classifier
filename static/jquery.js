$(document).ready(function() {
  $('a[data-toggle="tab"]').on('shown.bs.tab', function (event) {
    event.preventDefault;
    $.ajax({
      type : 'DELETE',
      url : '/reset'
    }).done(function(tuple) {
      $('#pid').html(tuple.prediction);
      $('#list-ingredients').empty();
      $('#warning').remove();
      updateChart();
    });
});
$('#reset').on('click', function(event) {
  event.preventDefault();
  $.ajax({
    type : 'DELETE',
    url : '/reset'
  }).done(function(tuple) {
    $('#pid').html(tuple.prediction);
    $('#list-ingredients').empty();
    updateChart();
  });
});

  var count = 0;
  var valid = "default";
  var exists = "default";
  $('#submit2').on('click', function(event) {
    event.preventDefault();
    $.ajax({
      data : {
        recipe : $('#copy_recipe').val()
      },
      type : 'POST',
      url : '/update2'
    }).done(function(tuple) {
      $('#pid').html(tuple.prediction2);
      $('#copy_recipe').val("");
      var item = document.createElement("li");
      item.setAttribute("class", "list-group-item");
      item.setAttribute("id", "recognized");
      var span = document.createElement('span');
      span.appendChild(document.createTextNode("Recognized Ingredients: " + tuple.defined))
      item.appendChild(span)
      $('#recognized').remove()
      //$('#recognized-features').append(item)
      updateChart();
    });
  });
	$('#submit').on('click', function(event) {
    event.preventDefault();
    comment = $('#input').val()
		$.ajax({
			data : {
				ingredient : comment
			},
			type : 'POST',
			url : '/update',
      async: false
		}).done(function(tuple) {
      $('#pid').html(tuple.prediction);
      $('#input').val("");
      valid = tuple.valid;
      exists = tuple.exists;
       if(tuple.valid == "false" && comment != "") {
         var item = document.createElement("li");
         item.setAttribute("class", "list-group-item");
         item.setAttribute("id", "warning");
         var span = document.createElement('span');
         span.setAttribute("style", "color: grey");
         span.appendChild(document.createTextNode("'" + tuple.data + "' is not a valid feature."))
         item.appendChild(span)
         item.setAttribute("style", "background-color: transparent; border-radius: 0; color: #fff;")
         $('#warning').remove();
         $('#feature-valid').append(item)
       }
       else {
        $('#warning').remove();
        updateChart();
       }
    }
  );
    var item = document.createElement("li");
    item.setAttribute("class", "list-group-item");
    item.appendChild(document.createTextNode(comment))
    var bt = document.createElement("button");
    bt.setAttribute('name', comment)
    bt.setAttribute("type", "button");
    bt.setAttribute("class", "close");
    bt.setAttribute("aria-label", "close")
    bt.appendChild(document.createTextNode('x'))
    item.appendChild(bt)
    if(valid != "false" && exists == "false") {
      $('#list-ingredients').append(item);
    }

    $('.close').on('click', function() {
      $.ajax({
  			data : {
  				ingredient : $(this).attr("name")
  			},
  			type : 'DELETE',
  			url : '/update'
  		}).done(function(tuple) {
        $('#pid').html(tuple.prediction);
        $('#warning').remove();
        updateChart();
      });
      $(this).closest('.list-group-item').remove()
    });

	});
});

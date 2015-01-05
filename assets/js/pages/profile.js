initialisePage();

function initialisePage() {
    user.getAll(function(success, data) {
        // $('#user-info-div').html("");
        var template = '<div class="col-md-9" id="user-info-div" style="font-size:16px;"><label class="read-only-form-label">given name:</label>{{name}}<br><label class="read-only-form-label">family name:</label>{{familyName}}<br><label class="read-only-form-label">email:</label>{{email}}<br></div>';

        var imgTemplate = '<img src="{{profilePicture}}" class="img-circle img-profile">';

        $('#user-profile').append( processTemplate(template, data[0]) );
        $('#profile-picture-div').append( processTemplate(imgTemplate, data[0]) );
    });
    dumpNotifications();
}

function dumpNotifications() {
  notifications.getAll(function(success, data) {
    var template = '<div class="col-md-12 profileNotification {{readOnly.notificationType}}" style="border-bottom:1px solid #616161;">{{content}} </div>';
    console.log(data);
    var maxLength = (data.length >= 11) ? 10 : data.length;
    for(i=0; i < maxLength; i++) {
      data[i].readOnly.notificationType = returnNotificationTypeCSS(data[i].type)
      $("#notification-content-div").append( processTemplate(template, data[i]) );
    }
  });
}

function returnNotificationTypeCSS(notificationType) {
  var typeCSS = "";
  switch (notificationType) {
    case "FRIEND_REQUEST":
      typeCSS = "friendRequestNotification";
      break;
    case "INFO":
      typeCSS = "infoNotification";
      break;
    case "ERROR":
      typeCSS = "errorNotification";
      break;
    case "MISC":
      typeCSS = "miscNotification";
      break;
    case "SUCCESS":
      typeCSS = "successNotification";
      break;
  }
    return typeCSS;
}

function markNotificationsSeen() {
  notifications.getAll(function(success, data) {
    for (var i = 0; i < data.length; i++) {
      data[i].seen = true;
      data[i].update();
    }
  });
}


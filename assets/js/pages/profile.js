initialisePage();

function initialisePage() {
    user.getAll(function(success, data) {
        // $('#user-info-div').html("");
        var template = '<div class="col-md-8" id="user-info-div" style="font-size:16px;"><label class="read-only-form-label">given name:</label>{{name}}<br><label class="read-only-form-label">family name:</label>{{familyName}}<br><label class="read-only-form-label">email:</label>{{email}}<br></div>';

        var imgTemplate = '<img src="{{profilePicture}}" class="img-circle img-profile">';

        $('#user-profile').append( processTemplate(template, data[0]) );
        $('#profile-picture-div').append( processTemplate(imgTemplate, data[0]) );
    });
}
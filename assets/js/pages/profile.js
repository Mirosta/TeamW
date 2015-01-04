initialisePage();

function initialisePage() {
    user.getAll(function(success, data) {
        // $('#user-info-div').html("");
        var template = '<div class="col-md-7" id="user-info-div" style="font-size:16px;"><label class="read-only-form-label">given name:</label>{{name}}<br><label class="read-only-form-label">family name:</label>{{familyName}}<br><label class="read-only-form-label">email:</label>{{email}}<br></div>';
        var div = processTemplate(template, data[0]);
        $('#user-profile').append(div);
        console.log(data[0]);
    });
}
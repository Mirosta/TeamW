//Processes a template string replacing {{someName}} with the value of the templateValues[someName] property
function processTemplate(template, templateValues)
{
    var offset = 0;
    var output = "";

    while(offset < template.length) //Loop over template string
    {
        var nextValue = template.indexOf('{{', offset); //Find beginning of variable
        var endValue = template.indexOf('}}', nextValue); //Find end of variable
        var outputLength = 0; //How many characters of the original template string we have added to the output in this loop
        var variableValue = ""; //String value of variable
        var additionalSkip = 0; //How long the variable definition was

        if(nextValue >= 0 && endValue >= 0)
        {
            var variableName = template.substring(nextValue + 2, endValue);
            variableValue = getVariable(templateValues, variableName.split("."), 0);
            additionalSkip = endValue - nextValue + 2;
            outputLength = nextValue - offset;
        }
        else
        {
            outputLength = template.length - offset;
        }
        output += template.substring(offset, offset + outputLength) + variableValue;
        offset += outputLength + additionalSkip;
    }

    return output;
}

function getVariable(templateValues, variableParts, offset)
{
    if(offset >= variableParts.length - 1)
    {
        if(typeof templateValues[variableParts[offset]] !== "undefined") return templateValues[variableParts[offset]].toString();
        else return "";
    }
    if(typeof templateValues[variableParts[offset]] !== "undefined") return getVariable(templateValues[variableParts[offset]], variableParts, ++offset);
    else return "";
}

//Makes a copy of the given object and removes the fields given
//Please note that serializing to JSON will remove functions anyway, so this is not necessary
//Also note that this is a shallow copy, properties containing references to objects will still reference the same objects
function stripNonSerializableFields (obj, fields)
{
    var copy = {};
    for(key in obj) //Loop over object properties
    {
        copy[key] = obj[key]; //Copy value of property
    }

    for(var i = 0; i < fields.length; i++)
    {
        delete copy[fields[i]];
    }

    return copy;
}

//Convenience method for apiCall
//Callback is in form function(boolean success, (string | object) errorOrObject)
function apiPost(url, object, callback)
{
    apiCall(url, "POST", object, callback);
}

//Convenience method for apiCall
//Callback is in form function(boolean success, (string | object) errorOrObject)
function apiGet(url, callback)
{
    apiCall(url, "GET", null, callback);
}

//Callback is in form function(boolean success, (string | object) errorOrObject)
function apiCall(url, httpMethod, object, callback)
{
    var json = "";
    if(object) json = JSON.stringify(object);
    console.log('Performing ' + httpMethod + ' on ' + url);
    console.log('Sending ' + json);
    $.ajax({
        type: httpMethod,
        data: json,
        url: url,
        success: function (data) {    //Callback from successful http request
            if(data && data.error && callback) callback(false, data.error);
            if (callback) callback(true, data);
        },
        error: function (request, status) { //Callback on error
            if (callback) callback(false, status);
        },
        dataType: "json"
    });
}
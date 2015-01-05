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
            variableValue = getVariable(templateValues, variableName.split("."), 0).toString();
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
        if(templateValues[variableParts[offset]] !== undefined && templateValues[variableParts[offset]] !== null) return templateValues[variableParts[offset]];
        else return "";
    }
    if(templateValues[variableParts[offset]] !== undefined && templateValues[variableParts[offset]] !== null) return getVariable(templateValues[variableParts[offset]], variableParts, ++offset);
    else return "";
}

function setVariable(templateValues, variableParts, offset, value, arrayIndex)
{
    if(offset >= variableParts.length - 1)
    {
        if(templateValues[variableParts[offset]] !== undefined && templateValues[variableParts[offset]] !== null)
            if (arrayIndex === undefined || arrayIndex ===null) templateValues[variableParts[offset]] = value;
            else templateValues[variableParts[offset]][arrayIndex] = value;
    }
    if(templateValues[variableParts[offset]] !== undefined && templateValues[variableParts[offset]] !== null) setVariable(templateValues[variableParts[offset]], variableParts, ++offset, value, arrayIndex);
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

//Callback is in format function(success, data)
function lookupField(types, object, callback)
{
    var noTypes = 0;
    for(type in types)
    {
        noTypes+= types[type].length;
    }
    var typeSynch = new Synchronise(noTypes,
        function(success, error)
        {
            if(success) callback(success, object);
            else callback(success, error);
        });
    var typeComplete = function(success, error)
    {
        if(success) typeSynch.complete();
        else typeSynch.failed(error);
    };

    for(type in types)
    {
        for(var i = 0; i < types[type].length; i++)
        {
            var objectParts = types[type][i].split(".");
            var key = getVariable(object, objectParts, 0);
            if(key.constructor === Array)
            {
                var synch = new Synchronise(key.length, typeComplete);
                for(var k = 0; k < key.length; k++)
                {
                    var subKey = key[k];
                    var objectForKey = models[type].get(subKey, onFieldLookup(object, objectParts, k, synch));
                }
            }
            else
            {
                var objectForKey = models[type].get(key, onFieldLookup(object, objectParts, undefined, typeSynch));
            }
        }
    }
}

//Callback is function(success, error)
function Synchronise(count, callback)
{
    this.count = count;
    this.progress = 0;
    this.hasFailed = false;
    this.complete = function()
    {
        this.progress++;
        if(this.progress >= this.count && !this.hasFailed)
        {
            callback(true);
        }
    };
    this.failed = function(error)
    {
        this.hasFailed = true;
        callback(false, error);
    };
}

function onFieldLookup(object, objectParts, offset, synchronise)
{
    return function (success, data)
    {
        if(success)
        {
            setVariable(object, objectParts, 0, data, offset);
            synchronise.complete();
        }
        else
        {
            synchronise.failed(data);
        }
    };
}

// Convert pence to £XX.XX
function penceToPound(amount) {
  var negative = amount < 0;
  if(negative) amount = -amount;
  
  var decimal = amount % 100;
  var whole = (amount - decimal)/100;
  if(decimal < 10) decimal = "0" + decimal;
  
  return (negative ? "-" : "") + "£" + whole + "." + decimal;
}